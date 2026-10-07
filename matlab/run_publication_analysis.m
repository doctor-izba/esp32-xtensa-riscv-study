function run_publication_analysis(repoRoot)
% Generate publication-width, grayscale-safe figures from accepted processed data.
arguments
    repoRoot (1,1) string = string(fileparts(fileparts(mfilename('fullpath'))))
end
outDir=fullfile(repoRoot,"artifacts","matlab","publication");
if ~isfolder(outDir), mkdir(outDir); end
set(groot,'defaultAxesFontName','DejaVu Sans','defaultTextFontName','DejaVu Sans');
L=readtable(fullfile(repoRoot,"data","processed","mode_a_largest_input_summary.csv"),TextType="string",VariableNamingRule="preserve");
T=readtable(fullfile(repoRoot,"data","processed","mode_a_cross_workload_summary.csv"),TextType="string",VariableNamingRule="preserve");
B=readtable(fullfile(repoRoot,"data","processed","mode_b_summary.csv"),TextType="string",VariableNamingRule="preserve");
workloads=["CRC32","SHA256","FFT_I16","FIR_F32","IIR_BQ_F32"];
labels=["CRC-32","SHA-256","FFT (Q15)","FIR (binary32)","IIR (binary32)"];
langs=["c_cpp","rust","micropython"];

% Figure 1: descriptive historical/local ratio; points avoid bar-baseline semantics.
M=nan(5,3);
for i=1:5, for j=1:3, q=L.workload==workloads(i)&L.language==langs(j); M(i,j)=L.plauska_over_esp32c6_mean(q); end, end
f=figure('Visible','off','Color','w','Units','inches','Position',[1 1 7.0 3.5]); hold on;
mk=['o','s','^']; shades=[0.05 0.38 0.68];
displayNames=["C/C++","Rust","MicroPython"];
for j=1:3, semilogy(1:5,M(:,j),LineStyle='none',Marker=mk(j),MarkerSize=7,MarkerFaceColor=[shades(j) shades(j) shades(j)],MarkerEdgeColor='k',DisplayName=displayNames(j)); end
yline(1,'k--','equal mean','LabelHorizontalAlignment','left','HandleVisibility','off');
set(gca,'YScale','log','YLim',[0.05 5],'XTick',1:5,'XTickLabel',labels,'FontSize',9,'TickLabelInterpreter','none');
ylabel({'Published Plauska mean /','new C6 mean (log scale)'}); xlim([0.65 5.35]); grid on; box on;
legend('Location','northoutside','Orientation','horizontal');
export_all(f,outDir,'mode_a_historical_local'); close(f);

% Figure 2: meaningful sizes only; zero-size overhead remains in CSV evidence.
f=figure('Visible','off','Color','w','Units','inches','Position',[1 1 7.0 3.7]); hold on;
styles={'-o','--s','-.^',':d','-x'};
for i=1:5
    q=T.workload==workloads(i)&T.language=="c_cpp";
    ratios=T.rust_over_cpp_median(q);
    plot(1:7,ratios(2:8),styles{i},Color=[0.12+0.14*(i-1) 0.12+0.14*(i-1) 0.12+0.14*(i-1)],LineWidth=1.2,MarkerSize=5,DisplayName=labels(i));
end
yline(1,'k--','parity','LabelHorizontalAlignment','right','HandleVisibility','off');
set(gca,'XTick',1:7,'XTickLabel',{'16','32','64','128','256','512','1024'},'FontSize',9);
xlabel('Frozen input size (workload units)'); ylabel('Rust median / C++ median'); xlim([0.7 7.3]); ylim([0.62 1.34]); grid on; box on;
legend('Location','eastoutside');
export_all(f,outDir,'mode_a_rust_cpp'); close(f);

% Figure 3: within-language compiler profile response.
largest=B(B.input_size==1024 & B.optimization=="COMPILER_PERF",:);
V=nan(5,2);
for i=1:5, for j=1:2, q=largest.workload==workloads(i)&largest.language==langs(j); V(i,j)=largest.mode_b_over_mode_a_median(q); end, end
f=figure('Visible','off','Color','w','Units','inches','Position',[1 1 7.0 3.4]); hold on;
plot(1:5,V(:,1),'-o',Color=[0.1 0.1 0.1],MarkerFaceColor='w',LineWidth=1.2,DisplayName='C/C++: GCC -O2');
plot(1:5,V(:,2),'--s',Color=[0.5 0.5 0.5],MarkerFaceColor=[0.5 0.5 0.5],MarkerEdgeColor='k',LineWidth=1.2,DisplayName='Rust: opt-level 3');
yline(1,'k--','Mode A','LabelHorizontalAlignment','right','HandleVisibility','off');
set(gca,'XTick',1:5,'XTickLabel',labels,'FontSize',9,'TickLabelInterpreter','none');
ylabel('Performance profile / Mode A median'); xlim([0.65 5.35]); ylim([0.70 1.10]); grid on; box on;
legend('Location','northoutside','Orientation','horizontal');
export_all(f,outDir,'mode_b_compiler_response'); close(f);

% Figure 4: log-scale point overview plus zero-baseline software detail.
sha=B(B.input_size==1024 & B.language=="c_cpp" & (B.workload=="SHA256"|B.workload=="SHA256_HW"),:);
a=sha.mode_a_median_us(1); perf=sha.mode_b_median_us(sha.optimization=="COMPILER_PERF"); hw=sha.mode_b_median_us(sha.optimization=="HW_SHA");
f=figure('Visible','off','Color','w','Units','inches','Position',[1 1 7.0 3.4]); tl=tiledlayout(1,2,'TileSpacing','compact','Padding','compact');
nexttile; v=[a perf hw]; semilogy(1:3,v,'o',LineStyle='none',MarkerSize=8,MarkerFaceColor=[0.35 0.35 0.35],MarkerEdgeColor='k'); set(gca,'XTick',1:3,'XTickLabel',{'Mode A','GCC -O2','HW SHA'},'FontSize',8); xtickangle(18); xlim([0.55 3.45]); ylabel('Median time (us, log scale)'); ylim([50 900]); grid on; box on; title('Complete C6 profiles');
for i=1:3, text(i,v(i),sprintf('%.0f',v(i)),HorizontalAlignment='center',VerticalAlignment='bottom',FontSize=8); end
nexttile; v=[a perf]; bar(v,FaceColor=[0.8 0.8 0.8],EdgeColor='k'); set(gca,'XTickLabel',{'Mode A SW','GCC -O2 SW'},'FontSize',8); ylabel('Median time (us)'); ylim([0 750]); grid on; title('Software detail');
for i=1:2, text(i,v(i),sprintf('%.0f',v(i)),HorizontalAlignment='center',VerticalAlignment='bottom',FontSize=8); end
title(tl,'SHA-256 at 1024 bytes'); tl.Title.FontName='DejaVu Sans';
export_all(f,outDir,'mode_b_sha_profiles'); close(f);

writetable(L,fullfile(outDir,'mode_a_largest_input_source.csv'));
writetable(largest,fullfile(outDir,'mode_b_largest_input_source.csv'));
fid=fopen(fullfile(outDir,'MATLAB_RUN.txt'),'w'); fprintf(fid,'MATLAB %s\nGenerated by matlab/run_publication_analysis.m\n',version); fclose(fid);
disp('PUBLICATION_MATLAB_PASS')
end

function export_all(f,outDir,name)
set(findall(f,'-property','FontName'),'FontName','DejaVu Sans');
savefig(f,fullfile(outDir,name+".fig"));
exportgraphics(f,fullfile(outDir,name+".pdf"),ContentType='vector');
exportgraphics(f,fullfile(outDir,name+".png"),Resolution=600);
end

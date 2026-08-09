function run_mode_a_cross_workload_analysis(repoRoot)
% Reproduce cross-workload Mode A tables and figures from processed CSV only.
arguments
    repoRoot (1,1) string = string(fileparts(fileparts(mfilename('fullpath'))))
end
inputFile = fullfile(repoRoot,"data","processed","mode_a_cross_workload_summary.csv");
largestFile = fullfile(repoRoot,"data","processed","mode_a_largest_input_summary.csv");
outDir = fullfile(repoRoot,"artifacts","matlab","mode_a_cross_workload");
if ~isfolder(outDir), mkdir(outDir); end
T = readtable(inputFile,TextType="string",VariableNamingRule="preserve");
L = readtable(largestFile,TextType="string",VariableNamingRule="preserve");
assert(height(T)==120 && height(L)==15,"Unexpected synthesis row count");
workloads = ["CRC32","SHA256","FFT_I16","FIR_F32","IIR_BQ_F32"];
languages = ["c_cpp","rust","micropython"];
M = nan(numel(workloads),numel(languages));
for i=1:numel(workloads)
    for j=1:numel(languages)
        q=L.workload==workloads(i) & L.language==languages(j);
        M(i,j)=L.plauska_over_esp32c6_mean(q);
    end
end

f=figure(Color="w",Position=[100 100 1050 560]);
b=bar(categorical(workloads,workloads),M); set(gca,YScale="log",FontSize=11,TickLabelInterpreter="none");
ymin=min(M,[],'all'); ymax=max(M,[],'all'); ylim([10^(floor(log10(ymin))-0.1) 10^(ceil(log10(ymax))+0.1)]);
yline(1,"k--","equal mean time",LabelHorizontalAlignment="left",HandleVisibility="off");
ylabel("Plauska mean / ESP32-C6 mean (log scale)"); xlabel("Workload");
legend(b,["C/C++","Rust","MicroPython"],Location="best"); grid on;
title("Mode A historical/local timing ratio at largest common input");
subtitle("Published Plauska mean / new physical C6 mean; descriptive, not a treatment effect");
for i=1:numel(workloads)
    for j=1:numel(languages)
        text(b(j).XEndPoints(i),M(i,j),sprintf('%.3g',M(i,j)), ...
            HorizontalAlignment="center",VerticalAlignment="bottom",FontSize=8);
    end
end
exportgraphics(f,fullfile(outDir,"figure1_historical_local_ratio.png"),Resolution=300);
exportgraphics(f,fullfile(outDir,"figure1_historical_local_ratio.pdf"),ContentType="vector");
savefig(f,fullfile(outDir,"figure1_historical_local_ratio.fig")); close(f);

f=figure(Color="w",Position=[100 100 1050 560]); hold on;
for i=1:numel(workloads)
    q=T.workload==workloads(i) & T.language=="c_cpp";
    plot((1:sum(q))',T.rust_over_cpp_median(q),"-o",LineWidth=1.5,DisplayName=workloads(i));
end
yline(1,"k--","parity",HandleVisibility="off"); xlabel("Frozen input-size position (0, 16, 32, 64, 128, 256, 512, 1024)");
ylabel("Rust / C++ median time"); grid on; set(gca,FontSize=11);
legend(Location="best",Interpreter="none"); title("ESP32-C6 Mode A Rust/C++ ratio across workloads");
exportgraphics(f,fullfile(outDir,"figure2_rust_cpp_ratio.png"),Resolution=300);
exportgraphics(f,fullfile(outDir,"figure2_rust_cpp_ratio.pdf"),ContentType="vector");
savefig(f,fullfile(outDir,"figure2_rust_cpp_ratio.fig")); close(f);

N=M(:,1:2);
f=figure(Color="w",Position=[100 100 1000 540]);
b=bar(categorical(workloads,workloads),N); set(gca,YScale="log",FontSize=11,TickLabelInterpreter="none");
yline(1,"k--","equal mean time",HandleVisibility="off"); ylabel("Plauska mean / ESP32-C6 mean (log scale)");
xlabel("Workload"); legend(b,["C/C++","Rust"],Location="best"); grid on;
title("Native Mode A historical/local contrast at largest common input");
exportgraphics(f,fullfile(outDir,"figure3_native_historical_local.png"),Resolution=300);
exportgraphics(f,fullfile(outDir,"figure3_native_historical_local.pdf"),ContentType="vector");
savefig(f,fullfile(outDir,"figure3_native_historical_local.fig")); close(f);

f=figure(Color="w",Position=[100 100 1050 560]);
scatter(1:5,N(:,1),90,"filled",DisplayName="C/C++"); hold on;
scatter(1:5,N(:,2),90,"filled",DisplayName="Rust");
set(gca,YScale="log",XTick=1:5,XTickLabel=workloads,FontSize=11,TickLabelInterpreter="none"); grid on;
yline(1,"k--","equal mean time",HandleVisibility="off"); ylabel("Plauska mean / ESP32-C6 mean (log scale)");
xlabel("Workload (first three integer/fixed; last two binary32)"); legend(Location="best");
title("Descriptive native historical/local pattern by workload arithmetic");
subtitle("Five-workload pattern is hypothesis-generating; no arithmetic or ISA treatment is isolated");
exportgraphics(f,fullfile(outDir,"figure4_arithmetic_class_contrast.png"),Resolution=300);
exportgraphics(f,fullfile(outDir,"figure4_arithmetic_class_contrast.pdf"),ContentType="vector");
savefig(f,fullfile(outDir,"figure4_arithmetic_class_contrast.fig")); close(f);

writetable(L,fullfile(outDir,"largest_input_plot_data.csv"));
R=T(T.language=="c_cpp",["workload","input_size","input_size_field","rust_over_cpp_median","micropython_over_cpp_median"]);
writetable(R,fullfile(outDir,"language_ratio_plot_data.csv"));
generatedAt=datetime('now','TimeZone','UTC','Format','yyyy-MM-dd''T''HH:mm:ss''Z''');
E=table(string(version),string(computer),string(generatedAt), ...
    'VariableNames',{'matlab_version','computer','generated_at_utc'});
writetable(E,fullfile(outDir,"analysis_environment.csv"));
end

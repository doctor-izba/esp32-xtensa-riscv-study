function run_sha256_mode_a_analysis(repositoryRoot)
%RUN_SHA256_MODE_A_ANALYSIS Validate and plot ESP32-C6 SHA-256 Mode A data.

arguments
    repositoryRoot (1,1) string
end

inputPath = fullfile(repositoryRoot, "data", "processed", ...
    "sha256_mode_a_esp32c6_observations.csv");
outputDir = fullfile(repositoryRoot, "artifacts", "matlab", "sha256_mode_a");
if ~isfolder(outputDir); mkdir(outputDir); end
data = readtable(inputPath, TextType="string", VariableNamingRule="preserve");
required = ["run_id","chip","language","benchmark","mode","input_bytes", ...
    "iteration","batch_count","total_batch_time_us", ...
    "normalized_time_per_call_us","digest","expected_digest", ...
    "correctness_pass","measurement_status"];
assert(all(ismember(required,string(data.Properties.VariableNames))), ...
    "SHA256:Schema", "Processed CSV lacks required named columns.");
assert(height(data)==2400, "SHA256:Rows", "Expected exactly 2400 rows.");
assert(all(data.mode=="A") && all(data.benchmark=="SHA256"), ...
    "SHA256:Mode", "Unexpected benchmark or mode.");
assert(all(data.correctness_pass=="true") && all(data.measurement_status=="valid"), ...
    "SHA256:Validity", "Only correct valid rows may be analyzed.");

languages = ["c_cpp","rust","micropython"];
labels = ["C++","Rust","MicroPython"];
sizes = [0,16,32,64,128,256,512,1024];
expectedBatch = [4,4,4,2,1,1,1,1; 4,4,4,2,1,1,1,1; 1,1,1,1,1,1,1,1];
medians = zeros(8,3); q1 = zeros(8,3); q3 = zeros(8,3);
summary = table();
for li=1:3
    for si=1:8
        mask = data.language==languages(li) & data.input_bytes==sizes(si);
        values = data.normalized_time_per_call_us(mask);
        assert(numel(values)==100 && all(data.iteration(mask)==(1:100)'), ...
            "SHA256:Grid", "Each condition requires iterations 1..100.");
        assert(all(data.batch_count(mask)==expectedBatch(li,si)), ...
            "SHA256:Batch", "Frozen batch mismatch.");
        reconstructed = data.total_batch_time_us(mask)./data.batch_count(mask);
        assert(all(abs(reconstructed-values)<=5.1e-10), ...
            "SHA256:Normalization", "Raw batch/count reconstruction failed.");
        medians(si,li)=median(values); q1(si,li)=prctile(values,25); q3(si,li)=prctile(values,75);
        row = table(languages(li),sizes(si),numel(values),mean(values),median(values), ...
            std(values),prctile(values,25),prctile(values,75),min(values),max(values), ...
            'VariableNames',{'language','input_bytes','n','mean_us','median_us','std_us', ...
            'q1_us','q3_us','min_us','max_us'});
        summary=[summary;row]; %#ok<AGROW>
    end
end
writetable(summary,fullfile(outputDir,"sha256_mode_a_summary.csv"));
colors=[0 .447 .741; .85 .325 .098; .494 .184 .556];

f1=figure("Visible","off","Color","white","Position",[100 100 1100 680]); ax=axes(f1); hold(ax,"on");
for li=1:3
    errorbar(ax,sizes,medians(:,li),medians(:,li)-q1(:,li),q3(:,li)-medians(:,li), ...
        "-o","LineWidth",1.8,"MarkerSize",6,"Color",colors(li,:),"DisplayName",labels(li));
end
set(ax,"YScale","log","FontSize",12,"Box","on"); grid(ax,"on");
xlabel(ax,"Input prefix (bytes)"); ylabel(ax,"SHA-256 time per call (\mus, log scale)");
title(ax,"Mode A software SHA-256 on ESP32-C6 (median and IQR, n = 100)");
legend(ax,"Location","northwest");
exportgraphics(f1,fullfile(outputDir,"figure1_sha256_execution_time.png"),"Resolution",300);
exportgraphics(f1,fullfile(outputDir,"figure1_sha256_execution_time.pdf"),"ContentType","vector");
savefig(f1,fullfile(outputDir,"figure1_sha256_execution_time.fig")); close(f1);

ratios=medians./medians(:,1); normalized=table();
for li=1:3
    normalized=[normalized; table(repmat(languages(li),8,1),sizes',ratios(:,li), ...
        'VariableNames',{'language','input_bytes','median_time_relative_to_cpp'})]; %#ok<AGROW>
end
writetable(normalized,fullfile(outputDir,"sha256_mode_a_normalized_to_cpp.csv"));
f2=figure("Visible","off","Color","white","Position",[100 100 1100 680]); ax=axes(f2); hold(ax,"on");
for li=1:3
    plot(ax,sizes,ratios(:,li),"-o","LineWidth",1.8,"MarkerSize",6, ...
        "Color",colors(li,:),"DisplayName",labels(li));
end
yline(ax,1,"--","C++ baseline","HandleVisibility","off");
set(ax,"YScale","log","FontSize",12,"Box","on"); grid(ax,"on");
xlabel(ax,"Input prefix (bytes)"); ylabel(ax,"Median time relative to C++ (\times, log scale)");
title(ax,"Mode A software SHA-256 normalized to C++"); legend(ax,"Location","northwest");
exportgraphics(f2,fullfile(outputDir,"figure2_sha256_normalized_to_cpp.png"),"Resolution",300);
exportgraphics(f2,fullfile(outputDir,"figure2_sha256_normalized_to_cpp.pdf"),"ContentType","vector");
savefig(f2,fullfile(outputDir,"figure2_sha256_normalized_to_cpp.fig")); close(f2);

historical=readtable(fullfile(repositoryRoot,"data","processed", ...
    "plauska_sha256_historical_summary.csv"),TextType="string",VariableNamingRule="preserve");
assert(height(historical)==24 && all(historical.n==100),"SHA256:Historical","Historical grid mismatch.");
localMean=zeros(8,3); historicalMean=zeros(8,3);
for li=1:3
    for si=1:8
        lm=summary.language==languages(li)&summary.input_bytes==sizes(si);
        hm=historical.language==languages(li)&historical.input_bytes==sizes(si);
        assert(nnz(lm)==1&&nnz(hm)==1,"SHA256:HistoricalGrid","Local/historical grid mismatch.");
        localMean(si,li)=summary.mean_us(lm); historicalMean(si,li)=historical.mean_us(hm);
    end
end
f3=figure("Visible","off","Color","white","Position",[100 100 1350 650]);
layout=tiledlayout(f3,1,2,"TileSpacing","compact","Padding","compact");
a=nexttile(layout); hold(a,"on"); b=nexttile(layout); hold(b,"on");
for li=1:3
    plot(a,sizes,historicalMean(:,li),"-o","LineWidth",1.8,"Color",colors(li,:),"DisplayName",labels(li));
    plot(b,sizes,localMean(:,li),"-o","LineWidth",1.8,"Color",colors(li,:),"DisplayName",labels(li));
end
for target=[a,b]
    set(target,"YScale","log","FontSize",11,"Box","on"); grid(target,"on");
    xlabel(target,"Input prefix (bytes)");
end
commonYLimits=[10,10^ceil(log10(max([historicalMean(:);localMean(:)])))];
ylim(a,commonYLimits); ylim(b,commonYLimits);
ylabel(a,"Mean execution time (\mus, log scale)");
title(a,"Historical Plauska: classic ESP32 Xtensa"); title(b,"This study Mode A: ESP32-C6 RISC-V");
legend(a,"Location","northwest");
title(layout,"Software SHA-256 historical context (shared scale; protocols are not equivalent)","FontWeight","bold");
exportgraphics(f3,fullfile(outputDir,"figure3_sha256_historical_context.png"),"Resolution",300);
exportgraphics(f3,fullfile(outputDir,"figure3_sha256_historical_context.pdf"),"ContentType","vector");
savefig(f3,fullfile(outputDir,"figure3_sha256_historical_context.fig")); close(f3);

environment=table(string(version),string(computer),string(inputPath),height(data), ...
    datetime("now","TimeZone","UTC","Format","yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"), ...
    'VariableNames',{'matlab_version','computer','input_path','input_rows','generated_at_utc'});
writetable(environment,fullfile(outputDir,"analysis_environment.csv"));
fprintf("SHA256_MATLAB_ANALYSIS_PASS rows=%d output=%s\n",height(data),outputDir);
end

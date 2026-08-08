function run_crc32_mode_a_analysis(repositoryRoot)
%RUN_CRC32_MODE_A_ANALYSIS Validate and plot the first ESP32-C6 Mode A run set.

arguments
    repositoryRoot (1,1) string
end

inputPath = fullfile(repositoryRoot, "data", "processed", ...
    "crc32_mode_a_esp32c6_observations.csv");
outputDir = fullfile(repositoryRoot, "artifacts", "matlab", "crc32_mode_a");
if ~isfolder(outputDir)
    mkdir(outputDir);
end

data = readtable(inputPath, TextType="string", VariableNamingRule="preserve");
required = ["run_id", "chip", "language", "benchmark", "mode", ...
    "input_bytes", "iteration", "batch_count", "total_batch_time_us", ...
    "normalized_time_per_call_us", "checksum", "expected_checksum", ...
    "correctness_pass", "measurement_status"];
assert(all(ismember(required, string(data.Properties.VariableNames))), ...
    "CRC32:Schema", "Processed CSV is missing required named columns.");
assert(height(data) == 2400, "CRC32:Rows", "Expected exactly 2400 rows.");
assert(all(data.mode == "A") && all(data.benchmark == "CRC32"), ...
    "CRC32:Mode", "Unexpected mode or benchmark.");
assert(all(data.correctness_pass == "true") && ...
    all(data.measurement_status == "valid"), ...
    "CRC32:Validity", "Only correct, valid observations may be plotted.");

languages = ["c_cpp", "rust", "micropython"];
labels = ["C++", "Rust", "MicroPython"];
sizes = [0, 16, 32, 64, 128, 256, 512, 1024];
expectedBatch = [1024,64,32,16,8,4,2,1; ...
                 512,128,64,32,16,8,4,2; ...
                 64,2,1,1,1,1,1,1];

summaryRows = table();
medianMatrix = zeros(numel(sizes), numel(languages));
q1Matrix = zeros(size(medianMatrix));
q3Matrix = zeros(size(medianMatrix));
for languageIndex = 1:numel(languages)
    for sizeIndex = 1:numel(sizes)
        mask = data.language == languages(languageIndex) & ...
            data.input_bytes == sizes(sizeIndex);
        values = data.normalized_time_per_call_us(mask);
        assert(numel(values) == 100, "CRC32:ConditionRows", ...
            "Each language/size condition must contain exactly 100 rows.");
        assert(all(data.iteration(mask) == (1:100)'), "CRC32:Iterations", ...
            "Iterations must be contiguous and ordered 1 through 100.");
        assert(all(data.batch_count(mask) == expectedBatch(languageIndex,sizeIndex)), ...
            "CRC32:Batching", "Frozen batch count mismatch.");
        reconstructed = data.total_batch_time_us(mask) ./ data.batch_count(mask);
        assert(all(abs(reconstructed - values) <= 5.1e-10), ...
            "CRC32:Normalization", "Per-call values do not reconstruct from raw batch fields.");

        med = median(values);
        q1 = prctile(values, 25);
        q3 = prctile(values, 75);
        medianMatrix(sizeIndex, languageIndex) = med;
        q1Matrix(sizeIndex, languageIndex) = q1;
        q3Matrix(sizeIndex, languageIndex) = q3;
        row = table(languages(languageIndex), sizes(sizeIndex), numel(values), ...
            mean(values), med, std(values), q1, q3, min(values), max(values), ...
            'VariableNames', {"language","input_bytes","n","mean_us", ...
            "median_us","std_us","q1_us","q3_us","min_us","max_us"});
        summaryRows = [summaryRows; row]; %#ok<AGROW>
    end
end
writetable(summaryRows, fullfile(outputDir, "crc32_mode_a_summary.csv"));

colors = [0.0000 0.4470 0.7410; 0.8500 0.3250 0.0980; 0.4940 0.1840 0.5560];
figure1 = figure("Visible", "off", "Color", "white", "Position", [100 100 1100 680]);
axes1 = axes(figure1); hold(axes1, "on");
for languageIndex = 1:numel(languages)
    lower = medianMatrix(:,languageIndex) - q1Matrix(:,languageIndex);
    upper = q3Matrix(:,languageIndex) - medianMatrix(:,languageIndex);
    errorbar(axes1, sizes, medianMatrix(:,languageIndex), lower, upper, ...
        "-o", "LineWidth", 1.8, "MarkerSize", 6, ...
        "Color", colors(languageIndex,:), "DisplayName", labels(languageIndex));
end
set(axes1, "YScale", "log", "FontSize", 12, "Box", "on");
grid(axes1, "on");
xlabel(axes1, "Input prefix (bytes)");
ylabel(axes1, "Normalized execution time per CRC call (\mus, log scale)");
title(axes1, "Mode A CRC-32 on ESP32-C6 (median and IQR, n = 100)");
legend(axes1, "Location", "northwest");
exportgraphics(figure1, fullfile(outputDir, "figure1_crc32_execution_time.png"), "Resolution", 300);
exportgraphics(figure1, fullfile(outputDir, "figure1_crc32_execution_time.pdf"), "ContentType", "vector");
savefig(figure1, fullfile(outputDir, "figure1_crc32_execution_time.fig"));
close(figure1);

ratios = medianMatrix ./ medianMatrix(:,1);
normalizedRows = table();
for languageIndex = 1:numel(languages)
    rows = table(repmat(languages(languageIndex), numel(sizes), 1), sizes', ...
        ratios(:,languageIndex), 'VariableNames', ...
        {"language","input_bytes","median_time_relative_to_cpp"});
    normalizedRows = [normalizedRows; rows]; %#ok<AGROW>
end
writetable(normalizedRows, fullfile(outputDir, "crc32_mode_a_normalized_to_cpp.csv"));

figure2 = figure("Visible", "off", "Color", "white", "Position", [100 100 1100 680]);
axes2 = axes(figure2); hold(axes2, "on");
for languageIndex = 1:numel(languages)
    plot(axes2, sizes, ratios(:,languageIndex), "-o", "LineWidth", 1.8, ...
        "MarkerSize", 6, "Color", colors(languageIndex,:), ...
        "DisplayName", labels(languageIndex));
end
yline(axes2, 1, "--", "C++ baseline", "HandleVisibility", "off");
set(axes2, "YScale", "log", "FontSize", 12, "Box", "on");
grid(axes2, "on");
xlabel(axes2, "Input prefix (bytes)");
ylabel(axes2, "Median execution time relative to C++ (\times, log scale)");
title(axes2, "Mode A CRC-32 language overhead normalized to C++");
legend(axes2, "Location", "northwest");
exportgraphics(figure2, fullfile(outputDir, "figure2_crc32_normalized_to_cpp.png"), "Resolution", 300);
exportgraphics(figure2, fullfile(outputDir, "figure2_crc32_normalized_to_cpp.pdf"), "ContentType", "vector");
savefig(figure2, fullfile(outputDir, "figure2_crc32_normalized_to_cpp.fig"));
close(figure2);

environment = table(string(version), string(computer), string(inputPath), ...
    height(data), datetime("now", "TimeZone", "UTC", "Format", "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"), ...
    'VariableNames', {"matlab_version","computer","input_path","input_rows","generated_at_utc"});
writetable(environment, fullfile(outputDir, "analysis_environment.csv"));
fprintf("CRC32_MATLAB_ANALYSIS_PASS rows=%d output=%s\n", height(data), outputDir);
end

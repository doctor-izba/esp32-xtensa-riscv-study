function run_crc32_low_level_analysis(repositoryRoot)
%RUN_CRC32_LOW_LEVEL_ANALYSIS Plot descriptive historical/local language ratios.

arguments
    repositoryRoot (1,1) string
end

inputPath = fullfile(repositoryRoot, "data", "processed", ...
    "crc32_historical_c6_comparison.csv");
outputDir = fullfile(repositoryRoot, "artifacts", "matlab", "crc32_low_level");
if ~isfolder(outputDir)
    mkdir(outputDir);
end

data = readtable(inputPath, TextType="string", VariableNamingRule="preserve");
required = ["input_bytes", "language", "historical_language_to_cpp_median_ratio", ...
    "c6_language_to_cpp_median_ratio", "comparability_note"];
assert(height(data) == 24 && all(ismember(required, string(data.Properties.VariableNames))), ...
    "CRC32LowLevel:Schema", "Expected the complete 24-row comparison table.");

sizes = [16, 32, 64, 128, 256, 512, 1024];
historicalRatio = zeros(size(sizes));
c6Ratio = zeros(size(sizes));
for index = 1:numel(sizes)
    mask = data.language == "rust" & data.input_bytes == sizes(index);
    assert(nnz(mask) == 1, "CRC32LowLevel:Grid", "Missing Rust comparison row.");
    historicalRatio(index) = data.historical_language_to_cpp_median_ratio(mask);
    c6Ratio(index) = data.c6_language_to_cpp_median_ratio(mask);
end

figure4 = figure("Visible", "off", "Color", "white", "Position", [100 100 1050 650]);
axes4 = axes(figure4); hold(axes4, "on");
plot(axes4, sizes, historicalRatio, "--o", "LineWidth", 1.8, "MarkerSize", 6, ...
    "DisplayName", "Plauska classic ESP32 (historical median ratio)");
plot(axes4, sizes, c6Ratio, "-s", "LineWidth", 1.8, "MarkerSize", 6, ...
    "DisplayName", "ESP32-C6 Mode A (local median ratio)");
yline(axes4, 1, ":", "Equal median time", "HandleVisibility", "off");
set(axes4, "XScale", "log", "FontSize", 12, "Box", "on", ...
    "XTick", sizes, "XTickLabel", string(sizes));
grid(axes4, "on");
xlabel(axes4, "Input prefix (bytes, log scale)");
ylabel(axes4, "Rust median / C++ median");
title(axes4, "CRC-32 relative language pattern across input size");
subtitle(axes4, "Separate platforms and non-equivalent protocols; descriptive only");
legend(axes4, "Location", "northeast");
exportgraphics(figure4, fullfile(outputDir, "figure4_crc32_rust_cpp_ratio.png"), "Resolution", 300);
exportgraphics(figure4, fullfile(outputDir, "figure4_crc32_rust_cpp_ratio.pdf"), "ContentType", "vector");
savefig(figure4, fullfile(outputDir, "figure4_crc32_rust_cpp_ratio.fig"));
close(figure4);

fprintf("CRC32_LOW_LEVEL_MATLAB_PASS rows=%d output=%s\n", height(data), outputDir);
end

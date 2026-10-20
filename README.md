# A Change of Core: Revisiting ESP32 Benchmarks on ESP32-C6

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23493672.svg)](https://doi.org/10.5281/zenodo.23493672)

Research by **Izbassar Yesbol** · [ORCID](https://orcid.org/0009-0002-1737-7982)
· hello@izba.sarl · Technical report, editorial revision 1.0.1.

[Report PDF](paper/review-manuscript.pdf) · [Supplement](paper/review-supplement.pdf)
· [Analysis reproduction](analysis-release/README.md) · [Public history scope](PUBLIC_HISTORY.md)

Five workloads were measured in C/C++, Rust and MicroPython on one ESP32-C6.
The 21,600 accepted observations comprise 12,000 reproduction-oriented Mode A
records and 9,600 separately identified optimization-profile records. Published
classic-ESP32 aggregates provide historical context, not a controlled ISA
comparison. The report is not externally peer reviewed.

## Reproduce the analysis

Use the self-contained `analysis-release/` directory. In that directory run:

```text
python verify_package.py
python analysis.py
```

Its README documents MATLAB R2024b figure generation and Tectonic PDF builds.
The data, software and imported historical/static metrics have separate roles.
This snapshot cannot rerun firmware, hardware or numerical correctness tests.

## History and licenses

The selected development history begins in August 2026 and retains 41 original
milestones. It excludes unresolved upstream arrays, implementations, binaries,
full machine-code listings and private captures from every retained commit.
The complete original archive is preserved privately. See `PUBLIC_HISTORY.md`.

Original analysis software is MIT; author-owned data, documentation and figures
are CC BY 4.0, with scope and third-party exclusions explained in
[LICENSING.md](analysis-release/LICENSING.md). A license here does not relicense
the cited publications or excluded third-party material.

## Publication status

Analysis archive **v1.0.1** and the accompanying report were published directly
in [Zenodo on 20 October 2026](https://zenodo.org/records/23493672).
Version DOI: [10.5281/zenodo.23493672](https://doi.org/10.5281/zenodo.23493672).
The [all-versions DOI](https://doi.org/10.5281/zenodo.23493671) points to the
latest archive version. See [publication receipt](publication/ZENODO_DEPOSIT_V1_0_1.json)
for uploaded hashes and public download verification.

This existing GitHub repository remains private while old excluded objects
retained by GitHub are addressed. GitHub–Zenodo auto-archiving is not enabled;
the DOI identifies the scoped Zenodo deposit, not this repository's full history.
The earlier sealed v1.0.0 ZIP remains a private snapshot.

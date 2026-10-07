# Licensing scope

Effective: 2026-10-07. Copyright holder for original project contributions:
Izbassar Yesbol, https://orcid.org/0009-0002-1737-7982.

## Original contributions

- Original software contributions by the repository author are licensed under
  the MIT License in `LICENSE`. This includes original acquisition,
  processing, validation, plotting, and build tooling, subject to the
  third-party exceptions below.
- Original measurement records, authored research documentation, manuscript,
  supplement, and original figures are licensed under Creative Commons
  Attribution 4.0 International (CC BY 4.0):
  https://creativecommons.org/licenses/by/4.0/ . The binding legal terms are
  https://creativecommons.org/licenses/by/4.0/legalcode.en . Attribution should
  identify Izbassar Yesbol, this study, the repository/version, and any changes.
  This grant covers the author's rights only, including database rights where
  applicable; it does not create copyright over otherwise unprotected facts.

CC BY 4.0 is a license choice, not a claim of peer review, journal acceptance,
or a DOI. Future publisher terms must be checked before submission. Preserve
this statement and the scientific provenance when preparing a release.

## Third-party exceptions

The original-contribution licenses do not replace the terms of any upstream
code, publication, dataset, library, generated numerical array, or embedded
firmware dependency. `THIRD_PARTY_NOTICES.md` maps identified origins and
notices. Where a file mixes original and third-party material, no blanket MIT
or CC BY grant is made for the whole file.

Specifically:

- ESP-DSP-derived FFT/FIR/IIR code portions, translations, and reconstructions
  retain their Apache-2.0 obligations and Espressif notice. The recovered
  Plauska C++ FIR/IIR files contain file-level Apache-2.0 declarations.
- Go-derived CRC code portions and reconstructions retain the Go Authors'
  BSD-3-Clause terms and notices.
- Brad Conte's SHA source has an upstream public-domain dedication; this is
  not relabelled as CC0. Separately authored SHA code remains covered only to
  the extent of the repository author's rights.
- Plauska's shared DATA, FFT table/reference output, coefficient literals,
  other unlicensed additions/ports, and their copies in generated source or
  native artifacts are excluded from the original-contribution grants while
  their redistribution status is unresolved. Independently calculated
  FIR/IIR oracle outputs are distinguished from copied upstream arrays.
- Native ELF, object, binary, firmware, and machine-code/disassembly artifacts
  contain or derive from multiple components. Their distribution requires
  the relevant component licenses/notices and permission for embedded
  third-party material; they are not wholly MIT-licensed artifacts.
- External literature and historical source materials retain their own
  terms. Citations, locators, hashes, and reported numerical facts do not
  license the source documents.

The public-release gate remains open until the recorded unresolved items in
`references/original-study/REDISTRIBUTION_REVIEW.md` are cleared. A permission
request or a license on our original work does not clear those items.

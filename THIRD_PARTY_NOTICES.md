# Third-party notices and unresolved material

Review date: 2026-10-07. These notices accompany the identified source,
translations, reconstructions, and native artifacts. They do not grant rights
to material for which permission is unresolved. This inventory is not a
completed dependency-license audit.

## ESP-DSP / Espressif FFT, FIR, and IIR

Copyright 2018-2019 Espressif Systems (Shanghai) PTE LTD

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License. You may obtain a copy
of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.

The full license is retained in `LICENSES/Apache-2.0.txt`, obtained from
https://raw.githubusercontent.com/espressif/esp-dsp/v1.0/LICENSE .
The retained text SHA-256 is
`cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.

Source lineage:

- FFT: https://github.com/espressif/esp-dsp/blob/v1.0/modules/fft/fixed/dsps_fft2r_sc16_ansi.c
- FIR: https://github.com/espressif/esp-dsp/blob/v1.0/modules/fir/float/dsps_fir_f32_ansi.c
- IIR: https://github.com/espressif/esp-dsp/blob/v1.0/modules/iir/biquad/dsps_biquad_f32_ansi.c
- Plauska snapshot: https://github.com/ignasp/ProgLangComp_onESP32/tree/c42dba0d41d547960b73e63b3d4e09917d61e171

The corresponding project kernels and adaptations are under
`benchmarks/historical/{fft,fir,iir}/c/main/*_software.cpp` and headers,
`micropython/*_impl.py`, kernel portions of `rust/src/main.rs`, and reference
equations in `tools/prepare_vectors.py`. Matched source/object/disassembly
artifacts under `artifacts/static/{fft,fir,iir}/` and native builds under
`artifacts/builds/` follow this lineage. Mode B reuses these kernels, including
the Rust FFT unchecked transformation.

Project changes include C++ wrapping, Rust/MicroPython translations, explicit
numeric-operation/state handling, correctness and acquisition integration,
and declared Mode B transformations. Their exact histories, flags, and
measurement-build identities remain in Git and build manifests. The original
sources are not presented as authored entirely by this project's researcher.
Unresolved Plauska-specific additions are not inferred to be licensed merely
from an upstream origin link.

## Go CRC-32

Copyright 2011 The Go Authors. All rights reserved.

Source: https://github.com/golang/go/blob/go1.19.3/src/hash/crc32/crc32_generic.go

The distribution terms and disclaimer are reproduced verbatim in
`LICENSES/BSD-3-Clause-Go.txt`, from
https://raw.githubusercontent.com/golang/go/go1.19.3/LICENSE . That license
contains the notice `Copyright (c) 2009 The Go Authors. All rights reserved.`
The retained text SHA-256 is
`2d36597f7117c38b006835ae7f537487207d8ec407aa9d9980794b2030cbc067`.

The CRC table-generation/update lineage applies conservatively to kernel
portions in `benchmarks/historical/crc32/`,
`benchmarks/historical/crc32/static_analysis/matched_crc32.cpp`,
the matched source copies under `artifacts/assembly/crc32/`, and their derived
native artifacts. Project changes include ports, harness integration, and
matched-build reconstruction. This notice does not resolve rights in the
separately recovered Plauska input DATA.

## Brad Conte SHA-256

Source: https://github.com/B-Con/crypto-algorithms

The upstream README dedicates its code to the public domain and requests
acknowledgement. Brad Conte's SHA-256 implementation is acknowledged as a
source in the recovered benchmark lineage. The audit records the current
project SHA implementation as independently authored equivalent code.
Relevant source is under `benchmarks/historical/sha256/`; matched sources are
under `artifacts/assembly/sha256/`. No CC0 declaration is invented for the
upstream dedication. Plauska-specific code additions, if copied, and its
shared input data remain separate rights questions.

## Plauska study and numerical data

Ignas Plauska, Audrius Liutkevičius, and Agnė Janavičiūtė,
"Performance Evaluation of C/C++, MicroPython, Rust and TinyGo Programming
Languages on ESP32 Microcontroller," Electronics 12(1), 143 (2023).
https://doi.org/10.3390/electronics12010143

Their article and source repository are the historical comparison source.
The repository snapshot is pinned above. Recovered arrays and author-specific
adaptations lacking a verified license are not covered by our original-work
licenses. A permission request is recorded separately; no reply or grant is
assumed. This includes copies embedded in ELF/firmware, not only generated
source files.

## Firmware dependencies and remaining audit

ESP-IDF, compiler runtimes, Rust crates, and other linked components retain
their individual terms. Dependency locks and build manifests identify the
versions; those records are not by themselves a complete set of distribution
notices. A complete component/notice inventory is required before public
binary archival. Exact measured native artifacts remain byte-identical;
these sidecar notices do not constitute a new build or measurement.

# Decision 0016 — scoped analysis archive, prepared but not published

Date: 2026-10-07. Version: `1.0.0-analysis-archive`.

The owner approved availability corrections, additional original analysis
materials, actual reproduction checks, PDF/archive rebuilding, and platform
selection. In the subsequent explicit clarification the owner chose:
**prepare and approve the package; do not publish yet**.

## Scope

Prepare an allowlisted, analysis-only ZIP for subsequent Zenodo deposit.
Use the existing MATLAB publication script, original manuscript sources,
project-derived cited historical aggregates, and numerical static metrics.
Export accepted local timing records by named-column projection; exclude
input/reference arrays, benchmark kernels/ports, firmware, native artifacts,
disassembly, complete console logs, third-party full texts/source recordings,
and Git history. No whole-repository visibility change is authorized.

The package must reproduce the 216 timing groups and ratios, all four
publication figures, and the four generated result tables. Static metrics
and historical aggregates are imported evidence, not independently reproduced
from unavailable binaries or external recordings. Clearly identify that limit
in the manuscript, supplement, and package instructions.

## Impact

This is a downstream distribution projection, not a new experiment, timing
policy, numeric contract, scientific argument, or replacement of evidence.
All raw files, frozen source vectors, accepted processed datasets, and exact
native artifacts remain unchanged. Source hashes and package hashes identify
the projection. The private full evidence archive is retained, with the
existing Rust CRC preservation exception unchanged.

Visual inspection also identified edge markers touching the plotting frame.
Figures 1–3 receive horizontal axis padding only; values, vertical limits,
scales, grouping, and interpretations remain unchanged. MATLAB and downstream
publication figures/PDFs are regenerated; frozen experiment artifacts are not.

## Platform and license policy

Zenodo is selected for the eventual scholarly archive, not journal acceptance
or peer review. Its checked policies accept research artifacts, require
appropriate distribution rights, allow mixed MIT/CC BY licensing, and require
creator/resource metadata. Prepare a dataset record with the original report
and analysis as associated files; do not fabricate an affiliation, funding,
publication date, record URL, or DOI. Add the actual archive locator to the
availability statement only after a separately authorized deposit.

Primary requirements checked on 2026-10-07:

- https://about.zenodo.org/policies/
- https://help.zenodo.org/docs/deposit/describe-records/licenses/
- https://help.zenodo.org/docs/deposit/describe-records/resource-type/
- https://help.zenodo.org/docs/deposit/describe-records/creators/
- https://help.zenodo.org/docs/deposit/create-new-upload/

## Gate

Approval applies only to the inspected ZIP whose hashes are recorded in
`publication/APPROVED_PACKAGE.json`, once the documented checks pass. It does
not clear the full repository's unresolved redistribution rights. Public
upload, public GitHub creation, DOI reservation, and visibility changes remain
withheld by the owner's clarification. No journal submission is authorized.

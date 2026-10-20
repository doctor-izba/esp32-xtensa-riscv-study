# Archival platform review — 2026-10-07

Update 2026-10-20: the owner authorized direct public deposit of the scoped
v1.0.1 archive in Zenodo while keeping the GitHub repository private. The
authenticated production draft issued DOI `10.5281/zenodo.23493672` before
the final build. Reservation is distinct from registration, which occurs upon
publication. This file is a build-time review snapshot; consult the live record
for current publication status. The DOI is for the analysis archive and
accompanying technical report, not a journal article or peer-review decision.

## Historical preparation review (v1.0.0, 2026-10-07)

The following statements describe the earlier preparation approval, preserved
unchanged in its sealed v1.0.0 ZIP; they do not describe v1.0.1 deposit status.

Selected: **Zenodo**, for a dataset archive accompanied by the technical report
and original analysis software. This is not a journal submission or external
peer review. The owner approved preparation only; no upload, account action,
DOI reservation, public repository, or visibility change was performed.

Official requirements checked:

| Requirement | Package decision | Official source |
| --- | --- | --- |
| Research artifacts and distribution rights | Allowlisted analysis-only archive; exclude unresolved upstream arrays/code/binaries. Approval is scoped, not a legal clearance of the whole repository. | https://about.zenodo.org/policies/ |
| Mixed licenses | MIT for original analysis software; CC BY 4.0 for author-owned data/documentation/manuscript. No relicensing of external source documents. | https://help.zenodo.org/docs/deposit/describe-records/licenses/ |
| Resource type | Dataset: accepted timing records are primary; analysis/report are accompanying files. | https://help.zenodo.org/docs/deposit/describe-records/resource-type/ |
| Creator metadata | Izbassar Yesbol; ORCID https://orcid.org/0009-0002-1737-7982. No invented affiliation or funding. | https://help.zenodo.org/docs/deposit/describe-records/creators/ |
| Upload limits and DOI | One ZIP, below 50 GB/100-file limit. A future archive gets its own record, not an invented journal DOI. No DOI reserved now. | https://help.zenodo.org/docs/deposit/create-new-upload/ |

`ZENODO_METADATA.json` is a worksheet, not a deposited API record. Publication
date, DOI, and record URL remain null. Before a separately authorized deposit,
set the actual date, obtain the real locator through the platform workflow,
update availability/supplement, rebuild and verify that deposit version.
Do not label the technical report as peer reviewed. A journal/preprint route
can be selected separately without holding up this bounded archive.

Readiness approval is limited to the exact locally sealed ZIP recorded in
`APPROVED_PACKAGE.json`. The full repository remains private. No reply from
Plauska is required for this scoped preparation; an unanswered issue does not
grant permission to redistribute excluded materials.

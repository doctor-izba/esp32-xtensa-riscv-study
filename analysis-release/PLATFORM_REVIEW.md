# Archival platform review — 2026-10-07

Update 2026-10-20: the owner requested obtaining a real Zenodo DOI for the
scoped v1.0.1 archive. The preparation-only status described below is the
historical v1.0.0 approval, preserved unchanged in its sealed ZIP. Authentication
and creation of the production Zenodo draft are pending. No DOI or public
record is claimed until verified from the platform. See Decision 0018.

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

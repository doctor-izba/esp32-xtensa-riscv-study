# Decision 0015 — original-work licenses and upstream permissions

Date: 2026-10-07.

Status: original-work license selection approved by the owner in the current
publication-preparation request; upstream permission and public binary
redistribution remain pending.

## Decision

Use MIT for the repository author's original software contributions and
CC BY 4.0 for original measurements, documentation, manuscript, supplement,
and figures, with the explicit third-party scope exclusions in `LICENSING.md`.
The researcher is Izbassar Yesbol; the owner supplied ORCID
`0009-0002-1737-7982`, whose public person record confirms that name.

Restore identified Espressif Apache-2.0 and Go BSD-3-Clause attribution using
sidecar notices and verbatim license texts. No measured kernel, vector, raw
observation, historical summary, or exact native artifact is edited or
rebuilt for this rights correction. Its scientific protocol is unchanged.

Request explicit upstream permission for unlicensed Plauska numerical data
and adaptations, including their embedding in source and binary artifacts.
The owner asked to proceed with the recommended author-contact route.
The request is a publication-preparation action, not a permission grant.

## Impact and release gate

No new experiment, revised result, or changed numeric contract follows from
this decision. Measurement/build-source hashes continue to identify the
frozen experiment and its original source state. The notice inventory
acknowledges those sources rather than replacing their hash records.

Public visibility, DOI deposit, and public binary/source archival remain
pending until the rights inventory is resolved or a separately approved
distribution package excludes the unresolved material and its Git history.
No history rewrite, force push, public release, or DOI is authorized by this
license selection alone.

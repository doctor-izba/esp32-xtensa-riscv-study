# Decision 0018 — obtain a Zenodo DOI for the scoped release

Date: 2026-10-20. Release being prepared: analysis archive v1.0.1.

The owner explicitly requested obtaining a real DOI after selecting the new
title and reviewing the report. This supersedes the earlier prohibition on
starting the DOI workflow for this scoped package. It does not authorize
opening the full private repository or including excluded upstream evidence.

Use the production Zenodo account, create a draft and reserve a platform-issued
DOI, then add that exact DOI/record identifier to the report and metadata before
rebuilding the final archive. A reserved DOI is not a publicly registered or
resolving DOI until the record is published. Do not claim public availability
from reservation alone. Record platform state honestly throughout the workflow.

Preserve v1.0.0 and its exact approval record. Prepare v1.0.1 separately with
the current editorial revision, the same timing records, generated tables,
figure-generation code and evidence exclusions. Keep export schema 1.0.0:
the schema and scientific analysis do not change when the archive version changes.

Version-specific reproduction logs and preflight must exercise the final
DOI-bearing files. Do not copy old passing results under new input hashes.
The existing builder gains explicit preflight/validation paths and staging-only
mode; the reproduction script gains an explicit expected page count and output
directory so that v1.0.0 validation records are not overwritten.

Authentication, new-account registration and any platform-required acceptance
of legal terms are completed by the owner when necessary. No credentials or
tokens are recorded in the package or repository.

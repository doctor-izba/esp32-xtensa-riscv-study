# Decision 0019 — prepare allowed history for the existing GitHub repository

Date: 2026-10-20. Status: approved remote rewrite completed; public visibility held pending server-side object cleanup.

The owner explicitly requested preserving the permitted development history
from August in the existing `doctor-izba/esp32-xtensa-riscv-study` repository,
without creating a new GitHub repository. Preparation uses an isolated local
copy. The original local checkout and private backup remain intact. The owner
subsequently approved replacing both remote branches with the prepared history.

## Prepared candidate

- 41 historical commits beginning 8 August 2026 are retained. Author and
  committer identities, their timestamps and messages were checked against
  every original-to-filtered mapping.
- Empty commits are preserved as historical milestones after excluded content
  is removed. Hashes necessarily change; old private evidence anchors retain
  their original meaning rather than being relabeled as public commit IDs.
- The selected historical paths comprise original methodology, protocols,
  decisions, analysis software, aggregate tables, authored figures and text.
  Benchmark kernels, arrays, native artifacts, full listings, captures and
  internal review documents are excluded throughout the filtered history.
- Two new commits add the current scoped analysis snapshot and preserve its
  exact bytes across Git line-ending settings. The candidate has 43 commits.
- The current snapshot is in `analysis-release/`, alongside the retained
  historical paths. Its independent manifest and analysis pass after a fresh
  `git archive` extraction: 21,600 records, 216 groups, 176 ratios, four tables.
- Its README and PUBLIC_HISTORY.md disclose the projection and current local,
  unpublished, no-DOI state. This is not claimed to be a final Zenodo release.

Candidate checkout: `paper/build/public-history-review/`.
Private backup: `.git/publication-backups/20261020T074835Z/`.
The backup contains a verified all-refs Git bundle, binary working-tree patch,
untracked-file ZIP, original refs, historical blob inventory and commit mapping.
It is inside `.git` and is never part of the candidate's public files.

## Remote boundary

The GitHub repository remains private. No PRs, releases or forks were found.
After explicit owner approval, an atomic push with separate expected old
branch SHAs (`--force-with-lease`) replaced both remote branch histories.
`git ls-remote` confirmed:

- `main`: `9635a25b7f7787ea2e966f0a08db49f8d4c2f155`;
- `codex/paper-v4-1-polish`: `749af71ca4cc8a361f2ef12df793d02900d6af65`.

No backup refs were pushed. The main history retains 41 historical commits
and two publication preparation commits.

An authenticated GitHub API check still resolved the old main commit
`a101c7b73a87c328463174cbfbb1284703531985`. A second check resolved
`artifacts/assembly/crc32/cpp/riscv/matched/complete_disassembly.txt` at
that old commit (blob `43a02163997a0b4f865b4576121e391af1c06a40`, 910 bytes).
Only metadata was requested. These checks establish that excluded objects
remain accessible to an authorized account; anonymous access was not tested
because the repository remains private. Public visibility and automatic
Zenodo archiving have therefore not been enabled. No DOI had been issued
at the time of this GitHub check.

GitHub documents that old cached SHA views can survive a history rewrite.
Do not claim full server-side purging based only on local `git-filter-repo`
or force-push success. Check the remote state before public visibility or
Zenodo auto-archiving is enabled; unresolved cached objects may require a
platform-side decision or assistance. GitHub's documentation states that
Support does not generally remove non-sensitive data; these excluded materials
must not be misrepresented as leaked credentials. A local support draft is
prepared separately; no support message has been sent.

This record concerns distribution, not a method, vector, schema or analysis
change. The full private experimental evidence and sealed v1.0.0 ZIP remain
unchanged. Obtaining the Zenodo DOI remains the downstream publication task.

## Subsequent direct deposit

The owner selected direct upload while retaining the private repository.
Zenodo published the scoped v1.0.1 archive and two companion PDFs on
2026-10-20 at https://doi.org/10.5281/zenodo.23493672 . Anonymous downloads
of all three files matched local SHA-256 hashes, and the DOI resolved to the
published record. The private repository README now links this deposit;
GitHub visibility and automatic release preservation remain unchanged.

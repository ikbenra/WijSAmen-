# WijSAmen Evolution Vault v0 — proposed recovery system

**Status: code committed on experimental branch, NOT an operational off-site backup.**

## Threat model
- GitHub branch protection/rulesets prevent routine accidental deletion/force-push, but admins and account compromise can still defeat them.
- A second repository in the same account is not independent of account compromise.
- GitHub Actions artifacts expire; they are an interim restore checkpoint, not immutable archival storage.
- An independent Drive/object-storage copy should be write-once or protected by a separate identity. Ordinary Drive files are not immutable by default.
- Git version history is not a database/credential/external-action backup. Do not put secrets or private information in public archives.

## Deployment gates (not yet completed)
1. Repository administrator configures ruleset for `main` and protected archive tags: prevent deletion and force-push, require PR review/status checks; minimize bypass permissions. Verify with GitHub settings readback.
2. Run `bash ops/evolution-vault/backup.sh https://github.com/ikbenra/WijSAmen-.git /path/to/offsite-vault` from a trusted machine or runner with sufficient storage. Keep output outside the repo.
3. Upload both `.bundle` and `.sha256` to an independently permissioned storage location, e.g. Google Drive, using separate least-privilege credentials. Never commit credentials.
4. Verify uploaded size/checksum and restore from the uploaded bytes in an isolated directory. Preserve several generations; prevent the development agent from deleting backups.
5. Enable the proposed Actions workflow only after review/merge; verify actual run artifacts. Schedule and artifacts do NOT by themselves implement independent Drive storage.
6. Include git-lfs, PR refs and other relevant repositories in an extended backup design if present. Review GitHub retention limits and restore drill cadence.

## Recovery (isolated, no remote mutation)
```bash
sha256sum -c wijsamen-YYYYMMDDTHHMMSSZ.bundle.sha256
git bundle verify wijsamen-YYYYMMDDTHHMMSSZ.bundle
git clone --mirror wijsamen-YYYYMMDDTHHMMSSZ.bundle restored.git
git -C restored.git fsck --full --no-reflogs
```

Do not push restored refs over production without explicit approval and a reviewed restore plan.

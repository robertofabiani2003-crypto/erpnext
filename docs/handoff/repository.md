# Repository handoff
Status: READY
Version selection confirmed: 2026-11-11 (Europe/Moscow).
Fork: https://github.com/robertofabiani2003-crypto/erpnext
GitHub API verified fork=true, parent=frappe/erpnext, source=frappe/erpnext.
Checkout: C:\Users\rober\OneDrive\Документы\ChatGPT\ERPNext
Task branch: codex/erpnext-setup; HEAD 495380b59c8701629f25089bd3807e6ddf7f26c6.
ERPNext: v16.54.0, commit 495380b59c8701629f25089bd3807e6ddf7f26c6; fork version-16 and tag match upstream release.
Frappe: v16.56.0, commit 49789a1711d4dde2be9c6888efe35651465f4b64.
ERPNext pyproject requires Frappe >=16.55.0,<17.0.0; Frappe selected tag satisfies this.
Frappe pyproject requires Python >=3.14,<3.15.
Runtime requirements: Python 3.14, Node.js 24, MariaDB 11.8, Redis/Valkey 6+, Yarn 1.22+, pip 25.3+; Chromium for PDF. Linux Debian/Ubuntu recommended; deployment uses isolated Docker, not native Windows.
Verification: full working tree checked out (5641 tracked files), clean git status before documentation changes; git fsck --full passed. HEAD equals origin/version-16 and upstream tag v16.54.0 (verified GitHub API and ls-remote). No blocker for application build. Limitation: local Git history is shallow (depth 1); all release files are present. Full Git history is on GitHub; fetch --unshallow later if history is needed.
No server changes in this workstream. No pushes, merges, PRs or credential files.

Official sources:
- https://frappe.io/support-versions (version-16 supported, EOL end of 2029 planned)
- https://github.com/frappe/erpnext/releases/tag/v16.54.0
- https://github.com/frappe/frappe/releases/tag/v16.56.0
- https://github.com/frappe/erpnext/blob/v16.54.0/pyproject.toml
- https://github.com/frappe/frappe/blob/v16.56.0/pyproject.toml
- https://docs.frappe.io/framework/user/en/installation
- https://github.com/frappe/frappe_docker

Local documentation: SETUP.ru.md (uncommitted; only working-tree addition).
Verification complete: git fsck --full; whitespace check of new document; release identity, branch and dependency assertions; secret-pattern scan of new documentation and this handoff.
No application tests: no application code changed and no local Bench runtime installed.
Two temporary pack files from interrupted fetch remain under .git/objects/pack (about 18 MiB total); cleanup was rejected by automatic policy review. They are outside the working tree; fsck passes. No user action is needed for deployment.

# Security Policy

This is an MVP that processes **synthetic** candidate data in public environments. Real candidate data is processed only on HR Guru-controlled hardware (see ADR-0004 and ADR-0005).

## Reporting a vulnerability
Please use GitHub's private vulnerability reporting (Security → Report a vulnerability). Do not open a public issue.

## Controls in this repository
CodeQL, Semgrep, gitleaks, npm audit, pip-audit and Trivy run in CI (see `.github/workflows/security.yml`). Container images are scanned and an SBOM is published on every build (`cd.yml`).

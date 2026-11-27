# Test and Security Strategy

## 1. Test pyramid

| Level | Scope | Tools | Runs | Gate |
|---|---|---|---|---|
| Static | Lint, types, formatting | ESLint, TypeScript, Ruff, mypy (from Sprint 1) | Every PR | Blocking |
| Unit | Pure logic: router policy, RRF fusion, validators, RBAC | Vitest (TS), pytest (Python) | Every PR | Blocking, coverage ≥ 70% on business logic |
| Integration | API + Mongo, agents + MCP, graph with mocked LLM | Supertest, pytest + atlas-local container | Every PR | Blocking |
| Contract | API ↔ agent service, MCP tool schemas | JSON Schema tests from `packages/contracts` | Every PR | Blocking (from Sprint 3) |
| AI evaluation | Golden JDs, retrieval recall/nDCG, evidence accuracy, hallucination, injection corpus, fairness name-swap | pytest-based eval runner, DeepEval/Ragas metrics, local model | PRs touching `services/agents/**` or `evals/**` | Blocking on regression threshold (from Sprint 5) |
| End-to-end | UC-001: login → requirement → run → replan → shortlist or escalation → approve | Playwright | Nightly + before release | Blocking for release |
| Performance and resilience | API and search load, run latency, resume after kill, provider outage | k6, scripted drills (TS-E6-07) | Sprint 6, then before each release | p95 targets in NFR-5 |

**LLM tests in CI never call paid or rate-limited APIs.**
- Unit and integration tests use a deterministic fake model.
- Evaluations run with a local model in a self-hosted runner, or with recorded responses (cassettes) on GitHub-hosted runners.

## 2. Failure scenarios (each must have a test)

- Model returns invalid JSON → repair loop → `needs_human` after 2 attempts.
- Free provider returns 429 → fallback provider → local model → `paused_rate_limited`.
- MCP server down → run paused with a clear error.
- Agent process killed mid-run → resume from checkpoint, no duplicate side effects.
- Injection instruction in resume → no behaviour change.
- Tool called outside its scope → denied and audited.
- Loop never converges → `stopped_limit` at 12 iterations.

## 3. Security scanning in CI/CD

| Control | Tool | Trigger | Fails on |
|---|---|---|---|
| SAST | CodeQL (JS/TS, Python) | PR, push to main, weekly | Any alert ≥ high (triaged in the Security tab) |
| SAST (rules) | Semgrep CE (`p/default`, `p/owasp-top-ten`, `p/secrets`) | PR | Error-level findings |
| Secrets | gitleaks + GitHub secret scanning and push protection | PR, push | Any finding |
| SCA | `npm audit --audit-level=high`, `pip-audit`, Dependabot alerts | PR, weekly | High or critical |
| IaC / filesystem | Trivy `fs` (misconfig + vuln) | PR | High or critical |
| Containers | Trivy `image` | CD, before push to GHCR | Critical (High reported) |
| SBOM | Trivy CycloneDX SBOM attached to each image build | CD | — |
| DAST | OWASP ZAP baseline against the demo env | Sprint 5 onwards, weekly | High |

## 4. Responsible-AI checks
- Fairness: counterfactual name and gender-coded word swaps must not change scores by more than 5 points.
- Explainability: 100% of `met` verdicts carry an evidence quote that verifies against the source.
- Human oversight: tests assert there is no code path where a side-effecting tool (`shortlist.finalise`, `memory.save_feedback`) executes without an approval record.
- Constraint protection: UC-001 tests assert mandatory constraints are identical before and after every replan.
- Traceability: a completeness test asserts that every graph step of an evaluation run has a matching audit event (KPI-6).

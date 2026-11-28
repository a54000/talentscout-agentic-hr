# Baseline Measurement Plan (TS-E0-08)

**Purpose:** measure today's effort and quality **before** TalentScout, so the pilot is compared with real numbers, not guesses. Since the 2026-11-28 scope change, the baseline covers the first use cases: submission audit (UC-002), candidate verification (UC-003) and sourcing and pool reuse (UC-004).

## What we measure

| # | Metric | KPI | How | Who | Sample |
|---|---|---|---|---|---|
| 1 | Submission quality today: share of submissions with a wrong detail, a missed must-have or a duplicate | KPI-8 (audit precision) | Manual audit of random submissions with the [audit sheet](baseline/submission_audit_sheet.csv) | Delivery Lead | **30 submissions**, from 5+ recruiters, from the last 2 weeks of live data |
| 2 | Minutes a lead spends checking one submission | KPI-1, KPI-7 | Same sheet, `minutes_spent` | Delivery Lead | same 30 |
| 3 | False or wrong submissions: candidate not contacted, wrong role, wrong details | KPI-10 | Call or message candidates with the [verification sheet](baseline/verification_call_sheet.csv) | Delivery Lead | **15 candidates**, from the audited 30 |
| 4 | Verification response rate | KPI-9 | Same sheet: share that answered | Delivery Lead | same 15 |
| 5 | Sourcing minutes per requirement and profiles opened per submission | KPI-1, KPI-11 | Recruiter [time log](baseline/sourcing_time_log.csv) | 3 recruiters | 5 requirements each |
| 6 | ATS volumes and data quality: submissions per recruiter per week, duplicate, missing-info and no-CV rates, share progressing past submission, days to first submission | KPI-7, context | [`apps/ats/scripts/baseline_ats_metrics.py`](../../apps/ats/scripts/baseline_ats_metrics.py) (read-only, aggregates only) | PO | 90 days of ATS data |

## How to run it

1. **ATS numbers (5 minutes).** On the Mac:

```bash
docker compose exec ats python scripts/baseline_ats_metrics.py --days 90
```

   Paste the output into `baseline-results.md`. The restored data ends on 2026-05-26, so by default the window ends there. Once there are 4+ weeks of new submissions, run it again with `--end` set to today.

2. **Audit (about 3 hours).** Pick 30 random recent submissions (for example every 10th row of the recent candidates list). For each one, open the CV next to the recruiter's entry and fill one row of the audit sheet. Use the ATS candidate ID only, never names.
3. **Verification (about 1.5 hours).** For 15 of those, contact the candidate. Tell them it's HR Guru confirming their application, and that they may decline. Ask the 3 UC-003 questions (contacted for this role? interested? details correct?) and fill the verification sheet.
4. **Sourcing log (2 weeks, passive).** 3 recruiters log 5 requirements each in the time log: start and end time, profiles opened, profiles submitted.
5. Save filled sheets as `*.filled.csv`. They're git-ignored and stay on the Mac. Publish only the totals in `baseline-results.md`.

## Privacy
- The sheets hold ATS IDs and recruiter codes (R1, R2…), not names, phones or emails. The mapping stays with the PO.
- Verification contacts only candidates who already applied, with the purpose stated and the option to decline, in line with the UC-003 rules and DPDP.

## Limitations to state in the pilot report
- Small samples (30 audits, 15 verifications, 15 sourcing logs), no randomisation of recruiters.
- Self-reported timings, and one lead's judgement in the audit.
- Candidate data after 2026-05-26 is missing; the novelty effect during the pilot.

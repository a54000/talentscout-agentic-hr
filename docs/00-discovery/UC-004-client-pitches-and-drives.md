# UC-004: Client Pitches and Hiring Drives from the ATS Pool

**Priority 3** (PO decision, 2026-11-28). Builds on the retrieval work from [UC-001](UC-001-intelligent-candidate-sourcing.md).

> **In plain words:** over time the ATS fills up with thousands of candidates already screened and checked for earlier roles. Sales and delivery want to use that pool: "show this client 10 strong Java leads we can deliver", or "plan a hiring drive for 50 freshers in Pune". TalentScout searches the pool, favours candidates whose submissions passed the audit (UC-002) and verification (UC-003), and builds an **anonymised** pitch pack. Names and contact details are shared only after the client shortlists someone and the candidate agrees.

## 1. Actors

| Actor | Role |
|---|---|
| Delivery Lead / Business development | Defines the pitch or drive, reviews and sends the pack |
| Pitch agent | Plans searches, ranks, anonymises, writes the pack |
| Sourcing agent | Hybrid search over the pool, funnel counts, replanning (the UC-001 behaviour) |

## 2. Main flow

1. The lead enters a pitch brief: client or industry, role families and skills, experience bands, locations, count, and any budget band.
2. The Sourcing agent searches the pool with hybrid search and filters, and shows the funnel. If the count is short, it replans (alternative titles, adjacent skills, serving notice) without relaxing the brief's hard limits, then escalates (BR-2, BR-8).
3. Ranking prefers candidates with a recent `confirmed` verification and a clean audit, then by recency of interest.
4. The Pitch agent writes an anonymised profile for each candidate: role, years, key skills with evidence, notice band, CTC band, location. **No name, phone, email, current employer or photo.**
5. For drives it adds a pool summary: counts by skill, experience band and location, and availability by notice period.
6. The lead reviews, edits and exports (PDF or XLSX). Exporting is an approved action and is logged.
7. When the client shortlists a profile, the candidate's interest is re-confirmed (through UC-003 messaging, approved by the lead) before identity is shared.

## 3. Acceptance criteria

- Given a brief for 10 profiles, then the pack contains ≤ 10 anonymised profiles, each with skill evidence and no direct identifiers. A test scans the export for names, emails and phone numbers.
- Given a brief that the pool can't fill, then the run escalates with the funnel and options instead of padding with weak matches.
- Given a candidate who opted out or asked for erasure, then they never appear in a pack.

## 4. Rules

BR-2, BR-3, BR-7, BR-8, BR-10. Pitch packs are anonymised by default (BR-12), and identity is shared only after the candidate re-confirms.

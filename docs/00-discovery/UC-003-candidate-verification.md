# UC-003: Candidate Verification (false-submission check)

**Priority 2** (PO decision, 2026-11-28). Channels: **WhatsApp and email** (PO decision, 2026-11-28).

> **In plain words:** a recruiter might upload a candidate who was never actually contacted, or contacted for a different role, or with wrong details, to make their numbers look better. TalentScout asks the candidate directly by WhatsApp and email: "Were you contacted by HR Guru about *this* role at *this* company? Are you interested? Are these details right?" It then compares the answers with what the recruiter entered. No reply is also a signal. A lead approves the messages before they go out and reviews the results. The agent never accuses or penalises anyone by itself.

## 1. Actors

| Actor | Role |
|---|---|
| Delivery Lead / Quality reviewer | Chooses what to verify, approves outgoing messages, reviews results |
| Candidate | Receives the message; replies, ignores it or opts out |
| Recruiter | Is informed of the outcome on their submission and can respond |
| Verification agent | Drafts messages, sends approved ones, reads replies, compares, follows up, escalates |

## 2. What gets verified

- **Sampling, not everything** (default): all submissions flagged by the UC-002 audit, plus a random 20% of the rest per recruiter per week. Configurable by the lead.
- **Never** a candidate who opted out, or one whose ATS status shows they were already placed or rejected more than 90 days ago.

## 3. The questions (template, versioned)

Short, neutral, and in the candidate's language where known (English default). Example:

> Hi {first_name}, this is HR Guru. Our recruiter {recruiter_first_name} shared your profile for the **{role}** role with **{client_or_industry}**, location {location}. Could you confirm:
> 1. Were you contacted about this role? (Yes / No / Different role)
> 2. Are you interested? (Yes / No / Maybe)
> 3. Current CTC {ctc}, expected {ectc}, notice {notice}: correct? (Yes / or reply with the right values)
> Reply STOP to opt out.

Client names are shown only if the client allows it. Otherwise the industry is used ("a leading investment bank").

## 4. Main flow

1. The lead picks a batch (or accepts the weekly sample).
2. The Verification agent drafts one message per candidate from the approved template. **Drafts are never sent automatically.**
3. The lead approves the batch (re-authentication, BR-5). Each message gets an approval record.
4. Messages are sent through the **ATS's existing channels**: the WhatsApp relay and the ATS email sender. They are rate-limited (default 30 per hour per channel).
5. Replies are collected: WhatsApp inbound messages from the relay, email replies from the mailbox (IMAP).
6. The local model classifies each reply into the 3 answers plus any corrected values. A low-confidence reading goes to the lead.
7. The agent compares the answers with what the recruiter entered and sets an outcome:
   - `confirmed`: contacted for this role, details match;
   - `details_mismatch`: contacted, but CTC, notice or another detail differs (the differences are listed);
   - `wrong_role`: contacted for a different role;
   - `not_contacted`: candidate says nobody contacted them (**possible false submission**);
   - `not_interested`;
   - `no_response`;
   - `opted_out`.
8. **Replanning:** no reply on WhatsApp after 48 h → one email; no reply after a further 72 h → `no_response`. There are at most 2 follow-ups, and the lead can stop it at any time.
9. Results go to the lead's queue. `not_contacted` and `wrong_role` are **escalated** with the evidence (the message, the reply, what the recruiter entered). The lead decides and records a reason.

## 5. Failure flows

- **WhatsApp relay down or the number is restricted:** switch to email for that batch and alert the admin.
- **Bounced email or invalid number:** outcome `unreachable`. Shown on the recruiter scorecard as a data-quality issue, not as a false submission.
- **Candidate replies with something unrelated, or abusive text:** routed to the lead. No automatic reply except the opt-out confirmation.
- **Prompt injection in a reply** ("ignore instructions…"): treated as data; the classifier output is schema-checked.

## 6. Acceptance criteria

- Given an unapproved draft, then nothing is sent (KPI-5 stays 0).
- Given a reply "No, nobody called me", then the outcome is `not_contacted`, it is escalated, and the recruiter's entry and the reply are shown side by side.
- Given a reply "Yes, but my notice is 60 days", then the outcome is `details_mismatch` with notice entered 30 vs stated 60.
- Given "STOP", then the candidate is marked opted out, gets one confirmation, and is never messaged again on any channel.
- Given no reply, then exactly one follow-up is sent by email after 48 h and the outcome is `no_response` after a further 72 h.

## 7. Rules and compliance

- BR-5: every outgoing message needs a named approver.
- BR-10: candidates can opt out of every message, and opt-outs apply across all channels.
- BR-11: verification results are not proof on their own. A recruiter is never penalised automatically; a lead decides.
- **DPDP Act 2023:** the purpose is stated in the message. Messages are sent only to contact details the candidate shared for recruitment. Replies are kept for 12 months and then deleted.
- Real PII stays local: replies are classified by the local model only (BR-4).
- **WhatsApp channel risk (R-17):** the ATS relay uses an unofficial WhatsApp Web library. Messaging candidates at volume can get the number restricted. Mitigation: low daily caps, approved messages only, email fallback. The official WhatsApp Business API charges per message, which conflicts with the $0 budget, so that is a later decision for the sponsor.

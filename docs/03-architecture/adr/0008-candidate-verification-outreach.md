# ADR-0008: Candidate verification messages through the ATS channels, with human approval

- Status: Accepted (PO, 2026-11-28)
- Supersedes: the MVP rule "no candidate or client contact" (BR-5 v0.2, PRD principle 5)

## Context

HR Guru needs to detect false or inaccurate submissions (UC-003). The only reliable signal is the candidate's own answer. The ATS already has two outbound channels: a WhatsApp relay (`apps/ats/deploy/whatsapp-relay`, based on `whatsapp-web.js`) and Gmail SMTP email. The cash budget is $0.

## Decision

1. TalentScout may contact candidates **only for verification and interest re-confirmation**, never for marketing or unsolicited job offers.
2. Every message is **drafted by the agent, approved by a named lead** (with re-authentication), and only then sent. There is an approval token per batch; sending without one is impossible at the tool level (`message.send` requires the token).
3. Messages go out through the **ATS's existing channels**, called by a new, narrowly scoped `message.send` MCP tool: WhatsApp relay `/send` and the ATS email sender. TalentScout does not hold WhatsApp or SMTP credentials itself.
4. Replies are read read-only: WhatsApp inbound events from the relay (new endpoint) and email replies via IMAP. They are classified **locally** (BR-4).
5. Opt-out (`STOP`) is honoured across all channels, permanently, and checked before every send.
6. Channels are rate-limited (default 30 messages per hour per channel and 150 per day), with an email fallback when WhatsApp fails.

## Consequences

- **Positive:** the false-submission check uses the candidate as the source of truth; no new paid services; one place (the MCP tool) enforces approval, rate limits and opt-outs.
- **Negative:** `whatsapp-web.js` is unofficial and Meta may restrict the number at volume (R-17). The official WhatsApp Business Cloud API charges per business-initiated message, which conflicts with the $0 constraint; switching is a sponsor decision.
- **Work:** the WhatsApp relay needs an inbound-message endpoint and hardening (token required, log-injection fixes); the ATS needs a mailbox for replies; the threat model and DPDP pack cover messaging.

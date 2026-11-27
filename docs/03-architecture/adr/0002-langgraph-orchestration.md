# ADR-0002: LangGraph as the single orchestration framework

- **Status:** Accepted
- **Date:** 2026-11-27

## Context
We need stateful multi-agent orchestration with conditional routing, human interrupts, checkpointing and resume. Candidates: LangGraph, OpenAI Agents SDK, Microsoft Agent Framework, CrewAI.

## Decision
LangGraph (MIT, self-hosted, no paid platform). Use one framework only. Interoperability with agents built in other frameworks comes via **A2A** in Sprint 6, not by mixing frameworks inside one service.

## Consequences
- (+) Explicit graphs are easy to explain, test and draw in interviews.
- (+) The MongoDB checkpointer keeps state in our single database.
- (−) There is a learning curve.
- Not chosen: OpenAI Agents SDK, Microsoft Agent Framework, CrewAI. They are revisited only if a concrete need appears (principle: no unnecessary frameworks).

# ADR-0001: Hybrid stack: MERN product tier with a Python agent service

- **Status:** Accepted
- **Date:** 2026-11-27
- **Deciders:** Architect, Product Owner

## Context
The brief asks for the MERN stack. The agent ecosystem (LangGraph durable execution, Langfuse, Ragas, DeepEval) is most mature in Python. Existing resume and JD parsers are assumed to be Python (A-04).

## Options considered
1. **Pure MERN.** LangGraph.js, MCP TypeScript SDK, Atlas Vector Search. One language, but weaker evaluation and observability tooling in JS.
2. **Hybrid.** React + Express + MongoDB + Node for the product; a Python FastAPI + LangGraph agent service; a Node MCP server between agents and data.
3. **Python + Postgres + Next.js.** Reuses parsers, but drops MERN and adds a second database.

## Decision
Option 2.

## Consequences
- (+) It meets the MERN brief and uses the best agent tooling.
- (+) The MCP boundary is a real architectural seam: agents never hold database credentials.
- (−) Two languages and three deployables. Mitigated with a monorepo, shared JSON Schemas (`packages/contracts`) and one Compose file.
- (−) The CI matrix covers Node and Python.

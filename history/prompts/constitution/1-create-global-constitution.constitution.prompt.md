---
id: 1
title: "Create Global Constitution"
stage: constitution
date: "2026-01-02"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "master"
user: "Abdul Rehman"
command: "/sp.constitution Evolution of Todo project constitution"
labels: ["constitution", "governance", "spec-driven-development"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
tests: []
outcome: "Successfully created the global constitution for the Evolution of Todo project"
evaluation: "Constitution includes all required principles and governance structure"
---

# Prompt History Record

## User Prompt
```
/sp.contitution  Create a single global constitution for the entire "Evolution of Todo" project
covering Phase I through Phase V.

This constitution must define:

1. Spec-Driven Development as mandatory
   - No agent may write code without approved specs and tasks
   - All work must follow: Constitution → Specs → Plan → Tasks → Implement

2. Agent Behavior Rules
   - No manual coding by humans
   - No feature invention
   - No deviation from approved specifications
   - Refinement must occur at spec level, not code level

3. Phase Governance
   - Each phase is strictly scoped by its specification
   - Future-phase features must never leak into earlier phases
   - Architecture may evolve only through updated specs and plans

4. Technology Constraints
   - Python for backend
   - Next.js for frontend (later phases)
   - FastAPI, SQLModel, Neon DB
   - OpenAI Agents SDK, MCP
   - Docker, Kubernetes, Kafka, Dapr (later phases)

5. Quality Principles
   - Clean architecture
   - Stateless services where required
   - Clear separation of concerns
   - Cloud-native readiness

This constitution must remain stable across all phases
and act as the supreme governing document for all agents.
```

## Assistant Response
Created a comprehensive constitution for the "Evolution of Todo" project that includes all required principles and governance structure. The constitution defines:

- Spec-Driven Development Mandate as the first core principle
- Agent Behavior Rules with clear constraints
- Phase Governance for controlled progression
- Technology Stack Compliance requirements
- Quality Principles for architecture standards
- Additional constraints and security requirements
- Development workflow and quality gates
- Governance structure as the supreme document

The constitution has been saved to `.specify/memory/constitution.md` and follows all specified requirements.
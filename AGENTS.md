# giltiq-python — Agent Rules

Python SDK for the Giltiq VAT validation API (`api.giltiq.de`). Thin typed wrapper over the REST API; no infrastructure. Published to PyPI on GitHub release via the `ci` workflow.

- Keep parity with the REST API and with `giltiq-node`; new endpoints land in the API first (API parity, DECISION-005 in the workspace root `DECISIONS.md`).
- Run the test suite before committing.
- Agent commits: `agent: <type>(<scope>): <description>`.
- Workspace-wide rules live in `../CLAUDE.md`.


## Project memory (Hindsight)

This repo is scoped to the shared `giltiq` Hindsight bank (see `.pi/hindsight.json`), which holds both engineering context and company strategy (business plan, DECISIONS.md, hypotheses, gate state). Before scouting the codebase or re-deriving architecture, check the `hindsight_knowledge` tool (action "search" or "tree", then "get") for existing pages — component map, core concepts, conventions, key decisions, initiatives. They refresh automatically from project memory. Use `hindsight_recall` for dated facts (what was decided when, what shipped vs. what a card claims). When you learn something durable — a decision, a root cause, an incident, a market signal — retain it with `hindsight_retain` and name the source.

# Design Notes: Multi-Agent Inventory & Sales System

## Purpose
This document summarizes key architectural decisions, error-handling strategies, and testing scope for the multi-agent system.

## Architecture Overview
- Orchestrator agent coordinates work across specialized agents:
  - Inventory Management Agent: stock checks, delivery estimates.
  - Quote Generation Agent: discount calculation, quote history lookup, financial context.
  - Sales Transaction Agent: sale execution, stock validation, financial updates.
- All tools are thin wrappers around centralized helper functions to keep behavior deterministic and testable.

## Key Decisions
- Single-file implementation `multi_agent_system.py` for portability and review simplicity.
- Normalization of item names using synonyms and substring matching to minimize false negatives.
- Per-request caching for delivery-time tools to reduce redundant calls.
- CSV-driven evaluation with results written to `test_results.csv` for downstream rubric checks.

## Error Handling & Stability
- Early validation of `.env` variables: `UDACITY_OPENAI_API_KEY`, `OPENAI_BASE_URL`.
- Database interactions via SQLAlchemy-backed Pandas queries; controlled exception handling returns safe defaults.
- No endless loops: deterministic iteration over dataset with bounded rate limiting.
- Tools return customer-safe error strings, not stack traces.

## Testing
- Unit tests (`tests/test_core.py`) cover:
  - Item name normalization
  - Supplier delivery thresholds
  - Discount logic
  - Sales processing and stock changes (point-in-time and subsequent day checks)
- Smoke test via `USE_SMOKE=1` environment variable (first request only).
- Full run produces `test_results.csv` for rubric evaluation using `evaluate_results.py`.

## Performance & Extendability
- Designed to minimize API calls by caching repeated delivery queries.
- Can extend recommendation logic (similar items) and multi-item quote optimization.
- Agents and tools are modular; adding a Business Advisor Agent is straightforward.

## File Map
- `multi_agent_system.py`: core agents and tools.
- `workflow.mmd`: Mermaid diagram of the system.
- `evaluate_results.py`: rubric evaluation for test results.
- `tests/test_core.py`: unit tests.
- `README.md`: run instructions and rubric mapping.
- `requirements_pinned.txt`: reproducible install set for local venv.

## Known Constraints
- Mermaid-to-PNG rendering requires `mermaid-cli` (Node). A helper script is provided; if Node isn’t available, use Mermaid live editors to export.


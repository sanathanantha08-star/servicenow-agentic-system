# IT Ticket Multi-Agent System

A supervisor–subagent LangGraph pipeline that automates triage and analysis of incoming IT/SOC tickets from ServiceNow. When a new ticket lands on a queue, a supervisor graph routes it through a series of specialized subagents — each running as its own isolated LangGraph subgraph — to assign priority, perform root cause analysis, and surface similar historical incidents.


## Architecture

**Pattern:** Supervisor–worker, with each worker implemented as its own LangGraph subgraph (not flat nodes), based on a subgraph pattern already used in production elsewhere.

**Flow:** Ticket lands on queue → Supervisor triggered → routes to Triage → RCA → Similar Incident → (future: Notification / Actions / Close).

**Stack:**
- **Orchestration:** LangGraph (Python)
- **LLM / Embeddings:** Cohere (chat for reasoning, embed for semantic search)
- **Database:** MongoDB (Atlas, using native `$vectorSearch` for the knowledge base and historical ticket similarity search)
- **Ticketing system:** ServiceNow (via REST Table API, `httpx` async client)
- **Queue:** AWS SQS
- **Config/Validation:** Pydantic + pydantic-settings
- **Logging:** structlog (structured JSON logs)
- **Retry:** tenacity, with a custom retryable/fatal exception taxonomy

## Folder Structure

```
src/ticket_agent/
├── main.py, graph.py, state.py, config.py     # entrypoint, top-level supervisor graph/state
├── agents/                                     # one subfolder per subagent (own state, graph, nodes, prompts)
│   ├── triage/
│   ├── rca/
│   └── similar_incident/
├── supervisor/                                 # supervisor routing logic
├── models/                                     # Pydantic data contracts (ticket, kb, rca)
├── tools/                                      # node-facing wrappers (embeddings, servicenow, search)
├── db/                                         # MongoDB persistence layer (session, kb_store, ticket_store)
├── core/                                       # cross-cutting: logging, retry, exceptions
└── queue/                                      # SQS listener
```

## Changelog

| Date | Area | What was built |
|---|---|---|
| 10 Aug 2026 | Config | `config.py` — nested `pydantic-settings` (Mongo, ServiceNow, LLM, Queue, App sub-models), secrets made required (no defaults), `.env` loading via `SettingsConfigDict` with nested delimiter |
| 10 Aug 2026 | Models | `models/ticket.py` — `Ticket`, `TicketStatus`, `TicketPriority` enums, optional `priority` (assigned later by triage) |
| 10 Aug 2026 | Models | `models/kb.py` — `KBDocument`, `KBSearchResult` (composed, not duplicated) |
| 10 Aug 2026 | Models | `models/rca.py` — `RcaResponse` with `ticket_id`, `rca_summary`, `recommendations: list[str]`, `confidence_score` (bounded 0–1), `kb_references` |
| 10 Aug 2026 | Core | `core/exceptions.py` — exception hierarchy: `TicketAgentError` → `RetryableError` / `FatalError`, with specific subclasses (ServiceNow, MongoDB, LLM) |
| 10 Aug 2026 | Core | `core/retry.py` — `retryable()` decorator factory using `tenacity`, wired to `RetryableError` and `AppSettings.max_retries` |
| 10 Aug 2026 | Core | `core/logging.py` — `configure_logging()` (structlog + stdlib logging level from settings), `get_logger()` with context binding |
| 10 Aug 2026 | DB | `db/session.py` — Motor async client, singleton pattern (`get_client()` / `get_database()`), graceful `close_client()` |
| 10 Aug 2026 | DB | `db/kb_store.py` — `insert_kb_documents`, `search_kb_documents` using `$vectorSearch` aggregation pipeline against MongoDB Atlas |
| 11 Aug 2026 | DB | `db/ticket_store.py` — `insert_tickets`, `get_similar_tickets` (same `$vectorSearch` pattern applied to the tickets collection) |
| 11 Aug 2026 | Tools | `tools/kb_retriever.py` — `generate_embeddings()` (Cohere async embed, parameterized `input_type`), `search_knowledge_base()` tying embedding + KB search together |
| 11 Aug 2026 | Tools | `tools/ticket_search.py` — `search_similar_tickets()`, reusing `generate_embeddings` from `kb_retriever.py` rather than duplicating it |
| 11 Aug 2026 | Tools | `tools/servicenow_client.py` — `ServiceNowClient` class (httpx async client, `get_ticket`, `update_ticket`), module-level singleton accessor |
| 11 Aug 2026 | State | `state.py` — top-level `SupervisorState` (ticket, kb_search_results, similar_tickets, rca, triage_result, current_ticket_status, error), all fields typed against real Pydantic/enum models |
| 11 Aug 2026 | State | `agents/triage/state.py` — `TriageWorkerState`, local to the triage subgraph, matching field names with the parent for automatic passthrough at the subgraph boundary |
| 11 Aug 2026 | Prompts | `agents/triage/prompts/triage_agent_prompt.py` — `SERVICENOW_TRIAGE_SYSTEM_PROMPT`, a detailed severity-classification prompt (Low/Medium/High) with explicit anti-hallucination rules and forced JSON output |
| 11 Aug 2026 | Nodes | `agents/triage/nodes.py` — `triage_node()`: calls Cohere chat with the triage prompt, parses JSON response, maps to `TicketPriority`, returns partial state update on success/failure |

## Key Design Decisions & Concepts Covered

- **`db/` vs `tools/` split:** `db/` holds raw MongoDB operations only; `tools/` wraps them with node-facing logic (e.g. computing embeddings before calling a DB search).
- **Subgraph state pattern:** parent (`SupervisorState`) and child (`TriageWorkerState`) state schemas intentionally share field names — this is the mechanism LangGraph uses to pass values across the subgraph boundary, not accidental duplication.
- **LangGraph node return semantics:** nodes return partial dicts of *changed* fields only; LangGraph's compiled graph executor merges those into state (overwrite-by-default per key, unless a field uses an `Annotated[..., operator.add]` reducer).
- **Retryable vs. fatal errors:** exceptions are classified by whether retrying could plausibly succeed, so `core/retry.py` can retry the right things and fail fast on the rest.

## Plan for 13 Aug 2026

1. Verify `triage_node` end-to-end against a real/sample ticket (confirm `settings.llm.cohere_model` field name matches `config.py`, confirm Cohere response shape).
2. (Optional) Wrap `triage_node`'s Cohere call with `@retryable()` and raise `LLMServiceError`/`LLMServiceTimeoutError` instead of the bare `except Exception`.
3. Build `agents/triage/graph.py` — wire `TriageWorkerState` + `triage_node` into an actual compiled subgraph.
4. Repeat the state → prompt → nodes → graph pattern for `agents/rca/` (uses `kb_retriever.py`, produces `RcaResponse`).
5. Then `agents/similar_incident/` (uses `tools/ticket_search.py`).
6. Build `supervisor/nodes.py` — routing logic between subagents, last since it depends on knowing what each subagent actually returns.
7. Wire everything together in top-level `graph.py`, then `queue/listener.py` and `main.py`.
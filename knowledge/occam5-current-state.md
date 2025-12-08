# Occam5 Current State Analysis

Analyzed from `/home/user/occam5` for migration planning.

## Overview

Occam5 is an AI-powered collaboration platform with:
- **Backend**: FastAPI + SQLAlchemy 2.0 (async)
- **Frontend**: Vue 3 + Vite + Radix Vue + Tailwind
- **Database**: SQLite (default), PostgreSQL support
- **AI**: LangChain, LangGraph, OpenAI/Anthropic/Azure
- **Vector**: Milvus / in-memory
- **Real-time**: FastAPI WebSockets
- **Containers**: Podman (rootless desktops/terminals)

## Directory Structure

```
/home/user/occam5/
├── backend/
│   └── app/
│       ├── api/              # REST endpoints (~19 routers)
│       ├── agent/            # LangGraph workflows
│       ├── auth/             # FastAPI Users, JWT
│       ├── models/           # SQLAlchemy models (~35 models)
│       ├── services/         # Business logic (~80 services)
│       ├── tools/            # 20+ AI tools
│       ├── vector/           # Embedding, chunking, stores
│       └── websocket/        # Room-based broadcasting
├── frontend/
│   └── src/
│       ├── components/       # 18 feature domains
│       ├── composables/      # Business logic hooks
│       └── views/            # Top-level views
├── docker/                   # Podman desktop images
├── archon/                   # Additional agent system
├── cms/                      # Content management
└── desktop/                  # FUSE/native client
```

## Database Models (35+)

**Core:**
- User, UserCredentials, UserRelations
- ChatThread, Share, Group
- Site, SiteMember

**AI/ML:**
- AIModel, AIUsage, Workflow
- TaskGraph, ToolChoice
- Trace, Interaction

**Features:**
- DriveEntryEvent, Notification
- Social, Contact, Widget
- Credit, Subscription
- DeviceSession, DeviceAuth
- WebPushSubscription

## Services (~80 modules)

**Key Services:**
- `drive_service.py` (62KB) - File operations, versioning
- `share_service.py` (46KB) - User/group/email sharing
- `container_service.py` (39KB) - Podman orchestration
- `subscription_service.py` (25KB) - Stripe integration
- `memory_service.py` (23KB) - LangMem integration
- `presentation_service.py` (21KB) - Task graph
- `credit_service.py` (17KB) - Usage tracking

**AI Services:**
- `ai_agent_generator.py` - Character generation
- `agent_settings_service.py` - Agent configuration
- `tool_embedding_service.py` - Tool selection
- `workflow_engine.py` - LangGraph execution

## Capabilities

### Already Implemented
- ✅ Multi-agent orchestration (LangGraph)
- ✅ 20+ AI tools (web, DB, image gen)
- ✅ Vector search (Milvus)
- ✅ Real-time WebSocket
- ✅ File drive with versioning
- ✅ Social features (friends, groups, posts)
- ✅ Container desktops (Podman + noVNC)
- ✅ Credit/subscription system
- ✅ OAuth connectors

### MCP Integration
- **Chrome DevTools MCP**: Fully configured
  - Claude Code: `.claude/settings.json` has 20+ `mcp__chrome-devtools__*` tools
  - AI Agents: `ai_tools.yaml` has `chrome_devtools` mcp_server entry (added Cycle 74)
- Playwright MCP for E2E testing
- Config in `.claude/` directory

## Tech Stack Comparison: Giz vs Occam5

| Component | Giz | Occam5 |
|-----------|-----|--------|
| Backend | NestJS (Node.js) | FastAPI (Python) |
| Frontend | Vue 3 + Quasar | Vue 3 + Radix/Tailwind |
| Database | PostgreSQL (Knex.js) | SQLite/PostgreSQL (SQLAlchemy) |
| Cache | Redis | Redis (optional) |
| Real-time | Socket.IO | FastAPI WebSockets |
| AI | OpenAI, Anthropic, LangChain | LangChain, LangGraph |
| Vector | Milvus | Milvus |
| Container | - | Podman |

## Migration Considerations

### Can Reuse from Giz
1. **AI plugin patterns** - Both use OpenAI/Anthropic/LangChain
2. **Vector/Milvus integration** - Similar approach
3. **UI components** - Vue 3 in both, need style adaptation
4. **Redis patterns** - Both use Redis for caching/pub-sub

### Needs Translation
1. **Database ORM** - Knex.js → SQLAlchemy
2. **Server framework** - NestJS → FastAPI
3. **Real-time** - Socket.IO → FastAPI WebSockets
4. **Plugin system** - Giz plugins → Occam5 services

### Occam5 Unique Features (Keep)
- Podman container orchestration
- LangGraph agent workflows
- Credit/subscription system
- FUSE desktop client

## Test Status (Cycle 101 - 2025-12-08)

### Backend Tests: 243 passed, 48 failed, 9 errors
**Error Categories:**
1. **UUID fixture issues (9 errors)** - `test_agent_settings.py` uses string IDs like `test-user-1` instead of UUIDs
2. **Missing DriveService methods (8 fails)** - `create_public_link`, `update_item_shares` not implemented
3. **Import errors (5 fails)** - `langchain_groq`, `load_config`, `ai_analyze_code` missing
4. **API changes (7 fails)** - `ToolEmbeddingService.index_tools`, `ContextRanker` params changed
5. **Code edit engine (4 fails)** - tuple vs float comparison, omission detection broken

### Frontend Unit Tests: 84 passed (100%)
All frontend unit tests passing.

### Frontend E2E Tests: Not run
Playwright E2E tests exist in `frontend/tests/e2e/` but require running backend.

### Priority Fixes Before Migration
1. Fix UUID fixture in test_agent_settings.py
2. Implement or stub DriveService share methods
3. Fix code_edit_engine tuple/float comparison
4. Update ToolEmbeddingService tests for new API

---
*Updated Cycle 101 - Integration test baseline*

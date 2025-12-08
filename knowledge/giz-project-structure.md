# Giz Project Structure Analysis

Analyzed from `/home/user/giz` for Occam5 migration.

## Overview

Giz is a modular AI-powered platform built by ExInno Co., Ltd.

**Tech Stack:**
- Backend: NestJS (Node.js)
- Frontend: Vue 3 + Quasar
- Database: PostgreSQL (via Knex.js)
- Cache/Pub-Sub: Redis
- Queue: BullMQ
- Real-time: Socket.IO
- Package Manager: Yarn 3 workspaces

## Directory Structure

```
/home/user/giz/
├── common/           # Shared library (giz-common)
├── platform/
│   ├── server/       # NestJS backend (giz-server)
│   └── web/          # Vue 3 + Quasar frontend
├── plugins/
│   ├── ai/           # AI integration (OpenAI, Anthropic, Google, LangChain)
│   ├── ej2/          # Syncfusion EJ2 UI components
│   ├── search/       # Full-text search
│   ├── space/        # Workspace/collaboration
│   ├── storage/      # File storage (agents, CSV)
│   └── tiptap/       # Rich text editor
├── apps/
│   ├── container/    # Container app
│   ├── crm/          # CRM app
│   ├── examples/     # Example apps
│   └── space/        # Space app
├── supportbot/       # Support bot module
├── landings/         # Landing pages
├── ml/               # ML components
├── ops/              # Operations/deployment
└── docker-images/    # Docker configurations
```

## Database Configuration

**Connection Strings (from giz.env):**
```
GIZ_DS_DEFAULT=postgres://giz:****@chi.giz.ai:5432/giz
GIZ_DS_READONLY=postgres://giz:****@chi.giz.ai:5432/giz
GIZ_REDIS=redis://:****@chi.giz.ai:6379
```

**ORM:** Knex.js (not TypeORM/Prisma)
- SQL queries in `platform/server/src/data/sql.data.service.ts`
- Schema inspection via `knex-schema-inspector`

## Key Plugins Analysis

### 1. AI Plugin (`/plugins/ai`)
**Dependencies:**
- `@anthropic-ai/bedrock-sdk` - Claude via AWS Bedrock
- `openai` - OpenAI API
- `@google/genai` - Google Gemini
- `langchain` - LLM orchestration
- `@zilliz/milvus2-sdk-node` - Vector DB
- `replicate` - Replicate models
- `@runware/sdk-js` - Image generation
- `puppeteer` - Browser automation
- `redis-om` - Redis object mapping

**Structure:**
- `model/` - AI model definitions
- `server/` - Backend services
- `web/` - Frontend components

### 2. Storage Plugin (`/plugins/storage`)
**Structure:**
- `agent/` - Agent storage
- `agent-injected/` - Injected agent storage
- `csv/` - CSV handling
- `model/` - Storage models
- `server/` - Storage services
- `web/` - Storage UI

### 3. EJ2 Plugin (`/plugins/ej2`)
- Syncfusion EJ2 component integration
- Data grid, pivot views
- Custom data managers

### 4. TipTap Plugin (`/plugins/tiptap`)
- Rich text editor
- Collaborative editing support
- Markdown support

### 5. Search Plugin (`/plugins/search`)
- Full-text search functionality
- Faceted search
- Result highlighting

### 6. Space Plugin (`/plugins/space`)
- Workspace management
- Collaboration features
- Real-time editing

## Server Architecture

**Entry Point:** `platform/server/src/main.ts`

**Key Modules:**
- `auth/` - Authentication/authorization
- `data/` - Data access layer (Knex)
- `model/` - Model management
- `queue/` - Background job processing
- `notification/` - Push notifications
- `security/` - Security services
- `license/` - License management

## Build System

**Yarn Scripts:**
```bash
yarn build-common    # Build shared library
yarn build-server    # Build backend
yarn build-web       # Build frontend
yarn build-required  # Build all components
yarn start:pm2       # Start with PM2
```

## Migration Considerations for Occam5

1. **Database:** Same PostgreSQL schema can be reused
2. **Plugins:** AI plugin has direct relevance (OpenAI, Anthropic, LangChain)
3. **Storage:** Agent storage patterns applicable
4. **Auth:** Can reuse authentication patterns
5. **Real-time:** Socket.IO patterns transferable

---
*Analyzed for Occam5 migration - Cycle 63*

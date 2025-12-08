# Giz → Occam5 Migration Plan

## Executive Summary

**Goal**: Migrate Giz platform functionality to Occam5, combining Giz's enterprise features with Occam5's modern AI-first architecture.

**Approach**: Feature-by-feature migration, not database-level dump. Occam5 has different data models optimized for its architecture.

---

## Phase 1: Data Model Mapping

### User & Auth Migration

| Giz (Knex/PostgreSQL) | Occam5 (SQLAlchemy) | Notes |
|----------------------|---------------------|-------|
| `users` table | `User` model | Map email, profile fields |
| Custom auth | FastAPI Users | OAuth, JWT already in Occam5 |
| Sessions | DeviceSession | Multi-device support |

**Migration Script Needed**:
```python
# backend/scripts/migrate_giz_users.py
# 1. Connect to Giz PostgreSQL
# 2. Read users table
# 3. Create Occam5 users via User model
# 4. Preserve email, creation dates
```

### File Storage Migration

| Giz | Occam5 | Notes |
|-----|--------|-------|
| S3/Storage plugin | DriveService | POSIX-compliant storage |
| File metadata | DriveEntryEvent | Event logging |
| Sharing | ShareService | User/group/email sharing |

**Strategy**: Export files from Giz storage → Import to Occam5 drive per user

### AI Agent Migration

| Giz (plugins/ai) | Occam5 (backend/app/agent) | Action |
|------------------|---------------------------|--------|
| OpenAI client | Already exists | Use Occam5 |
| Anthropic client | Already exists | Use Occam5 |
| LangChain tools | Already exists | Use Occam5 |
| Milvus vector | Already exists | Use Occam5 |

**No migration needed** - Occam5 has superior agent architecture (LangGraph)

### EJ2 Components

| Giz Plugin | Occam5 Equivalent | Action |
|------------|-------------------|--------|
| DataGrid | Radix Table + custom | Port component styles |
| PivotView | Custom implementation | Lower priority |
| Charts | Chart.js / similar | If needed |

**Strategy**: Identify which EJ2 features are critical, implement in Occam5 Vue components

### TipTap Editor

| Giz | Occam5 | Action |
|-----|--------|-------|
| TipTap plugin | Milkdown | Occam5 uses Milkdown already |

**Strategy**: Milkdown is adequate; no migration needed

---

## Phase 2: Feature-by-Feature Migration

### Priority 1: Core Data

1. **User Migration**
   - Export Giz users
   - Create Occam5 accounts
   - Generate password reset tokens for re-authentication

2. **File Migration**
   - Export Giz storage files with metadata
   - Import to Occam5 drive per user
   - Preserve folder structure

### Priority 2: AI Features

Already covered by Occam5's superior implementation:
- Agent workflows (LangGraph)
- Tool registry (20+ tools)
- Vector search (Milvus)
- Streaming (WebSocket)

### Priority 3: Collaboration

1. **Groups** - Occam5 has Group model
2. **Sharing** - ShareService covers user/group/email
3. **Real-time** - WebSocket manager ready

### Priority 4: UI Polish

1. Port essential Giz UI patterns to Occam5
2. Adapt EJ2 component styles to Radix/Tailwind
3. Ensure mobile responsiveness

---

## Phase 3: Database Migration Scripts

### Script 1: User Migration

```python
# backend/scripts/migrate_giz_users.py
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.user import User
from app.database import async_session

GIZ_DB_URL = "postgresql+asyncpg://giz:****@chi.giz.ai:5432/giz"

async def migrate_users():
    giz_engine = create_async_engine(GIZ_DB_URL)
    async with giz_engine.connect() as conn:
        result = await conn.execute("SELECT id, email, name, created_at FROM users")
        users = result.fetchall()

    async with async_session() as session:
        for user in users:
            new_user = User(
                email=user['email'],
                display_name=user['name'],
                # ... other fields
            )
            session.add(new_user)
        await session.commit()
```

### Script 2: File Migration

```python
# backend/scripts/migrate_giz_files.py
# 1. Connect to Giz storage
# 2. Download files per user
# 3. Upload to Occam5 drive via DriveService
# 4. Preserve folder structure and metadata
```

---

## Phase 4: Chrome DevTools Integration

From twenim knowledge (Task 1):

### Add MCP Server Config

```yaml
# .claude/config.yaml or mcp.json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["@anthropic/mcp-chrome-devtools"]
    }
  }
}
```

### Create DevTools Service

```python
# backend/app/services/devtools_service.py
class DevToolsService:
    async def take_snapshot(self, page_idx: int = 0):
        """Get a11y tree snapshot"""
        pass

    async def click(self, uid: str):
        """Click element by UID"""
        pass

    async def evaluate_script(self, script: str):
        """Execute JavaScript"""
        pass
```

### Add as AI Tool

```python
# backend/app/tools/devtools_tool.py
class DevToolsTool:
    """Browser automation via Chrome DevTools"""
    # Expose take_snapshot, click, fill, evaluate_script to agents
```

---

## Phase 5: Deployment Preparation

### Pre-Deployment Checklist

- [ ] Database backups (both Giz and Occam5)
- [ ] Environment variables configured
- [ ] SSL certificates ready
- [ ] DNS pointing to new server

### Migration Sequence

1. **Backup Giz database**
2. **Run user migration script**
3. **Run file migration script**
4. **Verify data integrity**
5. **Deploy Occam5 with migrated data**
6. **Update DNS**
7. **Monitor for issues**

### Rollback Plan

1. Keep Giz running in parallel during transition
2. If issues: revert DNS to Giz
3. Fix Occam5 issues, retry migration

---

## Timeline Estimate

| Phase | Tasks | Cycles |
|-------|-------|--------|
| 1 | Data model mapping | 1-2 |
| 2 | Migration scripts | 3-5 |
| 3 | Run migration | 1 |
| 4 | Chrome DevTools | 2-3 |
| 5 | Testing & polish | 3-5 |
| 6 | Deployment | 1-2 |

**Total: ~15-20 cycles**

---

## Success Criteria

1. ✅ All Giz users can log into Occam5
2. ✅ All files accessible in Occam5 drive
3. ✅ AI agents functional with same capabilities
4. ✅ Chrome DevTools integrated for browser automation
5. ✅ No data loss during migration
6. ✅ Production deployment stable

---
*Migration plan created - Cycle 63*

# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

instance-management

## Roadmap

### project-skeleton — FastAPI + React project skeleton with basic structure

Status: done

Acceptance:
- Backend FastAPI app runs with health endpoint
- Frontend React + TypeScript + Vite app builds
- Docker compose with backend, frontend, Keycloak
- Basic README with install/run instructions

Implementation: `backend/app/main.py`, `backend/app/api/v1/health.py`, `backend/app/api/v1/instances.py`, `backend/app/models/instance.py`, `backend/app/models/instance_db.py`, `backend/app/services/instance_service.py`, `backend/app/core/config.py`, `backend/app/core/database.py`, `backend/requirements.txt`, `backend/tests/test_health.py`, `backend/tests/test_instances.py`, `backend/tests/test_models.py`, `backend/tests/test_root_health.py`, `backend/tests/conftest.py`, `frontend/package.json`, `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/components/InstancesPage.tsx`, `frontend/src/api/instances.ts`, `frontend/src/types/api.ts`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/src/test/setup.ts`, `frontend/src/components/InstancesPage.test.tsx`, `frontend/src/components/App.test.tsx`, `Dockerfile.backend`, `Dockerfile.frontend`, `compose.yaml`, `README.md`, `CHANGELOG.md`, `portfolio.json`, `.env.example`, `.gitignore`, `.github/workflows/ci.yml`, `keycloak/realm-export.json`

Tests: `backend/tests/test_health.py`, `backend/tests/test_instances.py`, `backend/tests/test_models.py`, `backend/tests/test_root_health.py`, `frontend/src/components/InstancesPage.test.tsx`, `frontend/src/components/App.test.tsx`

### instance-management — Minecraft instance management (create, list, launch)

Status: in_progress

Acceptance:
- Create new instance with version selection
- List instances with metadata
- Launch instance with Java detection

Implementation: `backend/app/services/java_detection.py`, `backend/app/services/instance_service.py`, `backend/app/api/v1/instances.py`, `frontend/src/types/api.ts`, `frontend/src/api/instances.ts`, `frontend/src/components/InstancesPage.tsx`, `frontend/src/App.css`

### auth-yggdrasil — Yggdrasil authentication with ALI support

Status: planned

Acceptance:
- Microsoft/Yggdrasil login flow
- Authlib-Injector header support
- Offline mode support

### mod-management — Mod loading and management

Status: planned

Acceptance:
- Mod profile creation
- Modrinth/CurseForge integration
- Dependency resolution


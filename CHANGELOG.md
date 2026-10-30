# Changelog

## 1.1.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-10-22

### Added
- Initial project skeleton with FastAPI backend and React frontend
- Instance management API (create, list, get, update, delete, launch)
- SQLite persistence with SQLAlchemy async
- React + TypeScript + Vite frontend with instance dashboard
- Docker Compose with backend, frontend, and Keycloak
- Basic CI workflow (backend tests, frontend build/test, Docker builds)
- Health check endpoints
- Portfolio.json with project metadata

## [Unreleased] - 2026-10-30

### Added
- Java detection service for automatic Java installation discovery
- Launch info endpoint (`GET /api/v1/instances/{id}/launch-info`) returning detected Java and launch command
- Frontend "Launch Info" modal showing Java version, path, JDK/JRE type, and full launch command
- Minecraft version to Java version mapping (1.12→Java 8, 1.16→Java 11, 1.17→Java 16, 1.18+→Java 17)
- Copy-to-clipboard for launch command in UI

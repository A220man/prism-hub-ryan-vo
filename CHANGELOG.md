# Changelog

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
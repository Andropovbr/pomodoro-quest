# pomodoro-quest

A simple gamified Pomodoro-style productivity app.

## Overview

## Architecture (high-level)

## Local Development

## Testing Strategy

## Reliability & SRE Considerations

This project intentionally goes beyond basic application code and includes reliability-oriented decisions inspired by real-world SRE practices.

### Application lifecycle vs. database lifecycle

During development, the project surfaced a common reliability pitfall: **database schema availability depending on application startup order**.

To address this:

- Database tables are created explicitly during application startup
- Test execution ensures database initialization happens before any request handling
- This mirrors production scenarios where schema readiness must be guaranteed before serving traffic

### Test isolation and database consistency

Early iterations used an in-memory SQLite database for tests (`sqlite:///:memory:`), which led to flaky failures due to SQLite’s **per-connection memory model**.

To ensure deterministic tests:

- Tests use a **file-based SQLite database** scoped exclusively to the test environment
- This guarantees consistent state across multiple connections, mirroring production behavior
- Persistent state from local development is explicitly avoided

This reflects a core SRE principle: **tests must be reliable, repeatable, and environment-independent**.

### Failure modes explicitly handled

The application explicitly handles several failure modes:

- Invalid state transitions (e.g. completing an already completed session)
- Missing resources (sessions or users not found)
- Data integrity violations (sessions referencing a non-existent user)

These safeguards make failure conditions visible and predictable instead of silent.

### Operational mindset

Although this is a small application, it was designed with operational concerns in mind:

- Clear separation between application logic and infrastructure concerns
- Environment-driven configuration (ready for secrets and managed databases)
- Deterministic startup behavior suitable for containerized deployments (ECS, Kubernetes)


## Deployment Notes (future)

## Local run (Docker)
```bash
docker compose up --build


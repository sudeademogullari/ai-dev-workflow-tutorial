<!--
SYNC IMPACT REPORT
==================
Version change: [uninitialized] → 1.0.0
Reason: Initial ratification — derived from 5-question project intake.

Principles defined:
  - I. Audience-First Design (new)
  - II. Real-Time Data by Default (new)
  - III. Multi-Source Data Integrity (new)
  - IV. Public-Safe Deployment (new)
  - V. Minimal Testing Discipline (new)

Added sections:
  - Technology Stack
  - Governance

Templates reviewed:
  - ✅ .specify/templates/plan-template.md — Constitution Check section is generic;
       gates should reference Principles I–V above.
  - ✅ .specify/templates/spec-template.md — mandatory sections align with principles.
  - ✅ .specify/templates/tasks-template.md — testing is marked OPTIONAL, consistent
       with Principle V (smoke tests only).
  - ✅ .specify/templates/commands/ — directory is empty; no files to update.

Deferred TODOs: none
-->

# E-Commerce Analytics Dashboard Constitution

## Core Principles

### I. Audience-First Design

Every feature MUST serve at least one of the three identified audiences with
clearly justifiable value.

- **Executives**: High-level KPIs, trend summaries, minimal friction.
- **Sales analysts**: Filtering, drill-downs, data exploration.
- **Operations teams**: Regional breakdowns, fulfillment metrics, inventory signals.

Rules:
- New charts or features MUST name the target audience in their spec.
- Features that serve no identified audience MUST NOT be added.
- When audiences conflict, executive readability takes precedence for the default view;
  analyst/ops depth MUST be accessible but SHOULD NOT clutter the primary layout.

### II. Real-Time Data by Default

Live data refresh is a first-class requirement, not an enhancement.

- All visualizations MUST display a visible data freshness indicator (timestamp or
  "last updated" label).
- Caching MUST be implemented to prevent excessive API calls while maintaining
  acceptable staleness — target refresh interval MUST be defined per data source.
- The app MUST degrade gracefully when live data is unavailable: fall back to the
  most recent cached or CSV data and surface a clear status message to the user.
- Silent staleness is not acceptable.

### III. Multi-Source Data Integrity

Historical CSV data and live API data are both canonical; they MUST be reconciled
consistently and transparently.

- The data layer MUST clearly distinguish the source (CSV vs. live API) for any
  displayed metric.
- Schema contracts between sources MUST be defined and validated at load time.
- Discrepancies between sources MUST surface as warnings, not silent overrides.
- No metric may blend CSV and live data without an explicit reconciliation strategy
  documented in the spec.

### IV. Public-Safe Deployment

The dashboard is publicly accessible on Streamlit Community Cloud. All deployment
decisions MUST treat exposure to anonymous public traffic as the default threat model.

- Secrets (API keys, credentials) MUST be stored in Streamlit secrets management,
  never in code or the repository.
- No personally identifiable information (PII) from real customers may appear in the
  deployed app or the repository.
- All Python dependencies MUST be pinned to specific versions in `requirements.txt`.
- The app MUST remain functional and performant under typical anonymous public traffic
  without requiring authentication.

### V. Minimal Testing Discipline

Testing scope is intentionally lightweight: smoke tests only.

- Tests MUST verify: (1) the app loads without error, (2) all charts render,
  (3) each data source connects successfully.
- TDD is NOT required. Tests SHOULD be written after implementation.
- All smoke tests MUST pass before any deployment to Streamlit Community Cloud.
- Unit tests for data transformations are optional and SHOULD only be added when
  a transformation is complex enough to have a non-obvious failure mode.

## Technology Stack

Canonical stack for this project. Deviations require documented rationale.

| Layer | Choice |
|-------|--------|
| Language | Python 3.11+ |
| UI framework | Streamlit |
| Charting | Plotly |
| Data manipulation | Pandas |
| Package management | uv |
| Deployment | Streamlit Community Cloud |
| Data sources | CSV (historical) + live API (real-time) |

- The stack MUST NOT grow without a principle-backed justification.
- New dependencies MUST be added to `requirements.txt` with pinned versions.

## Governance

This constitution supersedes all other conventions for this project.
When this file conflicts with any other document, the constitution takes precedence
and the conflicting document MUST be updated.

**Amendment procedure**:

1. Identify which principle is affected and state the rationale for change.
2. Bump the version per the policy below.
3. Update `LAST_AMENDED_DATE` to today's date.
4. Re-run the Consistency Propagation Checklist (`/speckit.constitution`).
5. Update any templates or specs made inconsistent by the amendment.

**Versioning policy**:

- MAJOR: Removing or fundamentally redefining a principle.
- MINOR: New principle, section, or materially expanded guidance.
- PATCH: Clarifications, wording fixes, non-semantic refinements.

**Compliance**: All features MUST pass a Constitution Check (see `plan-template.md`)
before implementation begins. The runtime development guidance file is `CLAUDE.md`.

**Version**: 1.0.0 | **Ratified**: 2026-03-29 | **Last Amended**: 2026-03-29

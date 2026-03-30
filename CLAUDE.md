# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is a **documentation-only tutorial** teaching AI-assisted software development workflows. It contains no runnable application code — participants build a Streamlit sales dashboard in their own repos by following these guides.

## Repository Structure

- `README.md` — top-level overview
- `prd/ecommerce-analytics.md` — the Product Requirements Document participants use as their specification
- `data/sales-data.csv` — sample dataset for the dashboard (482 orders, 12 months of 2024)
- `v1/` — original multi-document tutorial (two 100-minute sessions)
- `v2/` — current format: async pre-work + 3-hour live workshop
  - `pre-work-setup.md` — account creation, tool installation, repo setup (~60–90 min)
  - `workshop-build-deploy.md` — spec-kit planning → Claude Code implementation → Streamlit deployment (~3 hours)

## Content Conventions

**v2 is the current/canonical version.** v1 is kept as reference material.

**Commit messages** in this repo follow conventional format referencing what changed in the docs (not Jira issues, since this repo *teaches* that workflow rather than using it internally).

**Terminology consistency** matters across files:
- The tool is "Claude Code" (not "Claude", "claude", or "Claude CLI")
- The IDE is "Cursor" (not "VS Code" or "cursor")
- The package manager is "uv" (not "pip" directly for this workflow)
- The deployment target is "Streamlit Community Cloud"

**UI/flow caveats:** Both tutorial documents include notes that UI screenshots and flows evolve — when updating instructions, prefer describing the *goal* of a step rather than exact button labels when those are likely to change.

## The Workflow Being Taught

```
PRD → spec-kit → Jira tasks → Claude Code → git commit (with Jira ref) → GitHub push → Streamlit deploy
```

The core principle: every code change traces back to a Jira issue, which traces back to a spec-kit plan, which traces back to the PRD requirement.

## Dashboard Spec (What Participants Build)

The completed dashboard has:
- Two KPI scorecards: Total Sales (~$650K–$700K) and Total Orders (482)
- Sales trend line chart (monthly, 12 months)
- Category bar chart (Electronics, Accessories, Audio, Wearables, Smart Home)
- Regional bar chart (North, South, East, West)

Stack: Python 3.11+, Streamlit, Plotly, Pandas, deployed to Streamlit Community Cloud.

## Active Technologies
- Python 3.11+ + Streamlit, Plotly, Pandas (001-analytics-dashboard)
- CSV file (`data/sales-data.csv`) — no database (001-analytics-dashboard)

## Recent Changes
- 001-analytics-dashboard: Added Python 3.11+ + Streamlit, Plotly, Pandas

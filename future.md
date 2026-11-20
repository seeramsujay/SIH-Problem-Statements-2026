# SIH 2026 Dataset: Future Roadmap & Analytical Tooling

This repository provides an automated extraction pipeline and clean structured dataset for all 226 Smart India Hackathon 2026 problem statements. This roadmap outlines future analytical tool extensions.

---

## 1. Web Portal & Interactive Semantic Exploration

- **Web-Based Problem Statement Explorer**:
  - Deploy a lightweight, client-side static web application (Vite + React) hosted on GitHub Pages.
  - Implement full-text client-side search via MiniSearch with multi-select theme filters, ministry breakdowns, and hardware/software category toggles.
- **Vector Embedding Semantic Search**:
  - Precompute sentence embeddings for each problem statement description using `all-MiniLM-L6-v2`.
  - Allow teams to input project skills or tech stacks to surface the most relevant problem statements.

---

## 2. Competitive Intelligence & Solution Scaffolding

- **Automated Feasibility & Architecture Scaffolder**:
  - AI-assisted scaffolding script generating modular project templates (FastAPI, Next.js, Embedded C++) customized to the hardware/software specs of each problem statement.
- **Past Winner Pattern Matching**:
  - Cross-reference previous hackathon editions (SIH 2020-2025) to identify winning patterns, common submission blindspots, and recommended presentation artifacts.

---

## 3. Automation & Real-Time Notification

- **Automated Webhook Monitoring**:
  - GitHub Actions cron workflow to monitor `sih.gov.in` for newly added problem statements, amendments, or deadline revisions, generating automated git commits and Discord/Telegram alert webhooks.

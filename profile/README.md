<p align="center"><a href="https://github.com/Zeid-Data"><img src="https://raw.githubusercontent.com/zeiddata-dev/Research/main/assets/banners/readme/root.png" alt="Zeid Data Research" width="100%"></a></p>

# Zeid Data

![Focus: Defensive Security](https://img.shields.io/badge/Focus-Defensive%20Security-0f766e) ![Build: Evidence First](https://img.shields.io/badge/Build-Evidence%20First-111827) ![Ops: Reproducible](https://img.shields.io/badge/Ops-Reproducible-2563eb) ![Scope: Authorized Review](https://img.shields.io/badge/Scope-Authorized%20Review-7c2d12)

Defensive security engineering, detection content, and operational data systems.

<!-- ZEID-DATA:README:BEGIN -->

## Mission

| Principle |
| --- |
| Build practical tools for authorized security review. |
| Turn evidence, logs, and telemetry into measurable defensive action. |
| Keep security work reproducible, auditable, and grounded in artifacts. |

## Now Building

| Track | Status | Focus | Next |
| --- | --- | --- | --- |
| Lithium | ![Status: Running private build](https://img.shields.io/badge/Status-Running%20private%20build-0f766e) | Auth-gated React/Vite dashboard, SQLite-backed normalized evidence records, relative API routing, search-first review, and privacy-aware evidence drilldowns. | Prove the active React shell is the served UI, keep chat logs searchable, validate evidence drawer cleanup, and preserve viewer-gated API behavior. |
| Speculum | ![Status: Active build](https://img.shields.io/badge/Status-Active%20build-0f766e) | Authorized public-surface review utilities and security audit workflows. | Expand tests, reporting, documentation, and safe input validation. |
| Detection Engineering | ![Status: Ongoing](https://img.shields.io/badge/Status-Ongoing-0f766e) | Sigma, KQL, SPL, Elastic, structured indicators, and defensive validation scripts. | Convert repeatable incident patterns into tested detection content. |
| Infrastructure Hardening | ![Status: Ongoing](https://img.shields.io/badge/Status-Ongoing-0f766e) | Inventory, configuration review, service exposure checks, and rollback-safe automation. | Keep scripts small, auditable, reversible, and evidence-producing. |

## 🤖 Lithium Bot Tracker

<table>
<tr>
<td width="70" align="center">🤖</td>
<td>
<strong>Lithium status:</strong> Running private build<br>
<strong>Current read:</strong> Auth-gated React dashboard backed by normalized SQLite evidence records<br>
<strong>Next proof:</strong> Served UI must match the active React shell build, not stale dashboard assets
</td>
</tr>
</table>

| Area | Current running state |
| --- | --- |
| Status | ![Lithium: Running private build](https://img.shields.io/badge/Lithium-Running%20private%20build-7c3aed) |
| Public boundary | Dashboard traffic enters through an authenticated Nginx proxy. Unauthenticated dashboard and API requests are expected to return `401 Unauthorized`. |
| Frontend | React/Vite dashboard shell. User-facing UI name is `Lithium`. The active UI must be served from the current React shell build, not legacy Streamlit pages, stale release folders, or copied dashboard assets. |
| API contract | Frontend uses relative same-origin API calls, especially `GET /api/chat/events`. Public IPs, localhost ports, tokens, chat IDs, and direct backend service ports are intentionally not documented here. |
| Data layer | SQLite-backed normalized dashboard records. Raw Telegram, journal, memory, and bridge files are treated as source evidence, not runtime dashboard data sources. |
| Access model | Dashboard access is viewer-gated. Admin views and normal evidence views are separated. Unknown or unauthenticated viewers are blocked before records are exposed. |
| Current UI priority | Chat Logs first: search, profile filters, source filters, count audit bar, readable table columns, row-click evidence drawer, and clean technical evidence details. |
| Evidence rule | Claims, summaries, filters, and dashboard cards must link back to evidence records or clearly show that evidence is missing. No fake scores, unsupported insights, or raw JSON dumps in the normal UI. |
| Active services summary | Nginx, React shell, dashboard backend/proxy, public API proxy, and chat events API are active. A duplicate React API service was intentionally disabled to avoid port collision. |
| Safety note | No secrets are stored in this public tracker. Runtime credentials, private messages, chat IDs, tokens, passwords, and private evidence text are excluded. |

## Threat Intel Radar

| Pattern | Severity | Defender Focus | Signals | Build Response |
| --- | --- | --- | --- | --- |
| Credential phishing and token replay | ![Severity: Critical](https://img.shields.io/badge/Severity-Critical-red) | Identity telemetry, mailbox rules, OAuth grants, session anomalies, and account recovery evidence. | New consent grant<br>Impossible travel<br>Unexpected mailbox rule<br>Suspicious successful login | Identity review scripts, detection logic, and incident evidence checklists. |
| Infostealer-driven account takeover | ![Severity: Critical](https://img.shields.io/badge/Severity-Critical-red) | Endpoint evidence, browser token exposure, password reuse, and post-compromise cleanup. | Credential reuse<br>New device login<br>Password reset activity<br>Unusual data access | Host review commands, account reset workflow, and detection content. |
| Repository secret exposure | ![Severity: High](https://img.shields.io/badge/Severity-High-orange) | Git history, exposed tokens, stale credentials, and unsafe config files. | Secret-like filenames<br>Token-shaped strings<br>Committed environment files<br>Suspicious workflow permissions | Repo audit scripts, rotation checklist, and pre-commit scanning guidance. |
| Suspicious PowerShell persistence | ![Severity: High](https://img.shields.io/badge/Severity-High-orange) | Scheduled tasks, services, startup entries, encoded commands, and userland persistence. | Encoded command usage<br>Unknown scheduled task<br>Unexpected service binary path<br>Run key modification | Windows inventory scripts, persistence review, and safe-disable workflows. |
| Cloud key exposure and over-permissioning | ![Severity: High](https://img.shields.io/badge/Severity-High-orange) | Access keys, IAM policies, public buckets, logging gaps, and unused privileges. | Unused access key<br>Overbroad policy<br>Public storage object<br>Missing audit trail | Cloud inventory checks, least-privilege review, and exposure reports. |
| Public surface scraping and impersonation risk | ![Severity: Medium](https://img.shields.io/badge/Severity-Medium-yellow) | Public metadata, profile visibility, brand impersonation, and exposed contact paths. | New lookalike account<br>Public metadata drift<br>Unexpected indexed asset<br>Unauthorized brand reuse | Public-surface audit tooling, reporting templates, and evidence capture. |

## Defensive Build Map

| Adversary Behavior | Telemetry | Defensive Control | Zeid Data Build |
| --- | --- | --- | --- |
| Account takeover | Authentication logs<br>Mailbox rules<br>OAuth grants<br>Device history | MFA review<br>Session revocation<br>Rule cleanup<br>Login anomaly detection | Identity incident checklist and account review scripts |
| Secret harvesting | Git history<br>Workflow files<br>Environment files<br>Token inventory | Secret scanning<br>Token rotation<br>Least-privilege review<br>Protected branches | Repository exposure audit workflow |
| Endpoint persistence | Services<br>Scheduled tasks<br>Startup folders<br>Run keys<br>PowerShell logs | Persistence inventory<br>Safe-disable process<br>Script block logging<br>Change audit | Windows cleanup and persistence review toolkit |
| Data exposure | Public assets<br>Storage permissions<br>Application logs<br>Repository metadata | Exposure inventory<br>Access review<br>Evidence capture<br>Remediation tracking | Public-surface and data exposure review workflows |

## Public Repository Feed

| Repository | Description | Language | Stars | Updated |
| --- | --- | --- | --- | --- |
| [.github](https://github.com/Zeid-Data/.github) | Zeid Data organization profile and dynamic threat intel radar | Python | 0 | 2026-05-21 |
| [dominos_source](https://github.com/Zeid-Data/dominos_source) | Python bindings for the Domino APIs | Python | 0 | 2026-05-13T13:46:20Z |

## Operating Principles

| Rule |
| --- |
| Authorized testing only. |
| Evidence before conclusions. |
| Telemetry over vibes. |
| Rollback paths before risky changes. |
| Readable outputs beat clever outputs. |

---

Last generated: `2026-05-21`

<!-- ZEID-DATA:README:END -->

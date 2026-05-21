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

## ðŸ¤– Lithium Bot Tracker

<table>
<tr>
<td width="70" align="center">ðŸ¤–</td>
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

<!-- ZD_THREAT_RADAR_START -->
_Auto-updated: `2026-05-21 19:07 UTC`_

### Current exploited vulnerability radar

Source: CISA Known Exploited Vulnerabilities catalog. Severity below is Zeid Data operational severity, not a CVSS score.

| Severity | CVE | Product | Risk class | Added | Due | Zeid Data defensive build | Rationale |
|---|---|---|---|---:|---:|---|---|
| <img alt="Critical" src="https://img.shields.io/badge/Critical-red?style=flat-square"> | `CVE-2025-34291` | Langflow Langflow | Known exploited vulnerability | `2026-05-21` | `2026-06-04` | KEV watcher item and manual validation checklist | Ransomware-linked, RCE/auth bypass, or immediate exploit priority |
| <img alt="Critical" src="https://img.shields.io/badge/Critical-red?style=flat-square"> | `CVE-2026-34926` | Trend Micro Apex One | Path traversal/file exposure | `2026-05-21` | `2026-06-04` | Route/file exposure audit, web evidence capture, remediation report | Ransomware-linked, RCE/auth bypass, or immediate exploit priority |
| <img alt="Critical" src="https://img.shields.io/badge/Critical-red?style=flat-square"> | `CVE-2008-4250` | Microsoft Windows | Memory corruption | `2026-05-20` | `2026-06-03` | Patch-priority radar and host-update validation | Ransomware-linked, RCE/auth bypass, or immediate exploit priority |
| <img alt="Critical" src="https://img.shields.io/badge/Critical-red?style=flat-square"> | `CVE-2009-1537` | Microsoft DirectX | Known exploited vulnerability | `2026-05-20` | `2026-06-03` | KEV watcher item and manual validation checklist | Ransomware-linked, RCE/auth bypass, or immediate exploit priority |
| <img alt="Critical" src="https://img.shields.io/badge/Critical-red?style=flat-square"> | `CVE-2009-3459` | Adobe Acrobat and Reader | Memory corruption | `2026-05-20` | `2026-06-03` | Patch-priority radar and host-update validation | Ransomware-linked, RCE/auth bypass, or immediate exploit priority |
| <img alt="Critical" src="https://img.shields.io/badge/Critical-red?style=flat-square"> | `CVE-2010-0249` | Microsoft Internet Explorer | Known exploited vulnerability | `2026-05-20` | `2026-06-03` | KEV watcher item and manual validation checklist | Ransomware-linked, RCE/auth bypass, or immediate exploit priority |
| <img alt="Critical" src="https://img.shields.io/badge/Critical-red?style=flat-square"> | `CVE-2010-0806` | Microsoft Internet Explorer | Known exploited vulnerability | `2026-05-20` | `2026-06-03` | KEV watcher item and manual validation checklist | Ransomware-linked, RCE/auth bypass, or immediate exploit priority |
| <img alt="Critical" src="https://img.shields.io/badge/Critical-red?style=flat-square"> | `CVE-2026-41091` | Microsoft Defender | Known exploited vulnerability | `2026-05-20` | `2026-06-03` | KEV watcher item and manual validation checklist | Ransomware-linked, RCE/auth bypass, or immediate exploit priority |

### What we’re building to reduce the pattern

| Pattern | Evidence to look for | Zeid Data build |
|---|---|---|
| Exploited CVEs | Known exploited products, missing patch evidence, internet exposure | KEV radar, exposure checks, patch validation |
| Public metadata exposure | Public profiles, account linkage, visible relationships | Authorized public visibility audit tooling |
| Windows persistence | New services, scheduled tasks, startup entries, orphan binaries | Suspicious persistence inventory and cleanup scripts |
| Detection gaps | Missing SIEM rules, weak telemetry, untested assumptions | Sigma, KQL, SPL, and Elastic detections |
| Weak evidence chain | Findings without logs, source refs, or reproducible tests | Normalized evidence records, source refs, reports, dashboards |

### Lithium build tracker

| Signal | Value |
|---|---|
| Repository | `Zeid-Data/lithium` |
| Visibility | `private` |
| Language | `mixed` |
| Default branch | `main` |
| Last push | `2026-05-21T02:52:54Z` |
| Latest commit | `935a5c2` Add Lithium README |
| Latest workflow | No workflow run visible |

### Public build tracker

| Repo | Language | Updated | Description |
|---|---:|---:|---|
| [Zeid-Data/.github](https://github.com/Zeid-Data/.github) | Python | `2026-05-21` | Zeid Data organization profile and dynamic threat intel radar |
| [Zeid-Data/dominos_source](https://github.com/Zeid-Data/dominos_source) | Python | `2026-05-17` | Python bindings for the Domino APIs |

> Threat intel is only useful when it becomes a control, a detection, a test, or a fix.
<!-- ZD_THREAT_RADAR_END -->

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


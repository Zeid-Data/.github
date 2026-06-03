<p align="center"><a href="https://github.com/zeiddata-dev"><img src="https://raw.githubusercontent.com/zeiddata-dev/Research/main/assets/banners/readme/root.png" alt="Zeid Data Research" width="100%"></a></p>

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
| Lithium | ![Status: Active build](https://img.shields.io/badge/Status-Active%20build-0f766e) | Evidence-linked analytics dashboard with normalized records and search-first review. | Validate evidence drilldowns, viewer gates, and source-linked summaries. |
| Speculum | ![Status: Active build](https://img.shields.io/badge/Status-Active%20build-0f766e) | Authorized public-surface audit utilities and security review workflows. | Expand tests, reporting, and input validation. |
| Detection Engineering | ![Status: Ongoing](https://img.shields.io/badge/Status-Ongoing-0f766e) | Sigma, KQL, SPL, and Elastic detections backed by structured indicators. | Convert repeatable incident patterns into tested detection rules. |
| Infrastructure Hardening | ![Status: Ongoing](https://img.shields.io/badge/Status-Ongoing-0f766e) | Inventory, config review, service exposure checks, and rollback-safe automation. | Keep scripts small, auditable, and evidence-producing. |

## Threat Intel Radar

<!-- ZD_THREAT_RADAR_START -->
_Auto-updated: `2026-06-03 11:36 UTC`_

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

### What we're building to reduce the pattern

| Pattern | Evidence to look for | Zeid Data build |
|---|---|---|
| Exploited CVEs | Known exploited products, missing patch evidence, internet exposure | KEV radar, exposure checks, patch validation |
| Public metadata exposure | Public profiles, account linkage, visible relationships | Authorized public visibility audit tooling |
| Windows persistence | New services, scheduled tasks, startup entries, orphan binaries | Suspicious persistence inventory and cleanup scripts |
| Detection gaps | Missing SIEM rules, weak telemetry, untested assumptions | Sigma, KQL, SPL, and Elastic detections |
| Weak evidence chain | Findings without logs, source refs, or reproducible tests | Normalized evidence records, source refs, reports, dashboards |

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
| [.github](https://github.com/Zeid-Data/.github) | Zeid Data organization profile and dynamic threat intel radar | Python | 0 | 2026-06-01 |

## Operating Principles

| Rule |
| --- |
| Authorized testing only. |
| Evidence before conclusions. |
| Telemetry over vibes. |
| Rollback paths before risky changes. |
| Readable outputs beat clever outputs. |

---

Last generated: `2026-06-03`

<!-- ZEID-DATA:README:END -->

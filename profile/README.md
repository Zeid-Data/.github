<p align="center"><a href="https://github.com/Zeid-Data"><img src="https://raw.githubusercontent.com/zeiddata-dev/Research/main/assets/banners/readme/root.png" alt="Zeid Data Research" width="100%"></a></p>

# Zeid Data Labs

![Focus: Defensive Security](https://img.shields.io/badge/Focus-Defensive%20Security-0f766e) ![Build: Evidence First](https://img.shields.io/badge/Build-Evidence%20First-111827) ![Ops: Reproducible](https://img.shields.io/badge/Ops-Reproducible-2563eb) ![Scope: Authorized Review](https://img.shields.io/badge/Scope-Authorized%20Review-7c2d12)

Defensive security engineering, detection content, public-surface review tooling, and operational data systems.

<!-- ZEID-DATA:README:BEGIN -->

## Mission

| Principle |
| --- |
| Build practical tools for authorized security review. |
| Turn evidence, logs, telemetry, and source records into measurable defensive action. |
| Keep security work reproducible, auditable, public-safe, and grounded in artifacts. |

## Active Tracks

| Track | Public output | Evidence standard |
| --- | --- | --- |
| Detection Engineering | Sigma, KQL, SPL, Elastic logic, IOC structures, validation notes | Rule, source reference, test case, or telemetry requirement |
| Threat Intel Radar | KEV watch, exploit-priority patterns, patch-validation prompts | External source link and defensive action |
| Public Surface Review | Exposure checks, repository hygiene, metadata review, safe audit workflows | Authorized target, captured finding, remediation path |
| Operational Dashboards | Evidence-first dashboards, report patterns, SOC-style workbooks | Drilldown source record or explicit evidence-missing state |
| Automation | Python, PowerShell, Bash validators and collectors | What it read, what it changed, and how to roll back |

## Lab Console

<!-- ZD_THREAT_RADAR_START -->
_Auto-updated: `2026-05-31 23:56 UTC`_

### Live Lab Status

| Signal | Current | Evidence |
|---|---|---|
| Public repos tracked | `2` | [GitHub org](https://github.com/Zeid-Data?tab=repositories) |
| Latest public ship | Expand organization README lab console generator | [commit](https://github.com/Zeid-Data/.github/commit/3785f4626968a03201f247db59c9a4b142a81178) |
| Threat radar freshness | Dynamic feed backed by CISA KEV. Next scheduled workflow refresh will verify current feed date. | [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) |
| Automation cadence | Scheduled every 6 hours plus manual dispatch | [workflow](https://github.com/Zeid-Data/.github/actions/workflows/update-threat-radar.yml) |

### Shipped This Week

| Project | Change | Evidence | Date |
|---|---|---|---:|
| [.github](https://github.com/Zeid-Data/.github) | Expand organization README lab console generator | [commit](https://github.com/Zeid-Data/.github/commit/3785f4626968a03201f247db59c9a4b142a81178) | `2026-05-31` |
| [.github](https://github.com/Zeid-Data/.github) | Refresh organization README automation workflow | [commit](https://github.com/Zeid-Data/.github/commit/fdb3eeb6ccd3e40bbe7ddac2425f4f7c0a5206e0) | `2026-05-31` |

### Current Exploited Vulnerability Radar

Source: CISA Known Exploited Vulnerabilities catalog. Severity below is Zeid Data operational severity, not a CVSS score.

| Severity | CVE | Product | Risk class | Added | Due | Defensive build | Rationale |
|---|---|---|---|---:|---:|---|---|
| <img alt="Review" src="https://img.shields.io/badge/Review-blue?style=flat-square"> | Dynamic on next workflow run | CISA KEV feed | Known exploited vulnerability | dynamic | dynamic | KEV radar, exposure checks, patch validation | This row is a safe placeholder until the scheduled workflow rewrites the radar. |

### Public Repository Feed

| Repository | Latest public signal | Build health | Updated |
|---|---|---|---:|
| [.github](https://github.com/Zeid-Data/.github) | [Expand organization README lab console generator](https://github.com/Zeid-Data/.github/commit/3785f4626968a03201f247db59c9a4b142a81178) | [Update Zeid Data lab console](https://github.com/Zeid-Data/.github/actions/workflows/update-threat-radar.yml) | `2026-05-31` |
| [dominos_source](https://github.com/Zeid-Data/dominos_source) | Python bindings for the Domino APIs | No public workflow run visible | `2026-05-17` |

### What We Build From These Signals

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

## Operating Principles

| Rule |
| --- |
| Authorized testing only. |
| Evidence before conclusions. |
| Telemetry over vibes. |
| Rollback paths before risky changes. |
| Readable outputs beat clever outputs. |
| Public front pages must not expose secrets, private logs, private messages, chat IDs, tokens, passwords, or internal-only infrastructure details. |

---

Last generated: `2026-05-31`

<!-- ZEID-DATA:README:END -->

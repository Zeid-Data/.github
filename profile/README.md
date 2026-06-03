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
| Lithium | ![Status: Running private build](https://img.shields.io/badge/Status-Running%20private%20build-0f766e) | Auth-gated React/Vite dashboard. SQLite-backed normalized evidence records. Privacy-aware evidence drilldowns. Search-first review. | Matrix/Synapse migration. Rebranded iOS client (Lithium Chat) in parallel build. |
| EQ Framework | ![Status: Active build](https://img.shields.io/badge/Status-Active%20build-0f766e) | Standalone behavioral analysis and signal processing framework. Hosted on dedicated AWS Lightsail instance (eq-dev-01). Not Lithium-specific. | Expand normalized event schema. Harden API surface. Document independently. |
| Speculum | ![Status: Active build](https://img.shields.io/badge/Status-Active%20build-0f766e) | Authorized public-surface review utilities and security audit workflows. | Expand tests, reporting, documentation, and safe input validation. |
| Detection Pipeline | ![Status: Ongoing](https://img.shields.io/badge/Status-Ongoing-0f766e) | Structured detection content and pipeline infrastructure. Sigma, KQL, SPL, Elastic. Structured indicators. Defensive validation scripts. | Convert repeatable incident patterns into tested detection content. |
| Sigma Rule Engine | ![Status: Ongoing](https://img.shields.io/badge/Status-Ongoing-0f766e) | Authoring, testing, and validating Sigma rules for cross-SIEM deployment. KQL, SPL, and Elastic translation targets. | Build validation harness. Add test coverage for new rule submissions. |
| ZD Infra Layer | ![Status: Ongoing](https://img.shields.io/badge/Status-Ongoing-0f766e) | Inventory, configuration review, service exposure checks, rollback-safe automation. AWS Lightsail. Ubuntu 24.04 LTS. DNS, VPN, hardening, segmentation. | Keep scripts small, auditable, reversible, and evidence-producing. |

## Lithium

| | Lithium |
|---|---|
| Status | ![Running private build](https://img.shields.io/badge/Lithium-Running%20private%20build-7c3aed) |
| Public boundary | Auth-gated. Unauthenticated dashboard and API requests return 401. |

## Threat Intel Radar

### Current exploited vulnerability radar

Source: CISA Known Exploited Vulnerabilities catalog. Severity below is Zeid Data operational severity, not a CVSS score.

<!-- CISA_KEV_TABLE -->

### What we're building to reduce the pattern

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
| [Zeid-Data/.github](https://github.com/Zeid-Data/.github) | Python | `2026-06-01` | Zeid Data organization profile and dynamic threat intel radar |
| [Zeid-Data/dominos_source](https://github.com/Zeid-Data/dominos_source) | Python | `2026-05-17` | Python bindings for the Domino APIs |

> Threat intel is only useful when it becomes a control, a detection, a test, or a fix.

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
| [dominos_source](https://github.com/Zeid-Data/dominos_source) | Python bindings for the Domino APIs | Python | 0 | 2026-05-17 |

## Operating Principles

| Rule |
| --- |
| Authorized testing only. |
| Evidence before conclusions. |
| Telemetry over vibes. |
| Rollback paths before risky changes. |
| Readable outputs beat clever outputs. |

---

Last generated: <!-- LAST_GENERATED -->

<!-- ZEID-DATA:README:END -->

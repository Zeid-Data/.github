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
| Lithium | ![Status: Active build](https://img.shields.io/badge/Status-Active%20build-0f766e) | Evidence-linked operational analytics, normalized records, dashboard search, and privacy-aware review flows. | Validate fresh records, searchable drilldowns, viewer gates, and source-linked summaries. |
| Speculum | ![Status: Active build](https://img.shields.io/badge/Status-Active%20build-0f766e) | Authorized public-surface review utilities and security audit workflows. | Expand tests, reporting, documentation, and safe input validation. |
| Detection Engineering | ![Status: Ongoing](https://img.shields.io/badge/Status-Ongoing-0f766e) | Sigma, KQL, SPL, Elastic, structured indicators, and defensive validation scripts. | Convert repeatable incident patterns into tested detection content. |
| Infrastructure Hardening | ![Status: Ongoing](https://img.shields.io/badge/Status-Ongoing-0f766e) | Inventory, configuration review, service exposure checks, and rollback-safe automation. | Keep scripts small, auditable, reversible, and evidence-producing. |

## 🤖 Lithium Bot Tracker

<table>
<tr>
<td width="70" align="center">🤖</td>
<td>
<strong>Lithium bot status:</strong> Active build<br>
<strong>Current read:</strong> SQLite-backed normalized evidence records<br>
<strong>Next proof:</strong> Fresh record timestamps
</td>
</tr>
</table>

| Area | Details |
| --- | --- |
| Status | ![Lithium: Active build](https://img.shields.io/badge/Lithium-Active%20build-7c3aed) |
| Current focus | SQLite-backed normalized evidence records<br>Readable relationship and operational signal dashboards<br>Search-first drilldown views<br>Viewer-aware access controls<br>Evidence references attached to every claim |
| Validation targets | Fresh record timestamps<br>Non-empty message text where expected<br>Stable profile identity mapping<br>Permission-filtered dashboard responses<br>No raw file dependency in runtime dashboard views |

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
| [.github](https://github.com/Zeid-Data/.github) | Zeid Data organization profile and dynamic threat intel radar | Python | 0 | 2026-05-17T10:43:20Z |
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

Last generated: `2026-05-18 04:45:04 UTC`

<!-- ZEID-DATA:README:END -->

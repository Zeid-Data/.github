<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=210&text=Zeid%20Data&fontAlign=50&fontAlignY=38&desc=Threat%20Intel%20Radar%20%7C%20Evidence-First%20Security%20Engineering&descAlign=50&descAlignY=62&color=gradient" alt="Zeid Data banner">
</p>

<p align="center">
  <a href="https://zeiddata.com"><img alt="Website" src="https://img.shields.io/badge/Website-zeiddata.com-00B8A9?style=for-the-badge&logo=googlechrome&logoColor=white"></a>
  <a href="https://github.com/Zeid-Data"><img alt="GitHub Org" src="https://img.shields.io/badge/GitHub-Zeid--Data-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <img alt="Mission" src="https://img.shields.io/badge/Mission-Evidence%20Before%20Claims-7B61FF?style=for-the-badge">
</p>

# Zeid Data

Security engineering, defensive automation, evidence pipelines, and detection research.

We track exploited vulnerabilities and active risk patterns, then build small defensive tools that help answer:

- Are we exposed?
- What evidence proves it?
- What can we detect?
- What can we fix?
- What changed after the fix?

> Threat intel is only useful when it turns into a control, a detection, a test, or a fix.

---

## Threat Intel Radar → What We’re Building

<!-- ZD_THREAT_RADAR_START -->
_Auto-updated: `2026-05-17 01:20 UTC`_

### Current exploited vulnerability radar

Source: CISA Known Exploited Vulnerabilities catalog. Attribution is intentionally omitted unless the source data proves it.

| CVE | Product | Risk class | Added | Due | Zeid Data defensive build | Priority |
|---|---|---|---:|---:|---|---|
| `CVE-2026-42897` | Microsoft Microsoft | Known exploited vulnerability | `2026-05-15` | `2026-05-29` | KEV watcher item and manual validation checklist | Ransomware-linked priority |
| `CVE-2026-20182` | Cisco Catalyst SD-WAN | Authentication bypass | `2026-05-14` | `2026-05-17` | Config audit, auth log review, access-path tests | Ransomware-linked priority |
| `CVE-2026-42208` | BerriAI LiteLLM | SQL injection | `2026-05-08` | `2026-05-11` | Query-pattern detections and validation fixtures | Ransomware-linked priority |
| `CVE-2026-6973` | Ivanti Endpoint Manager Mobile (EPMM) | Remote code execution | `2026-05-07` | `2026-05-10` | Exposure checks, service inventory, patch validation report | Ransomware-linked priority |
| `CVE-2026-0300` | Palo Alto Networks PAN-OS | Memory corruption | `2026-05-06` | `2026-05-09` | Patch-priority radar and host-update validation | Ransomware-linked priority |
| `CVE-2026-31431` | Linux Kernel | Remote code execution | `2026-05-01` | `2026-05-15` | Exposure checks, service inventory, patch validation report | Ransomware-linked priority |
| `CVE-2026-41940` | WebPros cPanel & WHM and WP2 (WordPress Squared) | Authentication bypass | `2026-04-30` | `2026-05-03` | Config audit, auth log review, access-path tests | Ransomware-linked priority |
| `CVE-2024-1708` | ConnectWise ScreenConnect | Path traversal/file exposure | `2026-04-28` | `2026-05-12` | Route/file exposure audit, web evidence capture, remediation report | Ransomware-linked priority |

### What we’re building to reduce the pattern

| Pattern | Evidence to look for | Zeid Data build |
|---|---|---|
| Exploited CVEs | Known exploited products, missing patch evidence, internet exposure | KEV radar, exposure checks, patch validation |
| Public metadata exposure | Public profiles, account linkage, visible relationships | Authorized public visibility audit tooling |
| Windows persistence | New services, scheduled tasks, startup entries, orphan binaries | Suspicious persistence inventory and cleanup scripts |
| Detection gaps | Missing SIEM rules, weak telemetry, untested assumptions | Sigma, KQL, SPL, and Elastic detections |
| Weak evidence chain | Findings without logs, source refs, or reproducible tests | Normalized evidence records, source refs, reports, dashboards |

### Now building

| Repo | Language | Updated | Description |
|---|---:|---:|---|
| [Zeid-Data/.github](https://github.com/Zeid-Data/.github) | mixed | `2026-05-17` | Zeid Data organization profile and dynamic threat intel radar |
| [Zeid-Data/dominos_source](https://github.com/Zeid-Data/dominos_source) | Python | `2026-05-13` | Python bindings for the Domino APIs |

> Threat intel is only useful when it becomes a control, a detection, a test, or a fix.
<!-- ZD_THREAT_RADAR_END -->

---

## Defensive build map

| Threat pattern | What attackers abuse | What we build |
|---|---|---|
| Exploited CVEs | Unpatched internet-facing software | KEV radar, exposure checks, patch validation |
| Public metadata exposure | Public profiles, account linkage, visible relationships | Authorized public visibility audit tooling |
| Windows persistence | Services, scheduled tasks, startup entries, orphan binaries | Suspicious persistence inventory and cleanup scripts |
| Detection gaps | Missing SIEM rules and weak telemetry | Sigma, KQL, SPL, and Elastic detections |
| Weak reporting | Claims without logs or source refs | Evidence-first reports and dashboards |

---

## Operating rules

- Evidence first.
- Authorized and defensive by default.
- No secrets, private logs, credential material, or personal data in public repos.
- Claims need artifacts, telemetry, references, or reproducible commands.
- Automation must show what it read, what it changed, and what proves it worked.

---

<p align="center">
  <sub>Built for receipts, not vibes.</sub>
</p>

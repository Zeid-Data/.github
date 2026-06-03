#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

OWNER = os.getenv("ZD_OWNER", "Zeid-Data")
README_PATH = Path(os.getenv("ZD_README_PATH", "profile/README.md"))
KEV_LIMIT = int(os.getenv("ZD_KEV_LIMIT", "8"))
REPO_LIMIT = int(os.getenv("ZD_REPO_LIMIT", "6"))

START = "<!-- ZD_THREAT_RADAR_START -->"
END = "<!-- ZD_THREAT_RADAR_END -->"

CISA_KEV_JSON = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
GITHUB_API = "https://api.github.com"


def fetch_json(url: str, token: str | None = None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json, application/json",
        "User-Agent": "zeid-data-threat-radar-profile-updater",
    }
    if token and url.startswith(GITHUB_API):
        headers["Authorization"] = f"Bearer {token}"
        headers["X-GitHub-Api-Version"] = "2022-11-28"

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def safe_fetch(url: str, token: str | None = None, default: Any = None) -> Any:
    try:
        return fetch_json(url, token)
    except urllib.error.HTTPError as exc:
        print(f"[WARN] HTTP {exc.code}: {url}", file=sys.stderr)
        return default
    except Exception as exc:
        print(f"[WARN] fetch failed: {url}: {exc}", file=sys.stderr)
        return default


def clean(value: Any, default: str = "") -> str:
    text = default if value is None else str(value)
    text = text.replace("\n", " ").replace("\r", " ").replace("|", "\\|").strip()
    return re.sub(r"\s+", " ", text)


def short(value: Any, default: str = "", limit: int = 130) -> str:
    text = clean(value, default)
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def badge(label: str, color: str) -> str:
    label_safe = clean(label).replace("-", "--").replace(" ", "%20")
    return f'<img alt="{clean(label)}" src="https://img.shields.io/badge/{label_safe}-{color}?style=flat-square">'


def latest_kev() -> list[dict[str, Any]]:
    data = safe_fetch(CISA_KEV_JSON, default={})
    vulns = data.get("vulnerabilities", []) if isinstance(data, dict) else []
    return sorted(vulns, key=lambda x: x.get("dateAdded") or "0000-00-00", reverse=True)[:KEV_LIMIT]


def public_repos() -> list[dict[str, Any]]:
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    url = f"{GITHUB_API}/orgs/{OWNER}/repos?type=public&sort=pushed&direction=desc&per_page={REPO_LIMIT}"
    repos = safe_fetch(url, token, default=[])
    return repos if isinstance(repos, list) else []


def classify(item: dict[str, Any]) -> tuple[str, str]:
    text = " ".join(
        clean(item.get(k))
        for k in ("vulnerabilityName", "shortDescription", "requiredAction", "product", "vendorProject")
    ).lower()

    if any(x in text for x in ("remote code execution", "rce", "code execution")):
        return "Remote code execution", "Exposure checks, service inventory, patch validation report"
    if any(x in text for x in ("authentication bypass", "auth bypass", "improper authentication")):
        return "Authentication bypass", "Config audit, auth log review, access-path tests"
    if any(x in text for x in ("privilege escalation", "elevation of privilege")):
        return "Privilege escalation", "Windows persistence inventory, host hardening checks, SIEM rules"
    if "command injection" in text:
        return "Command injection", "HTTP log triage, child-process detections, validation fixtures"
    if any(x in text for x in ("path traversal", "directory traversal", "file inclusion")):
        return "Path traversal/file exposure", "Route/file exposure audit, web evidence capture, remediation report"
    if "sql injection" in text:
        return "SQL injection", "Query-pattern detections and validation fixtures"
    if any(x in text for x in ("use after free", "memory corruption", "buffer overflow", "out-of-bounds")):
        return "Memory corruption", "Patch-priority radar and host-update validation"
    if any(x in text for x in ("cross-site scripting", "xss")):
        return "Cross-site scripting", "Web hygiene checks, CSP review, validation fixtures"

    return "Known exploited vulnerability", "KEV watcher item and manual validation checklist"


def operational_severity(item: dict[str, Any], risk_class: str) -> tuple[str, str, str]:
    ransomware = clean(item.get("knownRansomwareCampaignUse"), "Unknown").lower()
    due = clean(item.get("dueDate"))

    past_due = False
    if due:
        try:
            past_due = dt.date.fromisoformat(due[:10]) <= dt.datetime.now(dt.UTC).date()
        except ValueError:
            past_due = False

    if "known" in ransomware or risk_class in {"Remote code execution", "Authentication bypass"}:
        return "Critical", "red", "Ransomware-linked, RCE/auth bypass, or immediate exploit priority"
    if past_due or risk_class in {"Privilege escalation", "Command injection", "SQL injection", "Memory corruption"}:
        return "High", "orange", "Past due or high-impact exploit class"
    if risk_class in {"Path traversal/file exposure", "Cross-site scripting"}:
        return "Medium", "yellow", "Exposure or web abuse class"
    return "Review", "blue", "Known exploited, needs product exposure validation"


def render() -> str:
    now = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = []

    lines.append(f"_Auto-updated: `{now}`_")
    lines.append("")
    lines.append("### Current exploited vulnerability radar")
    lines.append("")
    lines.append("Source: CISA Known Exploited Vulnerabilities catalog. Severity below is Zeid Data operational severity, not a CVSS score.")
    lines.append("")
    lines.append("| Severity | CVE | Product | Risk class | Added | Due | Zeid Data defensive build | Rationale |")
    lines.append("|---|---|---|---|---:|---:|---|---|")

    kev_rows = latest_kev()
    if not kev_rows:
        lines.append(f"| {badge('Review', 'blue')} | KEV fetch unavailable | n/a | n/a | n/a | n/a | Check workflow logs and network access | Feed unavailable |")
    else:
        for item in kev_rows:
            cve = clean(item.get("cveID"), "unknown")
            product = f"{clean(item.get('vendorProject'), 'Unknown vendor')} {clean(item.get('product'), 'Unknown product')}"
            risk, build = classify(item)
            sev, color, rationale = operational_severity(item, risk)
            added = clean(item.get("dateAdded"), "unknown")
            due = clean(item.get("dueDate"), "n/a")
            lines.append(f"| {badge(sev, color)} | `{cve}` | {product} | {risk} | `{added}` | `{due}` | {build} | {rationale} |")

    lines.append("")
    lines.append("### What we're building to reduce the pattern")
    lines.append("")
    lines.append("| Pattern | Evidence to look for | Zeid Data build |")
    lines.append("|---|---|---|")
    lines.append("| Exploited CVEs | Known exploited products, missing patch evidence, internet exposure | KEV radar, exposure checks, patch validation |")
    lines.append("| Public metadata exposure | Public profiles, account linkage, visible relationships | Authorized public visibility audit tooling |")
    lines.append("| Windows persistence | New services, scheduled tasks, startup entries, orphan binaries | Suspicious persistence inventory and cleanup scripts |")
    lines.append("| Detection gaps | Missing SIEM rules, weak telemetry, untested assumptions | Sigma, KQL, SPL, and Elastic detections |")
    lines.append("| Weak evidence chain | Findings without logs, source refs, or reproducible tests | Normalized evidence records, source refs, reports, dashboards |")
    lines.append("")
    lines.append("> Threat intel is only useful when it becomes a control, a detection, a test, or a fix.")
    return "\n".join(lines)


def main() -> int:
    if not README_PATH.exists():
        print(f"[FAIL] missing README: {README_PATH}", file=sys.stderr)
        return 2

    original = README_PATH.read_text(encoding="utf-8")
    if START not in original or END not in original:
        print("[FAIL] README missing dynamic markers", file=sys.stderr)
        return 3

    updated = original.split(START, 1)[0] + START + "\n" + render() + "\n" + END + original.split(END, 1)[1]
    README_PATH.write_text(updated, encoding="utf-8")
    print(f"[PASS] updated {README_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

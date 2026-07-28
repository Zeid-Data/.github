#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import os
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
SOURCE_BANNER_MARKDOWN = (
    '<p align="center">'
    '<a href="https://github.com/zeiddata-dev">'
    '<img src="https://raw.githubusercontent.com/zeiddata-dev/Research/main/assets/banners/readme/root.gif" '
    'alt="Zeid Data Research" width="100%">'
    '</a>'
    '</p>'
)
RADAR_START = "<!-- ZD_THREAT_RADAR_START -->"
RADAR_END = "<!-- ZD_THREAT_RADAR_END -->"
def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit("[FAIL] not inside a git repository")
    return Path(result.stdout.strip()).resolve()
ROOT = repo_root()
DEFAULT_README = ROOT / "profile" / "README.md"
NOW_BUILDING = ROOT / "data" / "now_building.json"
DEFENSIVE_MAP = ROOT / "data" / "defensive_build_map.json"
def require_expected_repo() -> None:
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    remote = result.stdout.strip()
    valid = (
        "github.com/Zeid-Data/.github" in remote
        or "github.com:Zeid-Data/.github" in remote
    )
    if not valid:
        print(f"[FAIL] wrong repo remote: {remote}")
        print("[EXPECTED] https://github.com/Zeid-Data/.github.git")
        raise SystemExit(1)
def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data
def quote_badge(value: Any) -> str:
    text = str(value).replace("-", "--")
    return urllib.parse.quote(text, safe="")
def badge(label: str, message: str, color: str) -> str:
    alt = f"{label}: {message}"
    return f"![{alt}](https://img.shields.io/badge/{quote_badge(label)}-{quote_badge(message)}-{quote_badge(color)})"
def clean_cell(value: Any) -> str:
    if isinstance(value, list):
        return "<br>".join(clean_cell(item) for item in value)
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", "<br>").strip()
def table(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows:
        rows = [["No records available."] + [""] * (len(headers) - 1)]
    out = [
        "| " + " | ".join(clean_cell(h) for h in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        padded = list(row) + [""] * max(0, len(headers) - len(row))
        out.append("| " + " | ".join(clean_cell(v) for v in padded[:len(headers)]) + " |")
    return "\n".join(out)
def request_json(url: str, token: str | None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "zeid-data-profile-updater",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))
def fetch_public_repos(owner: str, owner_type: str, token: str | None, offline: bool) -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    if offline:
        return [], ["offline mode enabled"]
    repos: list[dict[str, Any]] = []
    for page in range(1, 6):
        url = f"https://api.github.com/{owner_type}/{urllib.parse.quote(owner)}/repos?type=public&sort=updated&per_page=100&page={page}"
        try:
            payload = request_json(url, token)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
            warnings.append(f"repository feed unavailable: {exc.__class__.__name__}")
            break
        if not isinstance(payload, list) or not payload:
            break
        repos.extend(item for item in payload if isinstance(item, dict))
    repos.sort(key=lambda item: str(item.get("updated_at") or ""), reverse=True)
    return repos, warnings
def repo_rows(repos: list[dict[str, Any]], warnings: list[str]) -> list[list[Any]]:
    rows: list[list[Any]] = []
    for repo in repos:
        name = repo.get("name") or "unknown"
        url = repo.get("html_url") or ""
        description = repo.get("description") or "No description set."
        language = repo.get("language") or "Mixed"
        updated = repo.get("updated_at") or "unknown"
        stars = repo.get("stargazers_count", 0)
        name_cell = f"[{clean_cell(name)}]({url})" if isinstance(url, str) and url.startswith("https://") else clean_cell(name)
        rows.append([name_cell, description, language, stars, updated])
    if not rows and warnings:
        rows.append(["Repository feed", "Unavailable in this run.", "N/A", "N/A", "; ".join(warnings)])
    return rows
def build_readme(now: dict[str, Any], defensive: dict[str, Any], repos: list[dict[str, Any]], warnings: list[str], existing_radar: str = "") -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    organization = str(now.get("organization") or "Zeid Data")
    tagline = str(now.get("tagline") or "Defensive security engineering.")
    mission_rows = [[item] for item in now.get("mission", []) if str(item).strip()]
    building_rows = [
        [item.get("track"), badge("Status", item.get("status", "Unknown"), "0f766e"), item.get("focus"), item.get("next")]
        for item in now.get("now_building", [])
        if isinstance(item, dict)
    ]
    build_rows = []
    for item in defensive.get("build_map", []):
        if not isinstance(item, dict):
            continue
        build_rows.append([
            item.get("adversary_behavior"),
            item.get("telemetry", []),
            item.get("defensive_control", []),
            item.get("zeid_build"),
        ])
    principle_rows = [[item] for item in now.get("operating_principles", []) if str(item).strip()]
    warning_line = ""
    if warnings:
        warning_line = "\n> Repository metadata note: " + "; ".join(clean_cell(w) for w in warnings) + "\n"
    radar_content = existing_radar.strip() if existing_radar.strip() else "_Refreshes every 6 hours with latest CISA KEV data._"
    return f"""{SOURCE_BANNER_MARKDOWN}
# {organization}
{badge("Focus", "Defensive Security", "0f766e")} {badge("Build", "Evidence First", "111827")} {badge("Ops", "Reproducible", "2563eb")} {badge("Scope", "Authorized Review", "7c2d12")}
{tagline}

Maintained by **[zeiddata-dev](https://github.com/zeiddata-dev)**. Original tooling, detections, and research live there.
<!-- ZEID-DATA:README:BEGIN -->
## Mission
{table(["Principle"], mission_rows)}
## Now Building
{table(["Track", "Status", "Focus", "Next"], building_rows)}
## Threat Intel Radar
{RADAR_START}
{radar_content}
{RADAR_END}
## Defensive Build Map
{table(["Adversary Behavior", "Telemetry", "Defensive Control", "Zeid Data Build"], build_rows)}
## Public Repository Feed
{table(["Repository", "Description", "Language", "Stars", "Updated"], repo_rows(repos, warnings))}
{warning_line}
## Operating Principles
{table(["Rule"], principle_rows)}
---
Last generated: `{generated_at}`
<!-- ZEID-DATA:README:END -->
"""
def extract_links(markdown: str) -> list[str]:
    links: set[str] = set()
    for match in re.finditer(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", markdown):
        links.add(match.group(1).strip())
    for match in re.finditer(r"""(?:href|src)=["']([^"']+)["']""", markdown, flags=re.IGNORECASE):
        links.add(match.group(1).strip())
    return sorted(link for link in links if link)
def check_external_url(url: str) -> tuple[bool, str]:
    parsed = urllib.parse.urlsplit(url)
    clean_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, ""))
    headers = {
        "User-Agent": "zeid-data-profile-link-checker",
        "Accept": "*/*",
    }
    errors:

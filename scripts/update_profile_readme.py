#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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


def severity_color(severity: str) -> str:
    lookup = {
        "critical": "red",
        "high": "orange",
        "medium": "yellow",
        "low": "blue",
        "info": "lightgrey"
    }
    return lookup.get(str(severity).strip().lower(), "lightgrey")


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
        "| " + " | ".join("---" for _ in headers) + " |"
    ]
    for row in rows:
        padded = list(row) + [""] * max(0, len(headers) - len(row))
        out.append("| " + " | ".join(clean_cell(v) for v in padded[:len(headers)]) + " |")
    return "\n".join(out)


def request_json(url: str, token: str | None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "zeid-data-profile-updater"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_org_repos(org: str, token: str | None, offline: bool) -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    if offline:
        return [], ["offline mode enabled"]

    repos: list[dict[str, Any]] = []
    for page in range(1, 6):
        url = f"https://api.github.com/orgs/{urllib.parse.quote(org)}/repos?type=public&sort=updated&per_page=100&page={page}"
        try:
            payload = request_json(url, token)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
            warnings.append(f"repository feed unavailable: {exc.__class__.__name__}")
            break
        if not isinstance(payload, list) or not payload:
            break
        repos.extend(item for item in payload if isinstance(item, dict))

    repos.sort(key=lambda item: str(item.get("updated_at") or ""), reverse=True)
    return repos[:8], warnings


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


def build_readme(now: dict[str, Any], defensive: dict[str, Any], repos: list[dict[str, Any]], warnings: list[str]) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    organization = str(now.get("organization") or "Zeid Data")
    tagline = str(now.get("tagline") or "Defensive security engineering.")

    mission_rows = [[item] for item in now.get("mission", []) if str(item).strip()]
    building_rows = [
        [item.get("track"), badge("Status", item.get("status", "Unknown"), "0f766e"), item.get("focus"), item.get("next")]
        for item in now.get("now_building", [])
        if isinstance(item, dict)
    ]

    lithium = now.get("lithium_tracker", {})
    if not isinstance(lithium, dict):
        lithium = {}

    lithium_rows = [
        ["Status", badge("Lithium", lithium.get("status", "Unknown"), "7c3aed")],
        ["Current focus", lithium.get("current_focus", [])],
        ["Validation targets", lithium.get("validation_targets", [])]
    ]

    radar_rows = []
    for item in defensive.get("radar", []):
        if not isinstance(item, dict):
            continue
        severity = str(item.get("severity") or "Info")
        radar_rows.append([
            item.get("pattern"),
            badge("Severity", severity, severity_color(severity)),
            item.get("defender_focus"),
            item.get("signals", []),
            item.get("build_response")
        ])

    build_rows = []
    for item in defensive.get("build_map", []):
        if not isinstance(item, dict):
            continue
        build_rows.append([
            item.get("adversary_behavior"),
            item.get("telemetry", []),
            item.get("defensive_control", []),
            item.get("zeid_build")
        ])

    principle_rows = [[item] for item in now.get("operating_principles", []) if str(item).strip()]
    warning_line = ""
    if warnings:
        warning_line = "\n> Repository metadata note: " + "; ".join(clean_cell(w) for w in warnings) + "\n"

    return f"""# {organization}

{badge("Focus", "Defensive Security", "0f766e")} {badge("Build", "Evidence First", "111827")} {badge("Ops", "Reproducible", "2563eb")} {badge("Scope", "Authorized Review", "7c2d12")}

{tagline}

<!-- ZEID-DATA:README:BEGIN -->

## Mission

{table(["Principle"], mission_rows)}

## Now Building

{table(["Track", "Status", "Focus", "Next"], building_rows)}

## Lithium Build Tracker

{table(["Area", "Details"], lithium_rows)}

## Threat Intel Radar

{table(["Pattern", "Severity", "Defender Focus", "Signals", "Build Response"], radar_rows)}

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


def main() -> int:
    parser = argparse.ArgumentParser(description="Update the Zeid Data organization profile README.")
    parser.add_argument("--org", default=os.environ.get("GITHUB_ORG", "Zeid-Data"))
    parser.add_argument("--readme", default=str(DEFAULT_README))
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()

    require_expected_repo()

    readme_path = Path(args.readme)
    if not readme_path.is_absolute():
        readme_path = ROOT / readme_path

    now = load_json(NOW_BUILDING)
    defensive = load_json(DEFENSIVE_MAP)
    repos, warnings = fetch_org_repos(args.org, os.environ.get("GITHUB_TOKEN"), args.offline)

    content = build_readme(now, defensive, repos, warnings)
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    readme_path.write_text(content, encoding="utf-8")

    print(f"root={ROOT}")
    print(f"wrote={readme_path.relative_to(ROOT)}")
    print(f"repos={len(repos)}")
    if warnings:
        print("warnings=" + "; ".join(warnings))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

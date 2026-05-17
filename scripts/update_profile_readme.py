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
    '<img src="https://raw.githubusercontent.com/zeiddata-dev/Research/main/assets/banners/readme/root.png" '
    'alt="Zeid Data Research" width="100%">'
    '</a>'
    '</p>'
)


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
        "info": "lightgrey",
    }
    return lookup.get(str(severity).strip().lower(), "lightgrey")


def clean_cell(value: Any) -> str:
    if isinstance(value, list):
        return "<br>".join(clean_cell(item) for item in value)
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", "<br>").strip()


def first_list_item(value: Any, fallback: str) -> str:
    if isinstance(value, list) and value:
        return clean_cell(value[0])
    if isinstance(value, str) and value.strip():
        return clean_cell(value)
    return fallback


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


def lithium_robot_panel(lithium: dict[str, Any]) -> str:
    status = clean_cell(lithium.get("status", "Unknown"))
    focus = first_list_item(lithium.get("current_focus"), "No current focus listed.")
    validation = first_list_item(lithium.get("validation_targets"), "No validation target listed.")

    return f"""<table>
<tr>
<td width="70" align="center">🤖</td>
<td>
<strong>Lithium bot status:</strong> {status}<br>
<strong>Current read:</strong> {focus}<br>
<strong>Next proof:</strong> {validation}
</td>
</tr>
</table>"""


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
        ["Validation targets", lithium.get("validation_targets", [])],
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
            item.get("build_response"),
        ])

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

    return f"""{SOURCE_BANNER_MARKDOWN}

# {organization}

{badge("Focus", "Defensive Security", "0f766e")} {badge("Build", "Evidence First", "111827")} {badge("Ops", "Reproducible", "2563eb")} {badge("Scope", "Authorized Review", "7c2d12")}

{tagline}

<!-- ZEID-DATA:README:BEGIN -->

## Mission

{table(["Principle"], mission_rows)}

## Now Building

{table(["Track", "Status", "Focus", "Next"], building_rows)}

## 🤖 Lithium Bot Tracker

{lithium_robot_panel(lithium)}

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

    errors: list[str] = []
    for method in ("HEAD", "GET"):
        try:
            request = urllib.request.Request(clean_url, headers=headers, method=method)
            with urllib.request.urlopen(request, timeout=20) as response:
                status = getattr(response, "status", 200)
                if 200 <= status < 400:
                    return True, f"{status}"
                errors.append(f"{method}:{status}")
        except urllib.error.HTTPError as exc:
            if 200 <= exc.code < 400:
                return True, f"{exc.code}"
            errors.append(f"{method}:{exc.code}")
        except Exception as exc:
            errors.append(f"{method}:{exc.__class__.__name__}")

    return False, ";".join(errors)


def link_resolves(link: str, root: Path) -> tuple[bool, str]:
    if not link:
        return False, "empty"

    if link.startswith("#"):
        return True, "anchor"

    parsed = urllib.parse.urlsplit(link)

    if parsed.scheme in {"http", "https"}:
        return check_external_url(link)

    if parsed.scheme == "mailto":
        return True, "mailto"

    local_path = link.split("#", 1)[0]
    candidate = (root / local_path).resolve()

    try:
        candidate.relative_to(root)
    except ValueError:
        return False, "outside_repo"

    if candidate.exists():
        return True, "local"

    return False, "missing_local"


def unresolved_links(markdown: str, root: Path) -> list[str]:
    failures: list[str] = []
    for link in extract_links(markdown):
        ok, detail = link_resolves(link, root)
        if ok:
            print(f"PASS {detail} {link}")
        else:
            print(f"FAIL {detail} {link}")
            failures.append(link)
    return failures


def kill_bad_hrefs_and_sources(markdown: str, root: Path) -> str:
    changed = markdown

    html_href_pattern = re.compile(
        r"""<a\b([^>]*?)\s+href=["']([^"']+)["']([^>]*)>(.*?)</a>""",
        flags=re.IGNORECASE | re.DOTALL,
    )

    def replace_html_anchor(match: re.Match[str]) -> str:
        href = match.group(2).strip()
        body = match.group(4)
        ok, detail = link_resolves(href, root)
        if ok:
            return match.group(0)
        print(f"KILL href {detail} {href}")
        return body

    changed = html_href_pattern.sub(replace_html_anchor, changed)

    html_img_pattern = re.compile(
        r"""<img\b[^>]*?\s+src=["']([^"']+)["'][^>]*?>""",
        flags=re.IGNORECASE | re.DOTALL,
    )

    def replace_html_img(match: re.Match[str]) -> str:
        src = match.group(1).strip()
        ok, detail = link_resolves(src, root)
        if ok:
            return match.group(0)
        print(f"KILL img {detail} {src}")
        return ""

    changed = html_img_pattern.sub(replace_html_img, changed)

    markdown_link_pattern = re.compile(r"""(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+"[^"]*")?\)""")

    def replace_markdown_link(match: re.Match[str]) -> str:
        label = match.group(1)
        href = match.group(2).strip()
        ok, detail = link_resolves(href, root)
        if ok:
            return match.group(0)
        print(f"KILL markdown_href {detail} {href}")
        return label

    changed = markdown_link_pattern.sub(replace_markdown_link, changed)

    markdown_img_pattern = re.compile(r"""!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)""")

    def replace_markdown_img(match: re.Match[str]) -> str:
        src = match.group(2).strip()
        ok, detail = link_resolves(src, root)
        if ok:
            return match.group(0)
        print(f"KILL markdown_img {detail} {src}")
        return ""

    changed = markdown_img_pattern.sub(replace_markdown_img, changed)

    return changed


def validate_links(markdown: str, root: Path) -> None:
    links = extract_links(markdown)
    if not links:
        raise SystemExit("[FAIL] no links found to validate")

    print("[LINK CHECK]")
    failures = unresolved_links(markdown, root)

    if failures:
        print("[FAIL] unresolved links:")
        for item in failures:
            print(item)
        raise SystemExit(1)

    print(f"PASS checked_links={len(links)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Update the Zeid Data organization profile README.")
    parser.add_argument("--org", default=os.environ.get("GITHUB_ORG", "Zeid-Data"))
    parser.add_argument("--readme", default=str(DEFAULT_README))
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--check-links", action="store_true")
    args = parser.parse_args()

    require_expected_repo()

    readme_path = Path(args.readme)
    if not readme_path.is_absolute():
        readme_path = ROOT / readme_path

    now = load_json(NOW_BUILDING)
    defensive = load_json(DEFENSIVE_MAP)
    repos, warnings = fetch_org_repos(args.org, os.environ.get("GITHUB_TOKEN"), args.offline)

    content = build_readme(now, defensive, repos, warnings)
    content = kill_bad_hrefs_and_sources(content, ROOT)

    readme_path.parent.mkdir(parents=True, exist_ok=True)
    readme_path.write_text(content, encoding="utf-8")

    print(f"root={ROOT}")
    print(f"wrote={readme_path.relative_to(ROOT)}")
    print(f"repos={len(repos)}")
    if warnings:
        print("warnings=" + "; ".join(warnings))

    if args.check_links:
        validate_links(content, ROOT)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

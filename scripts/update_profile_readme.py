#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request
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
LITHIUM_STATUS = ROOT / "data" / "lithium_status.json"
LITHIUM_ASSET_DIR = ROOT / "assets" / "lithium"


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


def clamp_percent(value: Any) -> int:
    try:
        number = int(value)
    except Exception:
        number = 0
    return max(0, min(100, number))


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


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


def severity_color_word(severity: str) -> str:
    lookup = {
        "critical": "Critical",
        "high": "High",
        "medium": "Medium",
        "low": "Low",
        "info": "Info",
    }
    return lookup.get(str(severity).strip().lower(), "Info")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def generate_button_svg(status: dict[str, Any]) -> None:
    text = str(status.get("button_text", "Open Lithium Bot Tracker"))
    percent = clamp_percent(status.get("overall_percent", 0))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="82" viewBox="0 0 520 82" role="img" aria-label="{esc(text)}">
  <defs>
    <linearGradient id="bg" x1="0" x2="1">
      <stop offset="0" stop-color="#0f172a"/>
      <stop offset="1" stop-color="#312e81"/>
    </linearGradient>
    <linearGradient id="bar" x1="0" x2="1">
      <stop offset="0" stop-color="#22c55e"/>
      <stop offset="1" stop-color="#38bdf8"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="518" height="80" rx="18" fill="url(#bg)" stroke="#38bdf8" stroke-width="2"/>
  <text x="30" y="34" fill="#e0f2fe" font-family="Segoe UI, Arial, sans-serif" font-size="21" font-weight="700">{esc(text)}</text>
  <text x="30" y="58" fill="#a7f3d0" font-family="Segoe UI, Arial, sans-serif" font-size="15">Static status: {percent}% operational</text>
  <text x="455" y="52" fill="#e0f2fe" font-family="Segoe UI Emoji, Segoe UI, Arial, sans-serif" font-size="34">🤖</text>
  <rect x="265" y="52" width="150" height="9" rx="5" fill="#1e293b"/>
  <rect x="265" y="52" width="{int(150 * percent / 100)}" height="9" rx="5" fill="url(#bar)"/>
</svg>
'''
    write_text(LITHIUM_ASSET_DIR / "lithium-tracker-button.svg", svg)


def generate_robot_svg(status: dict[str, Any]) -> None:
    percent = clamp_percent(status.get("overall_percent", 0))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120" role="img" aria-label="Lithium bot status robot">
  <defs>
    <linearGradient id="face" x1="0" x2="1">
      <stop offset="0" stop-color="#0ea5e9"/>
      <stop offset="1" stop-color="#7c3aed"/>
    </linearGradient>
  </defs>
  <rect x="23" y="31" width="74" height="58" rx="16" fill="#020617" stroke="url(#face)" stroke-width="4"/>
  <rect x="38" y="48" width="14" height="14" rx="7" fill="#67e8f9"/>
  <rect x="68" y="48" width="14" height="14" rx="7" fill="#67e8f9"/>
  <path d="M42 73 Q60 84 78 73" fill="none" stroke="#a7f3d0" stroke-width="4" stroke-linecap="round"/>
  <path d="M60 31 V18" stroke="#38bdf8" stroke-width="4" stroke-linecap="round"/>
  <circle cx="60" cy="15" r="6" fill="#22c55e"/>
  <text x="60" y="108" text-anchor="middle" fill="#e0f2fe" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="700">{percent}%</text>
</svg>
'''
    write_text(LITHIUM_ASSET_DIR / "lithium-bot.svg", svg)


def generate_progress_svg(status: dict[str, Any]) -> None:
    categories = status.get("categories", [])
    if not isinstance(categories, list):
        categories = []

    width = 900
    row_h = 54
    height = 88 + max(1, len(categories)) * row_h
    rows = []

    for i, item in enumerate(categories):
        if not isinstance(item, dict):
            continue
        y = 76 + i * row_h
        name = esc(item.get("name", "Unknown"))
        label = esc(item.get("status", "Unknown"))
        percent = clamp_percent(item.get("percent", 0))
        bar_w = int(500 * percent / 100)
        rows.append(f'''
  <text x="36" y="{y + 22}" fill="#e5e7eb" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="600">{name}</text>
  <text x="300" y="{y + 22}" fill="#c4b5fd" font-family="Segoe UI, Arial, sans-serif" font-size="15">{label}</text>
  <rect x="390" y="{y + 5}" width="500" height="22" rx="11" fill="#1e293b"/>
  <rect x="390" y="{y + 5}" width="{bar_w}" height="22" rx="11" fill="#22c55e"/>
  <text x="650" y="{y + 22}" text-anchor="middle" fill="#020617" font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="800">{percent}%</text>
''')

    overall = clamp_percent(status.get("overall_percent", 0))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Lithium Bot progress chart">
  <defs>
    <linearGradient id="panel" x1="0" x2="1">
      <stop offset="0" stop-color="#020617"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="22" fill="url(#panel)" stroke="#334155" stroke-width="2"/>
  <text x="36" y="42" fill="#e0f2fe" font-family="Segoe UI, Arial, sans-serif" font-size="25" font-weight="800">Lithium Bot Static Build Status</text>
  <text x="820" y="42" text-anchor="end" fill="#a7f3d0" font-family="Segoe UI, Arial, sans-serif" font-size="24" font-weight="800">{overall}%</text>
  {''.join(rows)}
</svg>
'''
    write_text(LITHIUM_ASSET_DIR / "lithium-progress.svg", svg)


def generate_assets(status: dict[str, Any]) -> None:
    LITHIUM_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    generate_button_svg(status)
    generate_robot_svg(status)
    generate_progress_svg(status)


def lithium_section(status: dict[str, Any]) -> str:
    percent = clamp_percent(status.get("overall_percent", 0))
    categories = status.get("categories", [])
    if not isinstance(categories, list):
        categories = []

    rows = []
    for item in categories:
        if isinstance(item, dict):
            rows.append([
                item.get("name", "Unknown"),
                item.get("status", "Unknown"),
                str(clamp_percent(item.get("percent", 0))) + "%"
            ])

    return f'''<p align="center">
  <a href="#-lithium-bot-tracker">
    <img src="assets/lithium/lithium-tracker-button.svg" alt="Open Lithium Bot Tracker" width="520">
  </a>
</p>

## 🤖 Lithium Bot Tracker

<table>
<tr>
<td width="90" align="center">
<img src="assets/lithium/lithium-bot.svg" alt="Lithium bot status robot" width="76">
</td>
<td>
<strong>Overall build state:</strong> {percent}% operational<br>
<strong>Status:</strong> {clean_cell(status.get("status", "Static build status"))}<br>
<strong>Current focus:</strong> {clean_cell(status.get("current_focus", ""))}<br>
<strong>Next proof:</strong> {clean_cell(status.get("next_proof", ""))}
</td>
</tr>
</table>

<p align="center">
  <img src="assets/lithium/lithium-progress.svg" alt="Lithium Bot progress chart" width="760">
</p>

{table(["Area", "Status", "Progress"], rows)}

'''


def build_readme(now: dict[str, Any], defensive: dict[str, Any], status: dict[str, Any]) -> str:
    organization = str(now.get("organization") or "Zeid Data")
    tagline = str(now.get("tagline") or "Defensive security engineering.")

    mission_rows = [[item] for item in now.get("mission", []) if str(item).strip()]
    building_rows = [
        [item.get("track"), item.get("status"), item.get("focus"), item.get("next")]
        for item in now.get("now_building", [])
        if isinstance(item, dict)
    ]

    radar_rows = []
    for item in defensive.get("radar", []):
        if isinstance(item, dict):
            radar_rows.append([
                item.get("pattern"),
                severity_color_word(str(item.get("severity") or "Info")),
                item.get("defender_focus"),
                item.get("signals", []),
                item.get("build_response"),
            ])

    build_rows = []
    for item in defensive.get("build_map", []):
        if isinstance(item, dict):
            build_rows.append([
                item.get("adversary_behavior"),
                item.get("telemetry", []),
                item.get("defensive_control", []),
                item.get("zeid_build"),
            ])

    principle_rows = [[item] for item in now.get("operating_principles", []) if str(item).strip()]

    return f'''# {organization}

{tagline}

<!-- ZEID-DATA:README:BEGIN -->

## Mission

{table(["Principle"], mission_rows)}

## Now Building

{table(["Track", "Status", "Focus", "Next"], building_rows)}

{lithium_section(status)}
## Threat Intel Radar

{table(["Pattern", "Severity", "Defender Focus", "Signals", "Build Response"], radar_rows)}

## Defensive Build Map

{table(["Adversary Behavior", "Telemetry", "Defensive Control", "Zeid Data Build"], build_rows)}

## Operating Principles

{table(["Rule"], principle_rows)}

<!-- ZEID-DATA:README:END -->
'''


def extract_links(markdown: str) -> list[str]:
    links: set[str] = set()
    for match in re.finditer(r'!?\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)', markdown):
        links.add(match.group(1).strip())
    for match in re.finditer(r'(?:href|src)=["\']([^"\']+)["\']', markdown, flags=re.IGNORECASE):
        links.add(match.group(1).strip())
    return sorted(link for link in links if link)


def local_anchor_exists(markdown: str, anchor: str) -> bool:
    if anchor == "#-lithium-bot-tracker":
        return "## 🤖 Lithium Bot Tracker" in markdown
    if anchor.startswith("#"):
        return True
    return False


def check_external_url(url: str) -> tuple[bool, str]:
    parsed = urllib.parse.urlsplit(url)
    clean_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, ""))

    for method in ("HEAD", "GET"):
        try:
            request = urllib.request.Request(
                clean_url,
                headers={"User-Agent": "zeid-data-profile-link-checker"},
                method=method,
            )
            with urllib.request.urlopen(request, timeout=20) as response:
                status = getattr(response, "status", 200)
                if 200 <= status < 400:
                    return True, str(status)
        except urllib.error.HTTPError as exc:
            if 200 <= exc.code < 400:
                return True, str(exc.code)
        except Exception as exc:
            last_error = exc.__class__.__name__

    return False, last_error if "last_error" in locals() else "failed"


def validate_links(markdown: str, root: Path) -> None:
    failures: list[str] = []

    print("[LINK CHECK]")
    for link in extract_links(markdown):
        if link.startswith("#"):
            if local_anchor_exists(markdown, link):
                print(f"PASS anchor {link}")
            else:
                print(f"FAIL anchor {link}")
                failures.append(link)
            continue

        parsed = urllib.parse.urlsplit(link)

        if parsed.scheme in {"http", "https"}:
            ok, detail = check_external_url(link)
            print(("PASS" if ok else "FAIL") + f" {detail} {link}")
            if not ok:
                failures.append(link)
            continue

        if parsed.scheme == "mailto":
            print(f"PASS mailto {link}")
            continue

        local_path = link.split("#", 1)[0]
        candidate = (root / local_path).resolve()

        try:
            candidate.relative_to(root)
        except ValueError:
            print(f"FAIL outside_repo {link}")
            failures.append(link)
            continue

        if candidate.exists():
            print(f"PASS local {link}")
        else:
            print(f"FAIL missing_local {link}")
            failures.append(link)

    if failures:
        print("[FAIL] unresolved links:")
        for item in failures:
            print(item)
        raise SystemExit(1)

    print("PASS all links resolve")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the Zeid Data organization profile README.")
    parser.add_argument("--readme", default=str(DEFAULT_README))
    parser.add_argument("--check-links", action="store_true")
    args = parser.parse_args()

    require_expected_repo()

    now = load_json(NOW_BUILDING)
    defensive = load_json(DEFENSIVE_MAP)
    status = load_json(LITHIUM_STATUS)

    generate_assets(status)

    readme_path = Path(args.readme)
    if not readme_path.is_absolute():
        readme_path = ROOT / readme_path

    content = build_readme(now, defensive, status)
    write_text(readme_path, content)

    print(f"root={ROOT}")
    print(f"wrote={readme_path.relative_to(ROOT)}")
    print("wrote=assets/lithium/lithium-tracker-button.svg")
    print("wrote=assets/lithium/lithium-bot.svg")
    print("wrote=assets/lithium/lithium-progress.svg")

    if args.check_links:
        validate_links(content, ROOT)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

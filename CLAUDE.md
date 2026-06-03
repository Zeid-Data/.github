# zeid-data-github-profile

Organization profile repository. Generates and maintains `profile/README.md` via two independent automation scripts.

## Directory Layout

```
data/                         # Source-of-truth JSON consumed by scripts
  now_building.json           # Active projects and org tagline
  defensive_build_map.json    # Threat radar patterns and severity
profile/
  README.md                   # Generated output — do not hand-edit between sentinel comments
scripts/
  update_profile_readme.py    # Profile README generator (invoked by update-profile-readme workflow)
.github/
  scripts/
    update_threat_radar.py    # Threat radar updater (invoked by update-threat-radar workflow)
  workflows/
    update-profile-readme.yml # Runs on push to data/ or scripts/; creates a PR
    update-threat-radar.yml   # Runs on schedule every 6 h; commits directly to main
```

## Commands

Run the profile README generator locally (requires `GITHUB_TOKEN` and `GITHUB_ORG` env vars):

```bash
python scripts/update_profile_readme.py --org Zeid-Data --readme profile/README.md
```

With link validation:

```bash
python scripts/update_profile_readme.py --org Zeid-Data --readme profile/README.md --check-links
```

Run the threat radar updater locally:

```bash
ZD_OWNER=Zeid-Data ZD_README_PATH=profile/README.md python3 .github/scripts/update_threat_radar.py
```

## Sentinel Comments

`profile/README.md` contains the marker pair:

```
<!-- ZD_THREAT_RADAR_START -->
<!-- ZD_THREAT_RADAR_END -->
```

`update_threat_radar.py` replaces content between these markers on every run. Do not remove or reorder them, and do not add content between them manually — it will be overwritten.

## Secrets

| Secret | Used by | Purpose |
|--------|---------|---------|
| `GITHUB_TOKEN` | both workflows | Read repos, write commits/PRs |
| `ZD_GH_READ_TOKEN` | `update-threat-radar.yml` | Fetch data from private `Zeid-Data/lithium` repo |

## Data Files

Edit `data/now_building.json` to update active projects. Edit `data/defensive_build_map.json` to update threat radar patterns. Both trigger the profile-readme workflow on push.

## Known Issues

- `update-threat-radar.yml` references `actions/checkout@v6` (non-existent). Effective version resolves to latest available; update to `@v4` to be explicit.
- Link validation (`--check-links`) uses `urllib` HEAD requests with a timeout; flaky external URLs will fail the workflow step.
- `.lychee.toml` is untracked (in `.gitignore` via `*.toml`? check before committing). It controls the `lychee` link-checker if that tool is added.

# 2026 FIFA World Cup Forecast Control Tower

A public GitHub Pages dashboard that forecasts the 2026 FIFA World Cup champion using a probabilistic model, live JSON data, historical snapshots, and a separate scenario simulator.

## How to publish it on GitHub Pages

1. Create a public GitHub repository named `world-cup-2026-forecast`.
2. Upload all files from this folder to the repository.
3. Go to **Settings → Pages**.
4. Under **Build and deployment**, select **GitHub Actions**.
5. Go to the **Actions** tab.
6. Open **Update forecast and deploy Pages**.
7. Click **Run workflow**.
8. Open the Pages URL shown in the deployment summary.

## Update cadence

The workflow runs every 4 hours with `cron: "0 */4 * * *"`. You can also run it manually.

## Free-source limitation

Fixtures and structured tournament data are refreshed from free public sources when available. Injuries and squads are best-effort because reliable national-team injury data is difficult to automate for free.

## Files to edit manually if needed

- `data/live/teams.json`
- `data/live/injuries.json`
- `data/live/squads.json`
- `data/live/model-config.json`

This is a probabilistic forecast, not a guarantee.

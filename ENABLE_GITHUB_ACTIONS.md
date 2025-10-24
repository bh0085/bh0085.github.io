# Enable GitHub Actions for Pages

## ⚠️ REQUIRED STEP

For the Notion API key to be injected into the Gantt chart, you **must** enable GitHub Actions as the deployment source.

## Steps:

1. **Go to Repository Settings**
   - Visit: https://github.com/bh0085/bh0085.github.io/settings/pages

2. **Change Build and Deployment Source**
   - Under "Build and deployment"
   - Under "Source" dropdown
   - Change from **"Deploy from a branch"** to **"GitHub Actions"**
   - Click Save (if there's a save button)

3. **Wait for Deployment**
   - GitHub Actions will automatically run when you change this
   - Watch progress at: https://github.com/bh0085/bh0085.github.io/actions
   - Takes about 1-2 minutes

## What This Does

Once enabled, every push to `main` will:
1. Run the `deploy.yml` workflow
2. Inject your `NOTION_API_KEY` secret into `gantt.html`
3. Deploy the site to GitHub Pages

## After Enabling

Your Gantt chart will have:
- **Live data on page load** (fetches from Notion API directly in JavaScript)
- **"Refresh from Notion" button** to pull latest data
- **NOTION_API_KEY** securely injected at build time

## Current Status

- ✅ `NOTION_API_KEY` secret is set in GitHub
- ✅ `deploy.yml` workflow is configured
- ⏳ **Waiting for you to enable GitHub Actions as source**

Once you enable it, the next push will automatically inject the API key and deploy!


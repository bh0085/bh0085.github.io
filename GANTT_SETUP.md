# Gantt Chart Auto-Sync Setup

## ✅ What's Already Done

- **Gantt chart page** created at `/gantt.html`
- **GitHub Actions workflow** created to auto-sync from Notion
- **Python script** (`fetch_gantt.py`) to pull data from Notion
- **Protected with auth** - requires @mlcl.ai login
- **Home link** added to gantt page
- **Link from homepage** - shows "gantt chart" for logged-in users

## 🔧 How It Works

1. **GitHub Actions runs every 6 hours** (or manually triggered)
2. **Fetches data** from your Notion database using `NOTION_API_KEY` secret
3. **Updates** `gantt_data.json` with latest tasks
4. **Commits and pushes** the updated data automatically
5. **GitHub Pages deploys** the updated chart

## 📊 Your Gantt Chart

- **Live URL**: https://www.mlcl.ai/gantt.html
- **Data Source**: Notion database `291cdd12fc5e81ceafeadc78e6c03258`
- **Update Frequency**: Every 6 hours automatically
- **Manual Trigger**: Go to Actions tab → "Update Gantt Data" → "Run workflow"

## ⚙️ Configuration

The workflow uses:
- **Secret**: `NOTION_API_KEY` (already added by you ✓)
- **Database ID**: `291cdd12fc5e81ceafeadc78e6c03258` (hardcoded in `fetch_gantt.py`)
- **Schedule**: `0 */6 * * *` (every 6 hours)

## 🎯 Next Steps

1. **Test the workflow manually**:
   - Go to https://github.com/bh0085/bh0085.github.io/actions
   - Click "Update Gantt Data"
   - Click "Run workflow" → "Run workflow"
   - Wait ~30 seconds
   - Check if `gantt_data.json` was updated

2. **View your Gantt chart**:
   - Visit https://www.mlcl.ai/gantt.html
   - Sign in with your @mlcl.ai account
   - See your tasks visualized

3. **Update data manually** (if needed):
   ```bash
   cd /Users/benjaminholmes/prj/bh0085.github.io
   export NOTION_API_KEY='your-key'
   python fetch_gantt.py
   git add gantt_data.json
   git commit -m "Update Gantt data"
   git push
   ```

## 🔄 Data Flow

```
Notion Database
    ↓ (GitHub Actions every 6 hours)
fetch_gantt.py
    ↓
gantt_data.json
    ↓ (Git commit + push)
GitHub Pages
    ↓ (fetch in browser)
gantt.html displays chart
```

## 📝 Modifying Update Frequency

To change how often the data syncs, edit `.github/workflows/update-gantt.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Change this line
```

Examples:
- Every hour: `'0 * * * *'`
- Every 12 hours: `'0 */12 * * *'`
- Daily at 9am: `'0 9 * * *'`
- Every 30 minutes: `'*/30 * * * *'`


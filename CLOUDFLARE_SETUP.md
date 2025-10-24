# Cloudflare Worker Setup for Notion API

## Step 1: Create Cloudflare Worker

1. **Go to Cloudflare Dashboard:**
   - Visit: https://dash.cloudflare.com/
   - Sign in (or create free account)

2. **Create Worker:**
   - Click "Workers & Pages" in left sidebar
   - Click "Create application"
   - Click "Create Worker"
   - Name it: `notion-proxy`
   - Click "Deploy"

3. **Edit Worker Code:**
   - Click "Edit code" button
   - Delete all the default code
   - Copy and paste the entire contents of `cloudflare-worker.js` from this repo
   - Click "Deploy"

4. **Add Environment Variable:**
   - Click "Settings" tab
   - Click "Variables and Secrets"
   - Under "Environment Variables", click "Add variable"
   - Name: `NOTION_API_KEY`
   - Value: (paste your Notion API key from GitHub secrets)
   - Click "Encrypt" (this makes it a secret)
   - Click "Deploy"

5. **Get Your Worker URL:**
   - Click "Triggers" tab
   - Copy the URL under "Routes" - it looks like:
     `https://notion-proxy.YOUR-ACCOUNT.workers.dev`

6. **Send me this URL** and I'll update gantt.html to use it!

## What This Does

The Cloudflare Worker:
- Proxies requests to Notion API (avoiding CORS)
- Keeps your API key secure (server-side)
- Allows JavaScript fetch from your browser
- Only accepts requests from www.mlcl.ai

## Cost

Free tier includes:
- 100,000 requests/day
- More than enough for your Gantt chart refreshes


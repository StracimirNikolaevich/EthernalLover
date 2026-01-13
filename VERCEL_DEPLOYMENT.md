# Vercel Deployment Guide

This guide will help you deploy your AI Girlfriend Generator to Vercel as a serverless application.

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. GitHub account (for connecting your repository)
3. Supabase database set up (run `supabase_setup.sql`)

## Project Structure

```
EthernalLover/
├── api/                    # Serverless functions
│   ├── generate.py        # Generate AI girlfriend
│   ├── girlfriends.py     # Get all girlfriends
│   └── girlfriend.py      # Get specific girlfriend
├── public/                # Static files (frontend)
│   ├── index.html
│   ├── style.css
│   └── script.js
├── utils.py               # Shared utilities
├── vercel.json            # Vercel configuration
├── requirements.txt       # Python dependencies
└── .env.example           # Environment variables template
```

## Deployment Steps

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit - Vercel serverless version"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Deploy to Vercel

**Option A: Via Vercel Dashboard**
1. Go to https://vercel.com/dashboard
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)

**Option B: Via Vercel CLI**
```bash
npm i -g vercel
vercel login
vercel
```

### 3. Set Environment Variables

In Vercel Dashboard → Your Project → Settings → Environment Variables, add:

```
SUPABASE_URL=https://hqznqbpexocovhyagwmm.supabase.co
SUPABASE_KEY=sb_publishable_p58r1EAkrnd_xLm-thcGTw_NwRRl5ip
```

**Important**: For production, use environment variables instead of hardcoding keys!

### 4. Deploy

Click "Deploy" in Vercel dashboard or run `vercel --prod` via CLI.

## Local Development

### Install Vercel CLI

```bash
npm i -g vercel
```

### Run Locally

```bash
vercel dev
```

This will start a local server at `http://localhost:3000` that mimics Vercel's serverless environment.

## API Endpoints

After deployment, your API will be available at:

- `https://your-project.vercel.app/api/generate` (POST)
- `https://your-project.vercel.app/api/girlfriends` (GET)
- `https://your-project.vercel.app/api/girlfriend?id=123` (GET)

## Troubleshooting

### Function Timeout

If generation takes too long, you may need to increase timeout in `vercel.json`:

```json
{
  "functions": {
    "api/**/*.py": {
      "maxDuration": 60
    }
  }
}
```

### Perchance Issues

If Perchance generation fails:
1. Check that Playwright browsers are installed (they should be in serverless environment)
2. Consider using a different AI service if Perchance doesn't work in serverless

### CORS Issues

CORS is handled in `utils.py`. If you encounter CORS errors, check the headers in `create_response()` function.

## Environment Variables

Create a `.env.local` file for local development:

```
SUPABASE_URL=https://hqznqbpexocovhyagwmm.supabase.co
SUPABASE_KEY=sb_publishable_p58r1EAkrnd_xLm-thcGTw_NwRRl5ip
```

**Never commit `.env.local` to Git!**

## Production Checklist

- [ ] Set environment variables in Vercel dashboard
- [ ] Test all API endpoints
- [ ] Verify Supabase connection
- [ ] Test Perchance generation
- [ ] Check CORS settings
- [ ] Monitor function logs in Vercel dashboard

## Cost Considerations

- Vercel Hobby (Free): 100GB bandwidth, unlimited requests
- Serverless function execution time: 60s max (free tier)
- Supabase: Free tier available

## Support

If you encounter issues:
1. Check Vercel function logs in dashboard
2. Test endpoints with `curl` or Postman
3. Verify environment variables are set correctly
4. Check Supabase table exists and RLS policies are correct

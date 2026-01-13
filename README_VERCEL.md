# EthernalLover - Vercel Serverless Version

This is the serverless version of the AI Girlfriend Generator, converted from Flask to Vercel serverless functions.

## 🚀 Quick Start

### Deploy to Vercel

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Vercel serverless version"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy via Vercel Dashboard**
   - Go to https://vercel.com/dashboard
   - Click "Add New Project"
   - Import your GitHub repository
   - Add environment variables:
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
   - Click "Deploy"

3. **Or use Vercel CLI**
   ```bash
   npm i -g vercel
   vercel login
   vercel
   ```

### Local Development

```bash
# Install Vercel CLI
npm i -g vercel

# Run locally
vercel dev
```

Visit `http://localhost:3000`

## 📁 Project Structure

```
EthernalLover/
├── api/                    # Serverless functions
│   ├── generate.py        # POST /api/generate
│   ├── girlfriends.py     # GET /api/girlfriends
│   └── girlfriend.py      # GET /api/girlfriend?id=123
├── public/                 # Static frontend files
│   ├── index.html
│   ├── style.css
│   └── script.js
├── utils.py               # Shared utilities
├── vercel.json            # Vercel configuration
└── requirements.txt       # Python dependencies
```

## 🔧 Configuration

### Environment Variables

Set these in Vercel Dashboard → Settings → Environment Variables:

- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase anon/public key

### Supabase Setup

Run the SQL from `supabase_setup.sql` in your Supabase SQL Editor to create the `ai_girlfriends` table.

## 📡 API Endpoints

- `POST /api/generate` - Generate a new AI girlfriend
- `GET /api/girlfriends` - Get all girlfriends (limit 10)
- `GET /api/girlfriend?id=123` - Get specific girlfriend by ID

## 🆚 Differences from Flask Version

1. **Serverless Functions**: Each route is now a separate serverless function
2. **No Flask**: Removed Flask dependency, using Vercel's Python runtime
3. **Static Files**: Frontend served from `public/` directory
4. **Environment Variables**: Use Vercel's env vars instead of hardcoded values
5. **Response Format**: Functions return Vercel-compatible response format

## 🐛 Troubleshooting

### Function Timeout
Increase `maxDuration` in `vercel.json` if generation takes too long.

### Perchance Issues
Perchance uses Playwright which may have issues in serverless. Consider:
- Using a different AI service
- Increasing function timeout
- Using edge functions for faster cold starts

### CORS Errors
CORS is handled in `utils.py`. Check headers in `create_response()` function.

## 📚 Documentation

See `VERCEL_DEPLOYMENT.md` for detailed deployment instructions.

## 🔄 Migration from Flask

If you were using the Flask version (`app.py`), this serverless version:
- ✅ Works the same way from user perspective
- ✅ Uses same Supabase database
- ✅ Same frontend interface
- ✅ Better scalability (serverless)
- ✅ Free hosting on Vercel

The old Flask files (`app.py`, `templates/`, `static/`) are kept for reference but not used in deployment.

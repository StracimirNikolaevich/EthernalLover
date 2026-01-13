# API Keys Configuration

This document contains all API keys and configuration for the EthernalLover project.

## 🔐 Supabase Configuration

### Project URL
```
https://hqznqbpexocovhyagwmm.supabase.co
```

### Project ID
```
dennnpsshqxiluqyrxdi
```

### API Keys

**Publishable Key (Anon Key):**
```
sb_publishable_pT0axTxKM-xXV0PEVaYJ3w_0DV2Az9d
```

**Secret Key:**
```
sb_secret_NYx89404F3QczXBN2nay5Q_efIZYkrK
```

### JWT Tokens

**Anon Token:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imhxem5xYnBleG9jb3ZoeWFnd21tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgzMTM2NzYsImV4cCI6MjA4Mzg4OTY3Nn0.15SZstsOUJnLhQK8pmHTM_-OCRX6rCz2PIIyfWLaG-Q
```

**Service Role Token:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imhxem5xYnBleG9jb3ZoeWFnd21tIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODMxMzY3NiwiZXhwIjoyMDgzODg5Njc2fQ.V3yivzcCpJ_XTuqPh6SWFeEOdUTKATAdMgl0Odldp44
```

**JWT Secret Key:**
```
77ed29ef-7b55-4784-b5f2-e8719662c5dc
```

### Environment Variables
```bash
SUPABASE_URL=https://hqznqbpexocovhyagwmm.supabase.co
SUPABASE_PROJECT_ID=dennnpsshqxiluqyrxdi
SUPABASE_KEY=sb_publishable_pT0axTxKM-xXV0PEVaYJ3w_0DV2Az9d
SUPABASE_SECRET=sb_secret_NYx89404F3QczXBN2nay5Q_efIZYkrK
SUPABASE_JWT_SECRET=77ed29ef-7b55-4784-b5f2-e8719662c5dc
```

---

## 🎲 Perchance Configuration

### Generator Endpoint
```
https://perchance.org/welcome
```

### API Information

**Note:** Perchance.org does not provide official API keys. The service can be accessed programmatically using:

1. **Unofficial Python Package:**
   ```bash
   pip install perchance
   ```
   
   Usage:
   ```python
   import perchance
   generator = perchance.TextGenerator()
   ```

2. **Direct Generator Access:**
   - Endpoint: `https://perchance.org/welcome`
   - No authentication required
   - Access via web scraping or unofficial APIs

### Alternative Methods
- Use the `perchance` Python package for programmatic access
- Direct HTTP requests to generator endpoints
- Web scraping (not recommended for production)

---

## 🚀 Vercel Configuration

### Project ID
```
prj_Bvelqar30RhEocGUXN3NHTSHXFi8
```

### API Token
```
6hPD0uQl4UirmcikQ0oozRpp
```

**How to get your Vercel API Token:**
1. Go to [Vercel Dashboard](https://vercel.com/account/tokens)
2. Click "Create Token"
3. Name your token (e.g., "EthernalLover")
4. Copy the generated token

### Environment Variables
```bash
VERCEL_API_TOKEN=6hPD0uQl4UirmcikQ0oozRpp
VERCEL_TEAM_ID=your_team_id_here
VERCEL_PROJECT_ID=prj_Bvelqar30RhEocGUXN3NHTSHXFi8
```

### Vercel CLI Setup
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Link project
vercel link
```

### Deployment Configuration
- **Framework:** Other/Serverless
- **Build Command:** (leave empty)
- **Output Directory:** (leave empty)
- **Install Command:** `pip install -r requirements.txt`

---

## 📝 Usage Notes

### Security Best Practices

1. **Never commit API keys to version control**
   - Add `API_KEYS.md` to `.gitignore`
   - Use environment variables in production

2. **Use environment variables:**
   ```bash
   # .env file (not committed)
   SUPABASE_URL=your_url
   SUPABASE_KEY=your_key
   VERCEL_API_TOKEN=your_token
   ```

3. **Rotate keys regularly:**
   - Supabase: Regenerate keys in Dashboard → Settings → API
   - Vercel: Create new tokens and revoke old ones

### Quick Reference

| Service | Key Type | Location |
|---------|----------|----------|
| Supabase | Publishable Key | Dashboard → Settings → API |
| Supabase | Secret Key | Dashboard → Settings → API |
| Perchance | N/A | No official API |
| Vercel | API Token | Account → Tokens |

---

## 🔄 Key Rotation

If any keys are compromised:
1. **Supabase:** Go to Dashboard → Settings → API → Regenerate
2. **Vercel:** Go to Account → Tokens → Revoke old token → Create new
3. Update all environment variables
4. Redeploy applications

---

**Last Updated:** 2026
**Keep this file secure and never share publicly!**

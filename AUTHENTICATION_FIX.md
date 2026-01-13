# Authentication Configuration - Quick Fix

## Immediate Steps to Fix Login/Signup

### 1. Disable Email Confirmation (For Testing)

To allow immediate sign-in without email verification:

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to **Authentication** → **Providers**
4. Click on **Email**
5. Toggle **Enable email confirmations** to **OFF**
6. Click **Save**

Now users can sign in immediately after signup!

### 2. Configure Redirect URLs

1. Go to **Authentication** → **URL Configuration**
2. Set **Site URL**:
   - Local: `http://localhost:8000`
   - Production: Your Vercel URL
3. Add **Redirect URLs**:
   ```
   http://localhost:8000/**
   http://localhost:8000/characters
   https://your-vercel-url.vercel.app/**
   https://your-vercel-url.vercel.app/characters
   ```

### 3. Run Database Setup

1. Go to **SQL Editor** in Supabase
2. Copy entire `supabase_setup.sql` file
3. Paste and run it
4. Verify all tables and policies are created

### 4. Test Authentication

**Test Signup:**
1. Go to login page
2. Click "Sign up"
3. Enter email and password
4. Submit
5. Should see success message
6. Can immediately sign in (if email confirmation is OFF)

**Test Sign In:**
1. Enter email and password
2. Click "Sign In"
3. Should redirect to `/characters`

**Test Google OAuth:**
1. Click "Continue with Google"
2. Should redirect to Google
3. After sign-in, redirects back to app

## Common Issues Fixed

✅ Email confirmation blocking sign-in → Disabled in settings
✅ Redirect URL errors → Added all necessary URLs
✅ RLS policy conflicts → SQL script now drops existing policies first
✅ Storage bucket errors → Policies are properly configured
✅ Session not persisting → Fixed auth state handling

## Verification

After setup, test:
- [ ] Can create new account
- [ ] Can sign in immediately after signup
- [ ] Can sign in with existing account
- [ ] Redirects to `/characters` after login
- [ ] Session persists on page refresh
- [ ] Can sign out
- [ ] Google OAuth works (if configured)

Your authentication should now work flawlessly! 🎉

# Supabase Setup Guide - Complete Configuration

This guide will help you set up your Supabase database and authentication to work flawlessly with EthernalLover.

## Step 1: Run Database Setup SQL

1. Go to your [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project: `dennnpsshqxiluqyrxdi`
3. Click on **SQL Editor** in the left sidebar
4. Click **New Query**
5. Copy and paste the entire contents of `supabase_setup.sql`
6. Click **Run** (or press Ctrl+Enter)
7. Verify success - you should see "Success. No rows returned"

## Step 2: Configure Authentication Settings

### Enable Email Authentication

1. Go to **Authentication** → **Providers** in Supabase Dashboard
2. Make sure **Email** is enabled
3. Click on **Email** to configure:
   - **Enable email confirmations**: Toggle this based on your preference:
     - **ON** = Users must verify email before signing in (more secure)
     - **OFF** = Users can sign in immediately after signup (easier for testing)
   - **Secure email change**: Enable if you want users to confirm email changes
   - **Double confirm email changes**: Optional, for extra security

### Configure Site URL and Redirect URLs

1. Go to **Authentication** → **URL Configuration**
2. Set **Site URL** to your deployment URL:
   - For local testing: `http://localhost:8000`
   - For Vercel: `https://your-project.vercel.app`
3. Add **Redirect URLs**:
   ```
   http://localhost:8000/characters
   http://localhost:8000/**
   https://your-project.vercel.app/characters
   https://your-project.vercel.app/**
   https://hqznqbpexocovhyagwmm.supabase.co/auth/v1/callback
   ```

### Enable Google OAuth (Optional)

1. Go to **Authentication** → **Providers**
2. Click on **Google**
3. Toggle **Enable Sign in with Google** to ON
4. Add your **Client IDs** from Google Cloud Console
5. Add your **Client Secret (for OAuth)**
6. Click **Save**

**To get Google OAuth credentials:**
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create OAuth 2.0 Client ID (Web application)
- Add redirect URI: `https://hqznqbpexocovhyagwmm.supabase.co/auth/v1/callback`
- Copy Client ID and Secret to Supabase

## Step 3: Configure Storage Bucket

1. Go to **Storage** in Supabase Dashboard
2. Verify `character-images` bucket exists (created by SQL script)
3. If it doesn't exist, create it:
   - Click **New bucket**
   - Name: `character-images`
   - Public bucket: **ON** (checked)
   - Click **Create bucket**
4. Click on the bucket to verify policies are set:
   - Public can view images
   - Authenticated users can upload
   - Authenticated users can delete

## Step 4: Verify Row Level Security (RLS)

The SQL script should have created all RLS policies. Verify:

1. Go to **Table Editor** → `ai_girlfriends`
2. Click on **Policies** tab
3. You should see 4 policies:
   - Users can view their own characters
   - Users can insert their own characters
   - Users can update their own characters
   - Users can delete their own characters

4. Do the same for `chat_messages` table

## Step 5: Test Authentication

### Test Email/Password Signup

1. Go to your login page
2. Click "Sign up" link
3. Enter email and password
4. Submit the form
5. Check for success message
6. If email confirmation is enabled, check your email
7. Click the confirmation link
8. Try signing in

### Test Email/Password Sign In

1. Use an account you've created
2. Enter email and password
3. Click "Sign In"
4. Should redirect to `/characters` page

### Test Google OAuth (if configured)

1. Click "Continue with Google"
2. Should redirect to Google sign-in
3. After signing in, should redirect back to `/characters`

## Step 6: Troubleshooting

### "Email not confirmed" error
- **Solution**: Check your email and click the confirmation link
- Or disable email confirmation in Supabase Dashboard → Authentication → Providers → Email

### "Invalid login credentials" error
- Check email and password are correct
- Make sure email is confirmed (if confirmation is enabled)
- Try resetting password

### Google OAuth not working
- Verify Client ID and Secret are correct in Supabase
- Check redirect URI matches: `https://hqznqbpexocovhyagwmm.supabase.co/auth/v1/callback`
- Verify Google OAuth is enabled in Supabase

### RLS Policy errors
- Make sure RLS is enabled on tables
- Verify policies are created correctly
- Check that `auth.uid()` matches `user_id` in queries

### Storage upload errors
- Verify `character-images` bucket exists
- Check bucket is public
- Verify storage policies allow authenticated uploads

## Quick Configuration Checklist

- [ ] Database tables created (`ai_girlfriends`, `chat_messages`)
- [ ] RLS policies enabled and configured
- [ ] Storage bucket `character-images` created
- [ ] Storage policies configured
- [ ] Email authentication enabled
- [ ] Site URL configured
- [ ] Redirect URLs added
- [ ] Google OAuth configured (optional)
- [ ] Tested email signup
- [ ] Tested email signin
- [ ] Tested Google OAuth (if enabled)

## Recommended Settings for Easy Testing

If you want to test quickly without email confirmation:

1. Go to **Authentication** → **Providers** → **Email**
2. Toggle **Enable email confirmations** to **OFF**
3. Users can sign in immediately after signup

**Note**: For production, it's recommended to keep email confirmation ON for security.

## Production Settings

For production deployment:

1. **Enable email confirmations**: ON
2. **Secure email change**: ON
3. **Site URL**: Your production Vercel URL
4. **Redirect URLs**: Include production URLs only
5. **Google OAuth**: Fully configured with production redirect URIs

Your Supabase database is now configured and ready to use!

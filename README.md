# EthernalLover - AI Girlfriend Application

A full-stack web application for creating and chatting with AI companions, built with Vercel serverless functions and Supabase.

## Features

- 🔐 **Authentication**: Email/password and Google OAuth login via Supabase
- 👥 **Character Management**: Create and manage multiple AI companions
- 💬 **Chat System**: Real-time chat with your AI companions
- 📸 **Image Sharing**: Upload and share images in conversations
- 💾 **Data Persistence**: All characters, chats, and images saved in Supabase

## Project Structure

```
EthernalLover/
├── public/              # Frontend files
│   ├── index.html      # Login page
│   ├── characters.html  # Character selection page
│   ├── character.html   # Character details + chat page
│   ├── auth.js         # Supabase authentication
│   ├── app.js          # Navigation and character management
│   ├── chat.js         # Chat functionality
│   └── style.css       # Styling
├── api/                # Vercel serverless functions
│   ├── characters.py   # List/create characters
│   ├── character.py    # Get/delete character
│   ├── generate.py     # Generate character with Perchance
│   ├── messages.py     # Get/send chat messages
│   └── upload.py      # Upload images to Supabase Storage
├── utils.py            # Shared utilities
├── supabase_setup.sql  # Database schema
├── vercel.json         # Vercel configuration
├── requirements.txt    # Python dependencies
└── API_KEYS.md        # API keys and configuration
```

## Setup Instructions

### 1. Database Setup

1. Go to your [Supabase Dashboard](https://supabase.com/dashboard)
2. Open the SQL Editor
3. Run the SQL from `supabase_setup.sql` to create:
   - `ai_girlfriends` table
   - `chat_messages` table
   - Row Level Security (RLS) policies
   - Storage bucket for images

### 2. Environment Variables

Set these in your Vercel project settings:

```bash
SUPABASE_URL=https://hqznqbpexocovhyagwmm.supabase.co
SUPABASE_KEY=sb_publishable_pT0axTxKM-xXV0PEVaYJ3w_0DV2Az9d
SUPABASE_SECRET=sb_secret_NYx89404F3QczXBN2nay5Q_efIZYkrK
SUPABASE_JWT_SECRET=77ed29ef-7b55-4784-b5f2-e8719662c5dc
```

### 3. Deploy to Vercel

**Option A: Via Vercel Dashboard**
1. Push your code to GitHub
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "Add New Project"
4. Import your repository
5. Configure:
   - Framework: Other
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
6. Add environment variables
7. Deploy

**Option B: Via Vercel CLI**
```bash
npm i -g vercel
vercel login
vercel
```

### 4. Configure Supabase Storage

1. Go to Supabase Dashboard → Storage
2. Ensure `character-images` bucket exists (created by SQL script)
3. Verify bucket is public for reading
4. Check storage policies allow authenticated uploads

## Usage

1. **Login**: Visit your deployed site and sign in with email/password or Google
2. **Create Character**: Click "Create New Character" and fill in preferences
3. **Select Character**: Choose a character from your list
4. **Chat**: Send messages and images to your AI companion
5. **View History**: All conversations are saved and displayed

## API Endpoints

- `GET /api/characters` - Get all user's characters
- `POST /api/generate` - Generate new character
- `GET /api/character?id={id}` - Get character details
- `DELETE /api/character?id={id}` - Delete character
- `GET /api/messages?character_id={id}` - Get chat history
- `POST /api/messages` - Send message
- `POST /api/upload` - Upload image

## Technologies

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Vercel serverless functions)
- **Database**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage
- **Authentication**: Supabase Auth
- **AI Generation**: Perchance AI
- **Hosting**: Vercel

## Security

- All API endpoints require authentication
- Row Level Security (RLS) ensures users only access their own data
- Images are stored securely in Supabase Storage
- JWT tokens validated on every request

## Troubleshooting

**Characters not loading?**
- Check Supabase RLS policies are set correctly
- Verify user is authenticated
- Check browser console for errors

**Images not uploading?**
- Verify `character-images` bucket exists
- Check storage policies allow uploads
- Ensure file size is under 5MB

**Perchance generation failing?**
- Check internet connection
- Verify Perchance package is installed
- Check API logs for errors

## License

Private project - All rights reserved

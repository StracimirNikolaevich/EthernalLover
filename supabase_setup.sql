-- Supabase Database Setup for EthernalLover
-- Run this SQL in your Supabase SQL Editor

-- 1. Create ai_girlfriends table
CREATE TABLE IF NOT EXISTS ai_girlfriends (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    personality TEXT,
    appearance TEXT,
    interests TEXT,
    backstory TEXT,
    age TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    preferences JSONB DEFAULT '{}'::jsonb
);

-- 2. Create chat_messages table
CREATE TABLE IF NOT EXISTS chat_messages (
    id BIGSERIAL PRIMARY KEY,
    character_id BIGINT NOT NULL REFERENCES ai_girlfriends(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    sender_type TEXT NOT NULL CHECK (sender_type IN ('user', 'character')),
    message_text TEXT,
    image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_ai_girlfriends_user_id ON ai_girlfriends(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_girlfriends_created_at ON ai_girlfriends(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_chat_messages_character_id ON chat_messages(character_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON chat_messages(created_at DESC);

-- 4. Enable Row Level Security (RLS)
ALTER TABLE ai_girlfriends ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

-- 5. Drop existing policies if they exist (to avoid conflicts)
DROP POLICY IF EXISTS "Users can view their own characters" ON ai_girlfriends;
DROP POLICY IF EXISTS "Users can insert their own characters" ON ai_girlfriends;
DROP POLICY IF EXISTS "Users can update their own characters" ON ai_girlfriends;
DROP POLICY IF EXISTS "Users can delete their own characters" ON ai_girlfriends;
DROP POLICY IF EXISTS "Users can view messages for their characters" ON chat_messages;
DROP POLICY IF EXISTS "Users can insert messages for their characters" ON chat_messages;
DROP POLICY IF EXISTS "Users can update their own messages" ON chat_messages;
DROP POLICY IF EXISTS "Users can delete their own messages" ON chat_messages;

-- 6. RLS Policies for ai_girlfriends
-- Users can only see their own characters
CREATE POLICY "Users can view their own characters"
    ON ai_girlfriends FOR SELECT
    USING (auth.uid() = user_id);

-- Users can insert their own characters
CREATE POLICY "Users can insert their own characters"
    ON ai_girlfriends FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Users can update their own characters
CREATE POLICY "Users can update their own characters"
    ON ai_girlfriends FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Users can delete their own characters
CREATE POLICY "Users can delete their own characters"
    ON ai_girlfriends FOR DELETE
    USING (auth.uid() = user_id);

-- 7. RLS Policies for chat_messages
-- Users can only see messages for their own characters
CREATE POLICY "Users can view messages for their characters"
    ON chat_messages FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM ai_girlfriends
            WHERE ai_girlfriends.id = chat_messages.character_id
            AND ai_girlfriends.user_id = auth.uid()
        )
    );

-- Users can insert messages for their own characters
CREATE POLICY "Users can insert messages for their characters"
    ON chat_messages FOR INSERT
    WITH CHECK (
        auth.uid() = user_id AND
        EXISTS (
            SELECT 1 FROM ai_girlfriends
            WHERE ai_girlfriends.id = chat_messages.character_id
            AND ai_girlfriends.user_id = auth.uid()
        )
    );

-- Users can update their own messages
CREATE POLICY "Users can update their own messages"
    ON chat_messages FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Users can delete their own messages
CREATE POLICY "Users can delete their own messages"
    ON chat_messages FOR DELETE
    USING (auth.uid() = user_id);

-- 8. Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 9. Create trigger to auto-update updated_at
CREATE TRIGGER update_ai_girlfriends_updated_at
    BEFORE UPDATE ON ai_girlfriends
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 10. Create storage bucket for character images
INSERT INTO storage.buckets (id, name, public)
VALUES ('character-images', 'character-images', true)
ON CONFLICT (id) DO NOTHING;

-- 10. Storage policies for character-images bucket
-- Drop existing policies if they exist (to avoid conflicts)
DROP POLICY IF EXISTS "Authenticated users can upload images" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated users can update their images" ON storage.objects;
DROP POLICY IF EXISTS "Public can view images" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated users can delete their images" ON storage.objects;

-- Allow authenticated users to upload images
CREATE POLICY "Authenticated users can upload images"
    ON storage.objects FOR INSERT
    TO authenticated
    WITH CHECK (bucket_id = 'character-images');

-- Allow authenticated users to update their own images
CREATE POLICY "Authenticated users can update their images"
    ON storage.objects FOR UPDATE
    TO authenticated
    USING (bucket_id = 'character-images')
    WITH CHECK (bucket_id = 'character-images');

-- Allow public read access to images
CREATE POLICY "Public can view images"
    ON storage.objects FOR SELECT
    TO public
    USING (bucket_id = 'character-images');

-- Allow authenticated users to delete their own images
CREATE POLICY "Authenticated users can delete their images"
    ON storage.objects FOR DELETE
    TO authenticated
    USING (bucket_id = 'character-images');

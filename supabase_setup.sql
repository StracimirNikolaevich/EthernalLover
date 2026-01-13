-- Create the ai_girlfriends table in Supabase
-- Run this SQL in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS ai_girlfriends (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    personality TEXT,
    appearance TEXT,
    interests TEXT,
    backstory TEXT,
    preferences JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create an index on created_at for faster queries
CREATE INDEX IF NOT EXISTS idx_ai_girlfriends_created_at ON ai_girlfriends(created_at DESC);

-- Enable Row Level Security (optional, adjust as needed)
ALTER TABLE ai_girlfriends ENABLE ROW LEVEL SECURITY;

-- Create a policy to allow all operations (adjust based on your security needs)
CREATE POLICY "Allow all operations" ON ai_girlfriends
    FOR ALL
    USING (true)
    WITH CHECK (true);

"""
Shared utilities for Vercel serverless functions
"""
import os
from supabase import create_client, Client
from datetime import datetime
import json

# Supabase configuration from environment variables
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://hqznqbpexocovhyagwmm.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'sb_publishable_p58r1EAkrnd_xLm-thcGTw_NwRRl5ip')

def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def parse_generated_content(text, preferences):
    """Parse the generated text into structured data"""
    lines = text.split('\n')
    
    # Default values from preferences
    name = preferences.get('name', '').strip() or 'Luna'
    personality = preferences.get('personality', 'sweet and caring')
    appearance = preferences.get('appearance', 'beautiful with a warm smile')
    interests = preferences.get('interests', 'reading, music, and spending time together')
    
    # Try to extract information from generated text
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        if not line_lower:
            continue
            
        # Extract name (look for "name:" pattern or first capitalized word if no name provided)
        if 'name' in line_lower and (':' in line or 'is' in line_lower):
            if ':' in line:
                potential_name = line.split(':')[-1].strip()
                if potential_name and len(potential_name) < 50:  # Reasonable name length
                    name = potential_name.split()[0] if potential_name.split() else name
        elif not preferences.get('name') and i == 0 and len(line) > 0 and line[0].isupper():
            # First line starting with capital might be a name
            first_word = line.split()[0] if line.split() else ''
            if first_word and len(first_word) < 20 and first_word[0].isupper():
                name = first_word.strip('.,!?')
        
        # Extract personality
        if 'personality' in line_lower and ':' in line:
            personality = line.split(':')[-1].strip()
        elif 'personality' in line_lower:
            # Next line might be the description
            if i + 1 < len(lines) and lines[i + 1].strip():
                personality = lines[i + 1].strip()
        
        # Extract appearance
        if 'appearance' in line_lower and ':' in line:
            appearance = line.split(':')[-1].strip()
        elif 'appearance' in line_lower or 'looks' in line_lower:
            if i + 1 < len(lines) and lines[i + 1].strip():
                appearance = lines[i + 1].strip()
        
        # Extract interests
        if 'interest' in line_lower and ':' in line:
            interests = line.split(':')[-1].strip()
        elif 'hobby' in line_lower or 'hobbies' in line_lower:
            if ':' in line:
                interests = line.split(':')[-1].strip()
    
    # Use full text as backstory if it's substantial
    backstory = text.strip()
    if len(backstory) > 1000:
        backstory = backstory[:1000] + "..."
    
    return {
        'name': name,
        'personality': personality,
        'appearance': appearance,
        'interests': interests,
        'backstory': backstory if backstory else "A wonderful AI companion created just for you."
    }

def create_response(data, status_code=200):
    """Create a JSON response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(data)
    }

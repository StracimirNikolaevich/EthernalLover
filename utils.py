import os
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
import jwt
from typing import Optional, Dict, Any

# Supabase configuration from environment variables
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://hqznqbpexocovhyagwmm.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'sb_publishable_pT0axTxKM-xXV0PEVaYJ3w_0DV2Az9d')
SUPABASE_SECRET = os.environ.get('SUPABASE_SECRET', 'sb_secret_NYx89404F3QczXBN2nay5Q_efIZYkrK')
SUPABASE_JWT_SECRET = os.environ.get('SUPABASE_JWT_SECRET', '77ed29ef-7b55-4784-b5f2-e8719662c5dc')

def get_user_id_from_token(token: str) -> Optional[str]:
    """Extract user_id from JWT token"""
    try:
        # Decode without verification for now (in production, verify with Supabase JWT secret)
        # For Supabase, we can decode to get user_id
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded.get('sub')  # 'sub' is the user_id in Supabase JWT
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None

def get_supabase_client(auth_token: Optional[str] = None) -> Client:
    """Get Supabase client instance"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_auth_token_from_request(headers: Dict[str, Any]) -> Optional[str]:
    """Extract auth token from request headers"""
    auth_header = headers.get('authorization') or headers.get('Authorization')
    if not auth_header:
        return None
    
    if auth_header.startswith('Bearer '):
        return auth_header.replace('Bearer ', '')
    return auth_header

def create_response(data: Any, status_code: int = 200, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Create a standardized API response"""
    response = {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': data
    }
    
    if headers:
        response['headers'].update(headers)
    
    return response

def parse_generated_content(text: str, preferences: Dict[str, Any]) -> Dict[str, str]:
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
        elif not preferences.get('name') and i == 0 and line and line[0].isupper():
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

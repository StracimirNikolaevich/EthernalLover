"""
Vercel serverless function for getting all girlfriends
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_supabase_client, create_response

def handler(req):
    """Vercel serverless function handler"""
    # Handle CORS preflight
    if req.get('method') == 'OPTIONS':
        return create_response({}, 200)
    
    if req.get('method') != 'GET':
        return create_response({
            'success': False,
            'error': 'Method not allowed'
        }, 405)
    
    try:
        supabase = get_supabase_client()
        result = supabase.table('ai_girlfriends').select('*').order('created_at', desc=True).limit(10).execute()
        
        return create_response({
            'success': True,
            'girlfriends': result.data
        })
    except Exception as e:
        return create_response({
            'success': False,
            'error': str(e)
        }, 500)

"""
Vercel serverless function for getting a specific girlfriend by ID
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
        # Extract ID from query string - Vercel passes query as dict
        query = req.get('query', {}) or {}
        girlfriend_id = query.get('id') or query.get('girlfriend_id')
        
        if not girlfriend_id:
            return create_response({
                'success': False,
                'error': 'Girlfriend ID is required'
            }, 400)
        
        try:
            girlfriend_id = int(girlfriend_id)
        except ValueError:
            return create_response({
                'success': False,
                'error': 'Invalid girlfriend ID'
            }, 400)
        
        supabase = get_supabase_client()
        result = supabase.table('ai_girlfriends').select('*').eq('id', girlfriend_id).execute()
        
        if result.data:
            return create_response({
                'success': True,
                'girlfriend': result.data[0]
            })
        else:
            return create_response({
                'success': False,
                'error': 'Girlfriend not found'
            }, 404)
    except Exception as e:
        return create_response({
            'success': False,
            'error': str(e)
        }, 500)

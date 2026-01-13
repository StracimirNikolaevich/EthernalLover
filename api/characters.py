from http.server import BaseHTTPRequestHandler
import json
from utils import get_supabase_client, get_auth_token_from_request, get_user_id_from_token, create_response

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        return
    
    def do_GET(self):
        """Get all characters for the authenticated user"""
        try:
            # Get auth token
            auth_token = get_auth_token_from_request(dict(self.headers))
            if not auth_token:
                return self.send_json_response(
                    create_response({'success': False, 'error': 'Unauthorized'}, 401)
                )
            
            user_id = get_user_id_from_token(auth_token)
            if not user_id:
                return self.send_json_response(
                    create_response({'success': False, 'error': 'Invalid token'}, 401)
                )
            
            # Get characters from Supabase
            supabase = get_supabase_client()
            result = supabase.table('ai_girlfriends').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            
            return self.send_json_response(
                create_response({
                    'success': True,
                    'characters': result.data if result.data else []
                })
            )
            
        except Exception as e:
            print(f"Error in GET /api/characters: {e}")
            return self.send_json_response(
                create_response({'success': False, 'error': str(e)}, 500)
            )
    
    def do_POST(self):
        """Create a new character (redirects to generate endpoint)"""
        try:
            # Get auth token
            auth_token = get_auth_token_from_request(dict(self.headers))
            if not auth_token:
                return self.send_json_response(
                    create_response({'success': False, 'error': 'Unauthorized'}, 401)
                )
            
            user_id = get_user_id_from_token(auth_token)
            if not user_id:
                return self.send_json_response(
                    create_response({'success': False, 'error': 'Invalid token'}, 401)
                )
            
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            preferences = data.get('preferences', {})
            
            # For now, just return success - actual generation should use /api/generate
            return self.send_json_response(
                create_response({
                    'success': True,
                    'message': 'Use /api/generate to create a character'
                })
            )
            
        except Exception as e:
            print(f"Error in POST /api/characters: {e}")
            return self.send_json_response(
                create_response({'success': False, 'error': str(e)}, 500)
            )
    
    def send_json_response(self, response_data):
        """Send JSON response"""
        self.send_response(response_data['statusCode'])
        for key, value in response_data['headers'].items():
            self.send_header(key, value)
        self.end_headers()
        
        body = json.dumps(response_data['body'])
        self.wfile.write(body.encode('utf-8'))
        return

from http.server import BaseHTTPRequestHandler
import json
from utils import get_supabase_client, get_auth_token_from_request, get_user_id_from_token, create_response

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        return
    
    def do_GET(self):
        """Get a single character by ID"""
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
            
            # Get character ID from query string
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            character_id = query_params.get('id', [None])[0]
            
            if not character_id:
                return self.send_json_response(
                    create_response({'success': False, 'error': 'Character ID required'}, 400)
                )
            
            # Get character from Supabase
            supabase = get_supabase_client()
            result = supabase.table('ai_girlfriends').select('*').eq('id', character_id).eq('user_id', user_id).execute()
            
            if not result.data or len(result.data) == 0:
                return self.send_json_response(
                    create_response({'success': False, 'error': 'Character not found'}, 404)
                )
            
            return self.send_json_response(
                create_response({
                    'success': True,
                    'character': result.data[0]
                })
            )
            
        except Exception as e:
            print(f"Error in GET /api/character: {e}")
            return self.send_json_response(
                create_response({'success': False, 'error': str(e)}, 500)
            )
    
    def do_DELETE(self):
        """Delete a character"""
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
            
            # Get character ID from query string
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            character_id = query_params.get('id', [None])[0]
            
            if not character_id:
                return self.send_json_response(
                    create_response({'success': False, 'error': 'Character ID required'}, 400)
                )
            
            # Delete character from Supabase (cascade will delete messages)
            supabase = get_supabase_client()
            result = supabase.table('ai_girlfriends').delete().eq('id', character_id).eq('user_id', user_id).execute()
            
            return self.send_json_response(
                create_response({
                    'success': True,
                    'message': 'Character deleted successfully'
                })
            )
            
        except Exception as e:
            print(f"Error in DELETE /api/character: {e}")
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

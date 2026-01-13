from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
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
        """Get chat messages for a character"""
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
            
            # Get character_id from query string
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            character_id = query_params.get('character_id', [None])[0]
            
            if not character_id:
                return self.send_json_response(
                    create_response({'success': False, 'error': 'Character ID required'}, 400)
                )
            
            # Verify character belongs to user
            supabase = get_supabase_client()
            char_result = supabase.table('ai_girlfriends').select('id').eq('id', character_id).eq('user_id', user_id).execute()
            
            if not char_result.data or len(char_result.data) == 0:
                return self.send_json_response(
                    create_response({'success': False, 'error': 'Character not found'}, 404)
                )
            
            # Get messages
            result = supabase.table('chat_messages').select('*').eq('character_id', character_id).order('created_at', desc=False).execute()
            
            return self.send_json_response(
                create_response({
                    'success': True,
                    'messages': result.data if result.data else []
                })
            )
            
        except Exception as e:
            print(f"Error in GET /api/messages: {e}")
            return self.send_json_response(
                create_response({'success': False, 'error': str(e)}, 500)
            )
    
    def do_POST(self):
        """Send a new message"""
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
            
            character_id = data.get('character_id')
            sender_type = data.get('sender_type', 'user')
            message_text = data.get('message_text')
            image_url = data.get('image_url')
            
            if not character_id:
                return self.send_json_response(
                    create_response({'success': False, 'error': 'Character ID required'}, 400)
                )
            
            if not message_text and not image_url:
                return self.send_json_response(
                    create_response({'success': False, 'error': 'Message text or image required'}, 400)
                )
            
            # Verify character belongs to user
            supabase = get_supabase_client()
            char_result = supabase.table('ai_girlfriends').select('id, name').eq('id', character_id).eq('user_id', user_id).execute()
            
            if not char_result.data or len(char_result.data) == 0:
                return self.send_json_response(
                    create_response({'success': False, 'error': 'Character not found'}, 404)
                )
            
            # Insert message
            message_data = {
                'character_id': character_id,
                'user_id': user_id,
                'sender_type': sender_type,
                'created_at': datetime.now().isoformat()
            }
            
            if message_text:
                message_data['message_text'] = message_text
            if image_url:
                message_data['image_url'] = image_url
            
            result = supabase.table('chat_messages').insert(message_data).execute()
            
            if result.data and len(result.data) > 0:
                return self.send_json_response(
                    create_response({
                        'success': True,
                        'message': result.data[0]
                    })
                )
            else:
                return self.send_json_response(
                    create_response({'success': False, 'error': 'Failed to save message'}, 500)
                )
            
        except Exception as e:
            print(f"Error in POST /api/messages: {e}")
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

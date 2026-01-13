from http.server import BaseHTTPRequestHandler
import json
import os
import uuid
from datetime import datetime, timedelta
from utils import get_supabase_client, get_auth_token_from_request, get_user_id_from_token, create_response

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        return
    
    def do_POST(self):
        """Upload an image to Supabase Storage"""
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
            
            # Parse multipart form data
            content_type = self.headers.get('Content-Type', '')
            
            # For Vercel, we'll expect JSON with base64 encoded image or use direct file handling
            # Try JSON first (for base64 images)
            try:
                data = json.loads(body.decode('utf-8'))
                image_data = data.get('image')  # base64 encoded
                character_id = data.get('character_id')
                
                if image_data and character_id:
                    import base64
                    # Decode base64 image
                    if image_data.startswith('data:image'):
                        # Remove data URL prefix
                        image_data = image_data.split(',')[1]
                    file_data = base64.b64decode(image_data)
                    file_extension = 'jpg'
                else:
                    raise ValueError("JSON format not found")
            except:
                # Fallback: try multipart form data
                import cgi
                import io
                
                form = cgi.FieldStorage(
                    fp=io.BytesIO(body),
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': content_type}
                )
                
                image_file = form.getvalue('image')
                character_id = form.getvalue('character_id')
                
                if not image_file or not character_id:
                    return self.send_json_response(
                        create_response({'success': False, 'error': 'Image and character_id required'}, 400)
                    )
                
                # Get file data
                if hasattr(image_file, 'read'):
                    file_data = image_file.read()
                    file_extension = image_file.filename.split('.')[-1] if hasattr(image_file, 'filename') and image_file.filename else 'jpg'
                elif isinstance(image_file, bytes):
                    file_data = image_file
                    file_extension = 'jpg'
                else:
                    return self.send_json_response(
                        create_response({'success': False, 'error': 'Invalid image format'}, 400)
                    )
            
            # Verify character belongs to user
            supabase = get_supabase_client()
            char_result = supabase.table('ai_girlfriends').select('id').eq('id', character_id).eq('user_id', user_id).execute()
            
            if not char_result.data or len(char_result.data) == 0:
                return self.send_json_response(
                    create_response({'success': False, 'error': 'Character not found'}, 404)
                )
            
            # Generate unique filename
            filename = f"{uuid.uuid4()}.{file_extension}"
            file_path = f"characters/{character_id}/{filename}"
            
            # Upload to Supabase Storage
            storage = supabase.storage.from('character-images')
            
            # Upload file
            try:
                upload_result = storage.upload(file_path, file_data, file_options={"content-type": f"image/{file_extension}", "upsert": "false"})
            except Exception as upload_error:
                # If upload fails, try with upsert
                try:
                    upload_result = storage.upload(file_path, file_data, file_options={"content-type": f"image/{file_extension}", "upsert": "true"})
                except:
                    return self.send_json_response(
                        create_response({'success': False, 'error': f'Upload failed: {str(upload_error)}'}, 500)
                    )
            
            # Get public URL
            try:
                url_result = storage.get_public_url(file_path)
                image_url = url_result if isinstance(url_result, str) else str(url_result)
            except:
                # Fallback: construct URL manually
                supabase_url = os.environ.get('SUPABASE_URL', 'https://hqznqbpexocovhyagwmm.supabase.co')
                image_url = f"{supabase_url}/storage/v1/object/public/character-images/{file_path}"
            
            return self.send_json_response(
                create_response({
                    'success': True,
                    'image_url': image_url,
                    'file_path': file_path
                })
            )
            
        except Exception as e:
            print(f"Error in POST /api/upload: {e}")
            import traceback
            traceback.print_exc()
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

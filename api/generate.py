from http.server import BaseHTTPRequestHandler
import json
import asyncio
import perchance
from datetime import datetime
from utils import (
    get_supabase_client, 
    get_auth_token_from_request, 
    get_user_id_from_token, 
    create_response,
    parse_generated_content
)

# Global Perchance generator
perchance_gen = None

def init_perchance():
    """Initialize Perchance generator"""
    global perchance_gen
    if perchance_gen is None:
        try:
            perchance_gen = perchance.TextGenerator()
            print("Perchance generator initialized")
        except Exception as e:
            print(f"Warning: Perchance initialization failed: {e}")
    return perchance_gen

async def generate_text_async(prompt):
    """Generate text asynchronously using Perchance"""
    global perchance_gen
    if perchance_gen is None:
        init_perchance()
    
    if perchance_gen is None:
        raise Exception("Perchance generator not available")
    
    generated_text = ""
    async for chunk in perchance_gen.text(prompt):
        generated_text += chunk
    return generated_text

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        return
    
    def do_POST(self):
        """Generate a new AI girlfriend character"""
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
            
            # Create prompt for AI girlfriend generation
            name_pref = preferences.get('name', '').strip()
            if not name_pref:
                name_pref = "a unique and beautiful name"
            
            prompt = f"""Create a detailed AI girlfriend character profile:
            Name: {name_pref}
            Personality: {preferences.get('personality', 'sweet and caring')}
            Appearance: {preferences.get('appearance', 'beautiful')}
            Interests: {preferences.get('interests', 'various')}
            Age: {preferences.get('age', '20s')}
            
            Please provide a complete character description with a name, personality description, appearance details, interests, and a brief backstory."""
            
            # Generate text using Perchance
            try:
                init_perchance()
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                generated_text = loop.run_until_complete(generate_text_async(prompt))
                loop.close()
            except Exception as e:
                print(f"Perchance generation error: {e}")
                # Fallback to using preferences directly
                generated_text = f"Name: {name_pref}\nPersonality: {preferences.get('personality', 'sweet and caring')}\nAppearance: {preferences.get('appearance', 'beautiful')}\nInterests: {preferences.get('interests', 'various')}"
            
            # Parse and structure the generated content
            girlfriend_data = parse_generated_content(generated_text, preferences)
            
            # Save to Supabase
            supabase = get_supabase_client()
            result = supabase.table('ai_girlfriends').insert({
                'user_id': user_id,
                'name': girlfriend_data['name'],
                'personality': girlfriend_data['personality'],
                'appearance': girlfriend_data['appearance'],
                'interests': girlfriend_data['interests'],
                'backstory': girlfriend_data['backstory'],
                'age': preferences.get('age', '20s'),
                'created_at': datetime.now().isoformat(),
                'preferences': json.dumps(preferences)
            }).execute()
            
            if result.data and len(result.data) > 0:
                girlfriend_data['id'] = result.data[0]['id']
                return self.send_json_response(
                    create_response({
                        'success': True,
                        'character': girlfriend_data
                    })
                )
            else:
                return self.send_json_response(
                    create_response({'success': False, 'error': 'Failed to save character'}, 500)
                )
            
        except Exception as e:
            print(f"Error in POST /api/generate: {e}")
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

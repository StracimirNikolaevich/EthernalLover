"""
Vercel serverless function for generating AI girlfriend
"""
import asyncio
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import perchance
from utils import get_supabase_client, parse_generated_content, create_response
from datetime import datetime

async def generate_text_async(prompt):
    """Generate text asynchronously using Perchance"""
    try:
        perchance_gen = perchance.TextGenerator()
        generated_text = ""
        async for chunk in perchance_gen.text(prompt):
            generated_text += chunk
        return generated_text
    except Exception as e:
        raise Exception(f"Perchance generation failed: {str(e)}")

def handler(req):
    """Vercel serverless function handler"""
    # Handle CORS preflight
    if req.get('method') == 'OPTIONS':
        return create_response({}, 200)
    
    if req.get('method') != 'POST':
        return create_response({
            'success': False,
            'error': 'Method not allowed'
        }, 405)
    
    try:
        # Parse request body - Vercel passes body as string
        body_str = req.get('body', '{}')
        body = json.loads(body_str) if isinstance(body_str, str) else body_str
        preferences = body.get('preferences', {})
        
        # Create a prompt for AI girlfriend generation
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
        
        # Generate text using Perchance (run async function)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            generated_text = loop.run_until_complete(generate_text_async(prompt))
        finally:
            loop.close()
        
        # Parse and structure the generated content
        girlfriend_data = parse_generated_content(generated_text, preferences)
        
        # Save to Supabase
        supabase = get_supabase_client()
        result = supabase.table('ai_girlfriends').insert({
            'name': girlfriend_data['name'],
            'personality': girlfriend_data['personality'],
            'appearance': girlfriend_data['appearance'],
            'interests': girlfriend_data['interests'],
            'backstory': girlfriend_data['backstory'],
            'created_at': datetime.now().isoformat(),
            'preferences': json.dumps(preferences)
        }).execute()
        
        girlfriend_data['id'] = result.data[0]['id'] if result.data else None
        
        return create_response({
            'success': True,
            'girlfriend': girlfriend_data
        })
        
    except Exception as e:
        return create_response({
            'success': False,
            'error': str(e)
        }, 500)

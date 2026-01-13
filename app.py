from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import asyncio
import perchance
from supabase import create_client, Client
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Supabase configuration
SUPABASE_URL = "https://hqznqbpexocovhyagwmm.supabase.co"
SUPABASE_KEY = "sb_publishable_p58r1EAkrnd_xLm-thcGTw_NwRRl5ip"
SUPABASE_SECRET = "sb_secret_utFYQn0his-xv-aNXUxEiQ_BB-B8OHs"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize Perchance generator
perchance_gen = None

def init_perchance_sync():
    """Initialize Perchance generator synchronously"""
    global perchance_gen
    if perchance_gen is None:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            perchance_gen = perchance.TextGenerator()
            print("Perchance generator initialized")
        except Exception as e:
            print(f"Warning: Perchance initialization failed: {e}")
            print("Generation will be attempted but may fail")
    return perchance_gen

async def generate_text_async(prompt):
    """Generate text asynchronously"""
    global perchance_gen
    if perchance_gen is None:
        perchance_gen = perchance.TextGenerator()
    
    generated_text = ""
    async for chunk in perchance_gen.text(prompt):
        generated_text += chunk
    return generated_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_girlfriend():
    try:
        data = request.json
        preferences = data.get('preferences', {})
        
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
        generated_text = loop.run_until_complete(generate_text_async(prompt))
        loop.close()
        
        # Parse and structure the generated content
        girlfriend_data = parse_generated_content(generated_text, preferences)
        
        # Save to Supabase
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
        
        return jsonify({
            'success': True,
            'girlfriend': girlfriend_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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
        elif not preferences.get('name') and i == 0 and line[0].isupper():
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

@app.route('/api/girlfriends', methods=['GET'])
def get_girlfriends():
    try:
        result = supabase.table('ai_girlfriends').select('*').order('created_at', desc=True).limit(10).execute()
        return jsonify({
            'success': True,
            'girlfriends': result.data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/girlfriend/<int:girlfriend_id>', methods=['GET'])
def get_girlfriend(girlfriend_id):
    try:
        result = supabase.table('ai_girlfriends').select('*').eq('id', girlfriend_id).execute()
        if result.data:
            return jsonify({
                'success': True,
                'girlfriend': result.data[0]
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Girlfriend not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Initialize Perchance
    try:
        init_perchance_sync()
        print("Perchance generator initialized successfully")
    except Exception as e:
        print(f"Warning: Could not initialize Perchance generator: {e}")
        print("The app will still run, but generation may fail.")
    
    print("\n" + "="*50)
    print("Starting Flask server...")
    print("Server will be available at:")
    print("  - http://localhost:5000")
    print("  - http://127.0.0.1:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

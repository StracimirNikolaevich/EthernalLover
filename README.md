# EthernalLover - AI Girlfriend Generator

A web application that generates AI girlfriends using Perchance AI and stores them in Supabase.

## Features

- 🎨 Customizable AI girlfriend generation
- 💾 Persistent storage with Supabase
- 🎯 Personalized preferences (name, personality, appearance, interests)
- 📱 Responsive design
- 🔄 View recent generations

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Supabase Database

You need to create a table in your Supabase database. Run this SQL in your Supabase SQL editor:

```sql
CREATE TABLE ai_girlfriends (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    personality TEXT,
    appearance TEXT,
    interests TEXT,
    backstory TEXT,
    preferences JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 3. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Configuration

API keys are stored in `API-KEYS.md`. The application uses:
- Supabase for database storage
- Perchance for AI text generation

## Project Structure

```
EthernalLover/
├── app.py                 # Flask backend
├── templates/
│   └── index.html        # Frontend HTML
├── static/
│   ├── style.css         # Styles
│   └── script.js         # Frontend JavaScript
├── requirements.txt      # Python dependencies
├── API-KEYS.md          # API keys and configuration
└── README.md            # This file
```

## Usage

1. Open the application in your browser
2. Fill in your preferences (or leave defaults)
3. Click "Generate AI Girlfriend"
4. View your generated girlfriend and recent generations

## Technologies

- **Backend**: Flask (Python)
- **Database**: Supabase (PostgreSQL)
- **AI Generation**: Perchance
- **Frontend**: HTML, CSS, JavaScript

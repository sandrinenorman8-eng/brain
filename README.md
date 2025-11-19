# Deuxième Cerveau - Backend

Personal knowledge management system with Flask backend, Node.js search service, and AI-powered note organization using Groq LLM.

## Tech Stack

- **Backend**: Flask 3.0.0 (Python)
- **AI**: Groq API (llama-3.3-70b-versatile) for intelligent note fusion
- **Search**: Node.js service on port 3008
- **Storage**: File-based with hierarchical structure
- **Frontend**: Vanilla JS + Tailwind CSS

## Configuration

### 1. Create `config.ini`

```ini
[groq]
api_key = YOUR_GROQ_API_KEY_HERE
```

Get your free API key at: https://console.groq.com/keys

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

```bash
# Start application
START.bat

# Stop application
STOP.bat
```

## Structure

- `app.py` - Main Flask application
- `search-server.js` - Full-text search service
- `category_path_resolver.py` - Path resolution with hierarchy
- `data/` - Notes storage (hierarchical)
- `static/` - Frontend assets

## Features

- **Category-based note organization** with hierarchical structure
- **Full-text search** across all notes
- **AI-powered fusion** - Intelligent note organization and summarization
- **File upload** support for any file type
- **Category management** - Create, merge, delete categories
- **Automatic backups** with timestamped archives

## AI Features

The system uses Groq's LLM to:
- Organize notes by themes and topics
- Generate structured summaries
- Extract action items and key insights
- Merge related notes intelligently

## Ports

- Flask: 5008
- Search: 3008

## Environment Variables

Optional `.env` file support:
```
GROQ_API_KEY=your_key_here
```

Or use `config.ini` (see Configuration section above)

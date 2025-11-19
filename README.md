# Deuxième Cerveau - Backend

Personal knowledge management system with Flask backend and Node.js search service.

## Tech Stack

- **Backend**: Flask 3.0.0 (Python)
- **Search**: Node.js service on port 3008
- **Storage**: File-based with hierarchical structure
- **Frontend**: Vanilla JS + Tailwind CSS

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

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

- Category-based note organization
- Full-text search across all notes
- File upload support
- Category fusion and management
- Automatic backups

## Ports

- Flask: 5008
- Search: 3008

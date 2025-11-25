## Technology Stack

### Backend
- **Flask 3.0.0** (Python web framework)
- **Python 3.x** with standard library (os, json, datetime, zipfile, shutil)
- **requests 2.32.3** for HTTP communication
- **python-dotenv 1.0.0** for environment configuration

### Frontend
- **Vanilla JavaScript** (no framework)
- **Tailwind CSS** (CDN) for styling
- **Font Awesome 6.0.0** for icons
- **Google Fonts** (Manrope, Orbitron)

### Search Service
- **Node.js** with built-in modules (fs, http, path)
- Runs on port 3008 as separate service

### Architecture
- **Flask server** on port 5008 (main application)
- **Node.js search server** on port 3008 (full-text search)
- **File-based storage** in `data/` directory with hierarchical structure
- **JSON configuration** for categories and mappings

## Common Commands

### Starting the Application
```bash
# Windows - Start everything
START.bat

# Manual start (Flask only)
python app.py

# Manual start (Search server)
node search-server.js
```

### Stopping the Application
```bash
# Windows - Stop all services
STOP.bat

# Manual stop - Ctrl+C in respective terminals
```

### Development
```bash
# Install Python dependencies
pip install -r requirements.txt

# Clean up empty folders
python cleanup_empty_folders.py

# Verify endpoints
python verify_endpoints.py

# Update notes data cache
update_notes_data.bat
```

### Testing
```bash
# Run app tests
python app_test.py

# Debug integration
node debug_integration.js

# Check server files
node check_server_files.js
```

### Backup
```bash
# Create complete backup
BACKUP_COMPLET.bat
# Creates timestamped ZIP in zip/ folder
```

## Build System

No build step required - files are served directly. The `START.bat` script copies files from `src/` to root if they exist, but this is optional.

## File Encoding

All text files use **UTF-8 encoding** with fallback support for cp1252, latin-1, and iso-8859-1 for legacy files.

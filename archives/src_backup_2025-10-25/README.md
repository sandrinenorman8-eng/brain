# Source Directory Structure

This is the **source of truth** for the Deuxième Cerveau application.

## Directory Organization

```
src/
├── backend/          # Flask backend application
│   ├── app.py        # Main Flask server
│   ├── categories.json  # Categories configuration
│   └── monitor.py    # File monitoring service
│
├── frontend/         # Frontend HTML/JS files
│   ├── index.html    # Main application interface
│   ├── all_notes_standalone.html  # All notes viewer
│   └── search-server.js  # Node.js search server
│
└── tests/           # Integration tests
    ├── run_integration_tests.bat
    └── test_integration_protocol.ps1
```

## Important Notes

⚠️ **ALWAYS EDIT FILES IN `src/` DIRECTORY**

- The root directory files are **auto-generated copies** from `src/`
- When you run `start_deuxieme_cerveau.bat`, it copies files from `src/` to root
- Editing root files directly will cause them to be overwritten on next startup

## Workflow

1. **Edit source files** in `src/backend/` or `src/frontend/`
2. **Run the startup script** to deploy changes: `start_deuxieme_cerveau.bat`
3. **Test your changes** at http://localhost:5008

## File Mapping

| Source File | Deployed To | Purpose |
|------------|-------------|---------|
| `src/backend/app.py` | `app.py` | Flask API server |
| `src/backend/categories.json` | `categories.json` | Categories data |
| `src/backend/monitor.py` | `monitor.py` | File watcher |
| `src/frontend/index.html` | `index.html` | Main UI |
| `src/frontend/all_notes_standalone.html` | `all_notes_standalone.html` | Notes viewer |
| `src/frontend/search-server.js` | `search-server.js` | Search service |

## Development

- **Backend**: Python Flask (port 5008)
- **Search**: Node.js Express (port 3008)
- **Frontend**: Vanilla JS with Tailwind CSS

## Testing

Run integration tests:
```bash
cd src/tests
.\run_integration_tests.bat
```

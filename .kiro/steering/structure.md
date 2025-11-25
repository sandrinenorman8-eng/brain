## Project Structure

### Root Directory Layout

```
deuxieme_cerveau/
├── app.py                          # Main Flask application
├── category_path_resolver.py       # Path resolution with hierarchy mapping
├── index.html                      # Main UI
├── all_notes_standalone.html       # Standalone notes viewer
├── search-server.js                # Node.js search service
├── START.bat / STOP.bat            # Startup/shutdown scripts
├── requirements.txt                # Python dependencies
├── package.json                    # Node.js metadata
├── categories.json                 # Category definitions (emoji, color)
├── category_mapping.json           # Hierarchical path mappings
├── data/                           # All user notes (hierarchical)
├── static/                         # CSS, JS, images
├── backups/                        # Automatic backups
├── zip/                            # Manual backup archives
├── .kiro/                          # Kiro AI configuration
└── docs/                           # Documentation
```

### Data Directory Structure

The `data/` folder uses a **hierarchical organization** with parent folders:

```
data/
├── buziness/                       # Business-related categories
│   ├── association/
│   ├── idée business/
│   ├── la villa de la paix/
│   ├── lagence/
│   ├── money brick/
│   └── opportunité/
├── cinema/                         # Film/script categories
│   └── scénario/
├── livres/                         # Book-related categories
│   ├── idee philo/
│   ├── motivation/
│   ├── psychologie succès/
│   └── société de livres/
├── logiciels/                      # Software project categories
│   ├── agenda intelligent/
│   ├── brikmagik/
│   ├── chrono brique/
│   ├── kodi brik/
│   ├── memobrik/
│   ├── promptbrik/
│   └── scrap them all/
├── priorité/                       # Priority categories
│   └── todo/
└── series/                         # Series/video categories
    ├── GEN Z/
    └── projet youtube/
```

### Key Modules

**category_path_resolver.py**
- `get_category_path(category_name)` - Returns relative path using mapping
- `get_absolute_category_path(category_name)` - Returns absolute path
- Uses `category_mapping.json` to resolve hierarchical paths

**app.py** - Main Flask routes:
- `/save/<category>` - Save note to category
- `/list/<category>` - List files in category
- `/read/<category>/<filename>` - Read specific file
- `/all_files` - Get all files across categories (cached)
- `/categories` - Get category list
- `/add_category` - Create new category
- `/open_folder/<category>` - Open in Windows Explorer
- `/erase_category/<category>` - Delete category and files
- `/upload_file` - Upload file to category
- `/backup_project` - Create full backup ZIP
- `/search_content` - Proxy to Node.js search
- `/all_notes` - Standalone notes viewer
- `/fusion/global` - Merge all notes

**search-server.js** - Search service:
- `POST /search` - Full-text search with excerpts
- `GET /status` - Server health check

### File Naming Convention

Notes follow the pattern: `{category}_{YYYY-MM-DD}.txt`

Example: `todo_2025-10-24.txt`

Each file contains timestamped entries:
```
HH:MM:SS: Note content here
HH:MM:SS: Another note
```

### Static Assets

```
static/
├── script.js                       # Main frontend logic
├── styles.css                      # Custom styles (if any)
└── images/                         # Icons, backgrounds
```

### Important Conventions

1. **Always use `category_path_resolver.py`** for path resolution - never hardcode paths
2. **Cache invalidation** - Call `_get_all_files_cached.cache_clear()` after data changes
3. **Encoding** - Try UTF-8 first, fallback to cp1252/latin-1 for legacy files
4. **Windows-specific** - Folder opening uses Windows Explorer commands
5. **Port allocation** - Flask on 5008, Search on 3008
6. **Backup location** - All backups go to `zip/` folder with timestamp

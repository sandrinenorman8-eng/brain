# API Documentation

## Base URL

```
http://localhost:5008
```

## Response Format

All API responses follow this format:

### Success Response
```json
{
  "success": true,
  "message": "Success message",
  "data": {},
  "timestamp": "2025-10-25T10:00:00"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "error_type": "ErrorType",
  "timestamp": "2025-10-25T10:00:00"
}
```

## Categories API

### List Categories

```
GET /api/categories
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "name": "scénario",
      "emoji": "🎬",
      "color": "#FF6B6B"
    }
  ]
}
```

### Add Category

```
POST /api/add_category
Content-Type: application/json

{
  "name": "new_category"
}
```

**Validation:**
- Name: 1-19 characters
- Name: lowercase, trimmed
- Name: must be unique

**Response (201):**
```json
{
  "success": true,
  "message": "Category created successfully",
  "data": {
    "name": "new_category",
    "emoji": "📁",
    "color": "#A1B2C3"
  }
}
```

### Delete Category

```
DELETE /api/erase_category/<category>
```

**Response:**
```json
{
  "success": true,
  "message": "Category 'category_name' and all its files have been deleted",
  "data": {
    "category": "category_name"
  }
}
```

## Notes API

### Save Note

```
POST /api/save/<category>
Content-Type: application/json

{
  "text": "Note content"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Note saved successfully",
  "data": {
    "filename": "data/category/category_2025-10-25.txt"
  }
}
```

### List Notes

```
GET /api/list/<category>
```

**Response:**
```json
{
  "success": true,
  "data": [
    "category_2025-10-25.txt",
    "category_2025-10-24.txt"
  ]
}
```

### Read Note

```
GET /api/read/<category>/<filename>
```

**Response:** HTML page with note content

### Get All Files

```
GET /api/all_files
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "category": "scénario",
      "emoji": "🎬",
      "color": "#FF6B6B",
      "filename": "scénario_2025-10-25.txt",
      "date": "2025-10-25",
      "hour": "14:30:45"
    }
  ]
}
```

### Upload File

```
POST /api/upload_file
Content-Type: multipart/form-data

file: <file>
category: <category_name>
```

**Response:**
```json
{
  "success": true,
  "message": "File uploaded successfully",
  "data": {
    "filename": "document.pdf",
    "category": "projets",
    "path": "data/projets/document.pdf",
    "size_kb": 125.5
  }
}
```

## Search API

### Search Content

```
POST /api/search_content
Content-Type: application/json

{
  "term": "search query"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "file": "category_2025-10-25.txt",
        "category": "category",
        "excerpt": "...matching text..."
      }
    ]
  }
}
```

**Error Codes:**
- `503` - Search server unavailable
- `504` - Search server timeout

## Fusion API

### Global Fusion

```
POST /api/fusion/global
```

**Response:**
```json
{
  "success": true,
  "message": "Global fusion successful",
  "data": {
    "filename": "fusion_globale_2025-10-25_14-30-45.txt",
    "filepath": "fusion_global/fusion_globale_2025-10-25_14-30-45.txt",
    "total_files": 42
  }
}
```

### Category Fusion

```
POST /api/fusion/category
Content-Type: application/json

{
  "categories": ["category1", "category2"]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Category fusion successful",
  "data": {
    "filename": "fusion_categories_category1_category2_2025-10-25_14-30-45.txt",
    "filepath": "fusion_categories/...",
    "categories": ["category1", "category2"],
    "total_files": 15
  }
}
```

### Single Category Fusion

```
POST /api/fusion/single-category
Content-Type: application/json

{
  "category": "category_name"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Fusion of category 'category_name' successful",
  "data": {
    "filename": "fusion_category_name_2025-10-25_14-30-45.txt",
    "filepath": "fusion_categories/...",
    "category": "category_name",
    "total_files": 8
  }
}
```

## Utility API

### Open Folder

```
GET /api/open_folder/<category>
```

**Platform:** Windows only

**Response:**
```json
{
  "success": true,
  "message": "Folder opened successfully",
  "data": {
    "path": "G:\\memobrik\\deuxieme_cerveau\\data\\category"
  }
}
```

### Backup Project

```
POST /api/backup_project
```

**Response:**
```json
{
  "success": true,
  "message": "Complete backup created successfully",
  "data": {
    "filename": "backup_memobrik_complet_2025-10-25_14-30-45.zip",
    "path": "G:\\memobrik\\zip\\backup_memobrik_complet_2025-10-25_14-30-45.zip",
    "size_mb": 125.5,
    "date": "2025-10-25_14-30-45",
    "scope": "Complete memobrik folder"
  }
}
```

## Web Pages

### Main Interface

```
GET /
GET /index.html
```

**Response:** HTML page

### All Notes Viewer

```
GET /all_notes
```

**Response:** HTML page with all notes

### All Notes Data

```
GET /all_notes_data
```

**Response:**
```json
{
  "html": "<div>...</div>",
  "categories_count": 10,
  "total_files": 42
}
```

### Static Files

```
GET /static/<filename>
```

**Response:** Static file (CSS, JS, images)

## Error Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable
- `504` - Gateway Timeout

## Rate Limiting

No rate limiting currently implemented.

## Authentication

No authentication currently required.

## CORS

CORS is enabled for all origins.

## Examples

### cURL Examples

**List categories:**
```bash
curl http://localhost:5008/api/categories
```

**Add category:**
```bash
curl -X POST http://localhost:5008/api/add_category \
  -H "Content-Type: application/json" \
  -d '{"name":"test"}'
```

**Save note:**
```bash
curl -X POST http://localhost:5008/api/save/test \
  -H "Content-Type: application/json" \
  -d '{"text":"My note content"}'
```

**Search:**
```bash
curl -X POST http://localhost:5008/api/search_content \
  -H "Content-Type: application/json" \
  -d '{"term":"search query"}'
```

**Upload file:**
```bash
curl -X POST http://localhost:5008/api/upload_file \
  -F "file=@document.pdf" \
  -F "category=projets"
```

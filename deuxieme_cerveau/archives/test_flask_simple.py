#!/usr/bin/env python3
"""
Test simple du serveur Flask
"""

from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/test')
def test():
    return "Flask server is working!"

@app.route('/all_notes')
def all_notes():
    """Test route pour all_notes"""
    try:
        # Vérifier si le fichier standalone existe
        if os.path.exists('all_notes_standalone.html'):
            with open('all_notes_standalone.html', 'r', encoding='utf-8') as f:
                content = f.read()
                return content
        else:
            return """
            <html>
            <head><title>Test Flask</title></head>
            <body>
                <h1>🧪 Test Flask Server</h1>
                <p>✅ Flask server is running on port 5008</p>
                <p>❌ all_notes_standalone.html not found</p>
                <p><a href="/test">Test simple endpoint</a></p>
            </body>
            </html>
            """
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"

@app.route('/all_notes_data')
def all_notes_data():
    """Test API endpoint"""
    return jsonify({
        'status': 'working',
        'message': 'Flask API is functional',
        'files_found': len([f for f in os.listdir('.') if f.endswith('.txt')])
    })

if __name__ == '__main__':
    print("🚀 Starting simple Flask test server...")
    print("📍 Access: http://localhost:5008/all_notes")
    print("🧪 Test: http://localhost:5008/test")
    app.run(debug=True, host='0.0.0.0', port=5008)

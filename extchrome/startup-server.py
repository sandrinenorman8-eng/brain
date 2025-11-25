#!/usr/bin/env python3
"""
Simple startup server that the Chrome extension can call to trigger server startup.
This runs on port 5009 and provides endpoints to start/stop servers.
"""

import os
import sys
import json
import time
import threading
import subprocess
from pathlib import Path
from flask import Flask, jsonify, request

# Add the parent directory to Python path so we can import the startup controller
sys.path.append(str(Path(__file__).parent))

try:
    from startup_controller import ServerStartupController
except ImportError:
    print("[ERROR] Could not import startup_controller")
    sys.exit(1)

app = Flask(__name__)
controller = ServerStartupController()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Startup server is running"})

@app.route('/start-servers', methods=['POST'])
def start_servers():
    """Start the main servers"""
    try:
        print("[INFO] Received request to start servers")

        # Run the startup in a separate thread so we don't block the response
        def run_startup():
            try:
                success = controller.start_all_servers()
                if success:
                    print("[SUCCESS] Servers started successfully")
                else:
                    print("[FAILED] Server startup failed")
            except Exception as e:
                print(f"[ERROR] Exception during server startup: {e}")

        # Start the servers in background
        startup_thread = threading.Thread(target=run_startup, daemon=True)
        startup_thread.start()

        return jsonify({
            "status": "starting",
            "message": "Server startup initiated",
            "servers": ["flask:5008", "search:3008"]
        })

    except Exception as e:
        print(f"[ERROR] Failed to start servers: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/check-servers', methods=['GET'])
def check_servers():
    """Check if servers are running"""
    try:
        flask_running = controller.is_port_open(5008)
        search_running = controller.is_port_open(3008)

        return jsonify({
            "flask": {"port": 5008, "running": flask_running},
            "search": {"port": 3008, "running": search_running},
            "all_running": flask_running and search_running
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/stop-servers', methods=['POST'])
def stop_servers():
    """Stop the servers"""
    try:
        controller.kill_process_on_port(5008)
        controller.kill_process_on_port(3008)
        time.sleep(1)

        return jsonify({"status": "stopped", "message": "Servers stopped"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def main():
    """Main entry point"""
    print("========================================")
    print("CHROME EXTENSION STARTUP SERVER")
    print("========================================")
    print("Endpoints:")
    print("  GET  /health        - Health check")
    print("  POST /start-servers  - Start main servers")
    print("  GET  /check-servers  - Check server status")
    print("  POST /stop-servers   - Stop servers")
    print("========================================")

    # Start the server
    app.run(host='localhost', port=5009, debug=False)

if __name__ == "__main__":
    main()
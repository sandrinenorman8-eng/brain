#!/usr/bin/env python3
"""
Cross-platform server startup controller for Chrome extension.
This script can be called by the Chrome extension to start the required servers.
"""

import os
import sys
import json
import time
import subprocess
import socket
from pathlib import Path

class ServerStartupController:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent / "deuxieme_cerveau"
        self.src_backend = self.base_dir / "src" / "backend"
        self.src_frontend = self.base_dir / "src" / "frontend"

    def check_python(self):
        """Check if Python is available"""
        try:
            result = subprocess.run([sys.executable, "--version"],
                                  capture_output=True, text=True, check=True)
            print(f"[OK] Python found: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("[ERROR] Python not found")
            return False

    def check_node(self):
        """Check if Node.js is available"""
        try:
            result = subprocess.run(["node", "--version"],
                                  capture_output=True, text=True, check=True)
            print(f"[OK] Node.js found: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("[ERROR] Node.js not found")
            return False

    def copy_src_files(self):
        """Copy files from src directories"""
        try:
            if self.src_backend.exists():
                # Copy Python files
                for py_file in self.src_backend.glob("*.py"):
                    import shutil
                    shutil.copy2(py_file, self.base_dir)
                # Copy JSON files
                for json_file in self.src_backend.glob("*.json"):
                    import shutil
                    shutil.copy2(json_file, self.base_dir)
                print("[OK] Backend files copied")
            else:
                print("[ERROR] src/backend not found")
                return False

            if self.src_frontend.exists():
                # Copy HTML files
                for html_file in self.src_frontend.glob("*.html"):
                    import shutil
                    shutil.copy2(html_file, self.base_dir)
                # Copy JS files
                for js_file in self.src_frontend.glob("*.js"):
                    import shutil
                    shutil.copy2(js_file, self.base_dir)
                print("[OK] Frontend files copied")
            else:
                print("[ERROR] src/frontend not found")
                return False

            return True
        except Exception as e:
            print(f"[ERROR] Failed to copy files: {e}")
            return False

    def kill_process_on_port(self, port):
        """Kill process running on specified port"""
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if f":{port}" in line and "LISTENING" in line:
                        pid = line.strip().split()[-1]
                        subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                        print(f"[OK] Killed process {pid} on port {port}")
                        return True
            else:  # Unix-like systems
                result = subprocess.run(['lsof', '-ti', f":{port}"], capture_output=True, text=True)
                if result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        if pid:
                            subprocess.run(['kill', '-9', pid], capture_output=True)
                            print(f"[OK] Killed process {pid} on port {port}")
                    return True
            return False
        except Exception as e:
            print(f"[ERROR] Failed to kill process on port {port}: {e}")
            return False

    def is_port_open(self, port):
        """Check if port is open"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            return result == 0

    def start_search_server(self):
        """Start the Node.js search server"""
        try:
            search_server = self.base_dir / "search-server-fixed.js"
            if not search_server.exists():
                print(f"[ERROR] Search server not found: {search_server}")
                return False

            # Start in background
            if os.name == 'nt':  # Windows
                subprocess.Popen(
                    ['node', str(search_server)],
                    cwd=self.base_dir,
                    creationflags=subprocess.DETACHED_PROCESS
                )
            else:  # Unix-like
                subprocess.Popen(
                    ['node', str(search_server)],
                    cwd=self.base_dir,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            print("[OK] Search server started on port 3008")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to start search server: {e}")
            return False

    def start_flask_server(self):
        """Start the Flask server"""
        try:
            app_file = self.base_dir / "app.py"
            if not app_file.exists():
                print(f"[ERROR] Flask app not found: {app_file}")
                return False

            # Flask server will run in foreground and block
            print("[OK] Starting Flask server on port 5008")
            result = subprocess.run([sys.executable, str(app_file)], cwd=self.base_dir)
            return result.returncode == 0
        except Exception as e:
            print(f"[ERROR] Failed to start Flask server: {e}")
            return False

    def wait_for_servers(self, timeout=30):
        """Wait for servers to be ready"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_port_open(3008) and self.is_port_open(5008):
                print("[OK] Both servers are ready")
                return True
            time.sleep(1)

        print("[ERROR] Servers not ready within timeout")
        return False

    def start_all_servers(self):
        """Main method to start all servers"""
        print("========================================")
        print("SERVER STARTUP CONTROLLER")
        print("========================================")

        # Check requirements
        if not self.check_python() or not self.check_node():
            return False

        # Copy source files
        if not self.copy_src_files():
            return False

        # Kill existing processes
        print("[INFO] Cleaning up existing processes...")
        self.kill_process_on_port(5008)
        self.kill_process_on_port(3008)
        time.sleep(1)

        # Start servers
        if not self.start_search_server():
            return False

        time.sleep(2)  # Give search server time to start

        if not self.wait_for_servers():
            return False

        print("========================================")
        print("SERVERS ACTIVE:")
        print("  - Flask:    http://localhost:5008")
        print("  - Search:   http://localhost:3008")
        print("========================================")

        return True

def main():
    controller = ServerStartupController()
    success = controller.start_all_servers()

    if success:
        print("[SUCCESS] All servers started successfully")
        return 0
    else:
        print("[FAILED] Server startup failed")
        return 1

if __name__ == "__main__":
    exit(main())
#!/usr/bin/env python3
"""
Monitor script for Deuxième Cerveau Flask application
Tests endpoints and monitors logs
"""

import requests
import time
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AppMonitor:
    def __init__(self, base_url="http://localhost:5008"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 10

    def test_endpoint(self, endpoint, method="GET", data=None, expected_status=200):
        """Test a specific endpoint"""
        url = f"{self.base_url}{endpoint}"
        try:
            if method == "GET":
                response = self.session.get(url)
            elif method == "POST":
                response = self.session.post(url, json=data)
            else:
                logger.error(f"Unsupported method: {method}")
                return False

            if response.status_code == expected_status:
                logger.info(f"✅ {method} {endpoint} - Status: {response.status_code}")
                return True, response
            else:
                logger.error(f"❌ {method} {endpoint} - Status: {response.status_code}, Response: {response.text[:200]}")
                return False, response
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ {method} {endpoint} - Connection Error: {e}")
            return False, None

    def test_all_endpoints(self):
        """Test all known endpoints"""
        logger.info("🔍 Testing all endpoints...")

        # Test root endpoint
        self.test_endpoint("/")

        # Test static files
        self.test_endpoint("/static/index.html")
        self.test_endpoint("/static/style.css")
        self.test_endpoint("/static/script.js")

        # Test API endpoints
        success, response = self.test_endpoint("/categories")
        if success and response:
            try:
                categories = response.json()
                logger.info(f"📂 Found {len(categories)} categories")

                # Test saving to each category
                for category in categories[:2]:  # Test first 2 categories
                    test_data = {"text": f"Test note from monitor at {datetime.now()}"}
                    self.test_endpoint(f"/save/{category['name']}", "POST", test_data)
            except json.JSONDecodeError:
                logger.error("Failed to parse categories JSON")

        # Test file operations
        self.test_endpoint("/api/files/scénario")

    def check_html_structure(self):
        """Check if HTML file has proper structure"""
        html_file = "index.html"
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            checks = [
                ("DOCTYPE", "<!DOCTYPE html>" in content),
                ("HTML tag", "<html>" in content and "</html>" in content),
                ("Head tag", "<head>" in content and "</head>" in content),
                ("Body tag", "<body>" in content and "</body>" in content),
                ("CSS link", '<link rel="stylesheet" href="style.css">' in content),
                ("JS script", '<script src="script.js"></script>' in content),
                ("No embedded CSS", "<style>" not in content),
                ("No embedded JS", "<script>" in content and 'src="script.js"' in content)
            ]

            logger.info("🔧 HTML Structure Check:")
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                logger.info(f"  {status} {check_name}")

            # Check file size
            size_kb = len(content) / 1024
            logger.info(".1f")

            return all(passed for _, passed in checks)
        else:
            logger.error(f"❌ HTML file not found: {html_file}")
            return False

    def monitor_loop(self, interval=30):
        """Main monitoring loop"""
        logger.info("🚀 Starting Deuxième Cerveau Monitor")
        logger.info(f"📡 Monitoring {self.base_url}")
        logger.info(f"⏱️  Check interval: {interval} seconds")

        while True:
            try:
                # Check HTML structure
                html_ok = self.check_html_structure()

                # Test endpoints if HTML is OK
                if html_ok:
                    self.test_all_endpoints()
                else:
                    logger.warning("⚠️  HTML structure issues detected, skipping endpoint tests")

                logger.info(f"💤 Waiting {interval} seconds...")
                time.sleep(interval)

            except KeyboardInterrupt:
                logger.info("🛑 Monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"💥 Monitor error: {e}")
                time.sleep(interval)

if __name__ == "__main__":
    monitor = AppMonitor()
    monitor.monitor_loop()

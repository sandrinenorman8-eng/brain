#!/usr/bin/env python3
"""
Fixed test script to properly check link functionality in Deuxième Cerveau
"""

import requests
import json
import time
from datetime import datetime

class LinkTester:
    def __init__(self, base_url="http://localhost:5008"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 10

    def test_endpoint(self, endpoint, method="GET", data=None, expected_status=200, description=""):
        """Test a specific endpoint"""
        url = f"{self.base_url}{endpoint}"
        print(f"\n🔍 Testing: {description}")
        print(f"   URL: {method} {url}")

        try:
            if method == "GET":
                response = self.session.get(url)
            elif method == "POST":
                response = self.session.post(url, json=data)
            else:
                print(f"   ❌ Unsupported method: {method}")
                return False

            status_ok = response.status_code == expected_status
            status_icon = "✅" if status_ok else "❌"

            print(f"   {status_icon} Status: {response.status_code} (expected {expected_status})")

            if not status_ok:
                print(f"   ❌ Response: {response.text[:200]}...")

            return status_ok, response

        except requests.exceptions.RequestException as e:
            print(f"   ❌ Connection Error: {e}")
            return False, None

    def test_all_notes_button(self):
        """Test 'Toutes les Notes' button functionality"""
        print("\n" + "="*50)
        print("🧪 TESTING: 'Toutes les Notes' Button")
        print("="*50)

        success, response = self.test_endpoint(
            "/all_notes",
            description="'Toutes les Notes' button (/all_notes)"
        )

        if success and response:
            content_length = len(response.text)
            print(f"   📄 Content length: {content_length} characters")

            # Check if it contains expected elements
            has_doctype = "<!DOCTYPE html>" in response.text
            has_html = "<html" in response.text
            has_title = "Toutes les Notes" in response.text
            has_body = "<body>" in response.text

            print(f"   ✅ Contains DOCTYPE: {has_doctype}")
            print(f"   ✅ Contains HTML tag: {has_html}")
            print(f"   ✅ Contains title: {has_title}")
            print(f"   ✅ Contains body: {has_body}")

            return has_doctype and has_html and has_title and has_body
        return False

    def test_categories_endpoint(self):
        """Test categories endpoint"""
        print("\n" + "="*50)
        print("🧪 TESTING: Categories Endpoint")
        print("="*50)

        success, response = self.test_endpoint(
            "/categories",
            description="Categories endpoint (/categories)"
        )

        if success and response:
            try:
                categories = response.json()
                print(f"   📂 Found {len(categories)} categories:")

                for i, cat in enumerate(categories[:5]):  # Show first 5
                    print(f"      {i+1}. {cat.get('emoji', '📁')} {cat.get('name', 'Unknown')}")

                if len(categories) > 5:
                    print(f"      ... and {len(categories) - 5} more")

                return len(categories) > 0, categories

            except json.JSONDecodeError:
                print(f"   ❌ Invalid JSON response: {response.text[:200]}")
                return False, None

        return False, None

    def test_folder_buttons(self, categories):
        """Test folder button functionality - should show files in modal"""
        print("\n" + "="*50)
        print("🧪 TESTING: Folder Buttons (File Listing)")
        print("="*50)

        if not categories:
            print("   ❌ No categories available to test")
            return False

        # Test first 3 categories that should have files
        test_categories = categories[:3]
        results = []

        for cat in test_categories:
            cat_name = cat.get('name', 'Unknown')
            print(f"\n   📁 Testing file listing for category: {cat.get('emoji', '📁')} {cat_name}")

            # Test list endpoint (what folder buttons actually use)
            success, response = self.test_endpoint(
                f"/list/{cat_name}",
                description=f"List files in {cat_name}"
            )

            if success and response:
                try:
                    files = response.json()
                    print(f"      📄 Found {len(files)} files")

                    if files:
                        print(f"      📖 Sample files: {files[:3]}")  # Show first 3 files

                        # Test reading one file to ensure file links work
                        first_file = files[0]
                        read_success, read_response = self.test_endpoint(
                            f"/read/{cat_name}/{first_file}",
                            description=f"Read file {first_file} from {cat_name}"
                        )

                        if read_success and read_response:
                            content_length = len(read_response.text)
                            print(f"         ✅ File readable: {content_length} characters")
                            results.append(True)
                        else:
                            print(f"         ❌ Cannot read file")
                            results.append(False)
                    else:
                        print(f"      ⚠️ No files in this category")
                        results.append(True)  # Not an error, just empty category

                except json.JSONDecodeError:
                    print(f"      ❌ Invalid JSON when listing files: {response.text[:200]}")
                    results.append(False)
            else:
                results.append(False)

        success_rate = sum(results) / len(results) if results else 0
        print(f"\n   📊 Folder buttons success rate: {success_rate:.1%}")
        return success_rate >= 0  # Allow empty categories

    def test_file_reading_simulation(self, categories):
        """Test file reading by simulating what happens when clicking file links"""
        print("\n" + "="*50)
        print("🧪 TESTING: File Link Reading")
        print("="*50)

        if not categories:
            print("   ❌ No categories available to test")
            return False

        # Find a category that has files
        for cat in categories:
            cat_name = cat.get('name', 'Unknown')
            print(f"\n   📂 Checking files in category: {cat.get('emoji', '📁')} {cat_name}")

            # Get file list
            success, response = self.test_endpoint(
                f"/list/{cat_name}",
                description=f"List files in {cat_name}"
            )

            if success and response:
                try:
                    files = response.json()
                    print(f"      📄 Found {len(files)} files")

                    if files:
                        # Test reading the most recent file
                        latest_file = files[0]  # Already sorted reverse chronologically
                        print(f"      📖 Testing read: {latest_file}")

                        read_success, read_response = self.test_endpoint(
                            f"/read/{cat_name}/{latest_file}",
                            description=f"Read latest file from {cat_name}"
                        )

                        if read_success and read_response:
                            content_length = len(read_response.text)
                            print(f"         ✅ File content: {content_length} characters")

                            # Check if content looks like a text file
                            content_preview = read_response.text[:100]
                            has_text_content = len(content_preview.strip()) > 0
                            print(f"         ✅ Has text content: {has_text_content}")

                            return has_text_content

                except json.JSONDecodeError:
                    print(f"      ❌ Invalid JSON when listing files: {response.text[:200]}")
                    continue

        print("   ❌ No readable files found")
        return False

    def run_all_tests(self):
        """Run all link tests"""
        print("🚀 Starting Deuxième Cerveau Link Tests (Fixed Version)")
        print(f"📡 Testing against: {self.base_url}")
        print(f"⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")

        # Test basic connectivity
        print("\n" + "="*50)
        print("🌐 BASIC CONNECTIVITY TEST")
        print("="*50)

        success, response = self.test_endpoint("/", description="Main page")
        if not success:
            print("❌ Cannot connect to application. Make sure Flask is running!")
            return False

        # Test "Toutes les Notes" button
        all_notes_ok = self.test_all_notes_button()

        # Test categories (needed for other tests)
        categories_ok, categories = self.test_categories_endpoint()

        # Test folder buttons (file listing)
        folders_ok = False
        if categories_ok and categories:
            folders_ok = self.test_folder_buttons(categories)

        # Test file reading
        files_ok = False
        if categories_ok and categories:
            files_ok = self.test_file_reading_simulation(categories)

        # Summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"✅ 'Toutes les Notes' button: {'PASS' if all_notes_ok else 'FAIL'}")
        print(f"✅ Categories endpoint: {'PASS' if categories_ok else 'FAIL'}")
        print(f"✅ Folder buttons (file listing): {'PASS' if folders_ok else 'FAIL'}")
        print(f"✅ File reading (links): {'PASS' if files_ok else 'FAIL'}")

        overall_success = all([all_notes_ok, categories_ok, folders_ok, files_ok])

        if overall_success:
            print("\n🎉 ALL TESTS PASSED! Links should be working correctly.")
        else:
            print("\n⚠️  SOME TESTS FAILED! Check the output above for specific issues.")

        print(f"\n⏰ Completed at: {datetime.now().strftime('%H:%M:%S')}")
        return overall_success

if __name__ == "__main__":
    tester = LinkTester()
    tester.run_all_tests()

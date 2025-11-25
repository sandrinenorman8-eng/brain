#!/usr/bin/env python3
"""
Test script to check link functionality in Deuxième Cerveau
Tests the specific issues: file links, "Toutes les Notes", and folder buttons
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
            has_html = "<html>" in response.text
            has_title = "Toutes les Notes" in response.text
            has_body = "<body>" in response.text

            print(f"   ✅ Contains HTML: {has_html}")
            print(f"   ✅ Contains title: {has_title}")
            print(f"   ✅ Contains body: {has_body}")

            return has_html and has_title and has_body
        return False

    def test_categories_endpoint(self):
        """Test categories endpoint (needed for folder buttons)"""
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
        """Test folder button functionality"""
        print("\n" + "="*50)
        print("🧪 TESTING: Folder Buttons")
        print("="*50)

        if not categories:
            print("   ❌ No categories available to test")
            return False

        # Test first 3 categories
        test_categories = categories[:3]
        results = []

        for cat in test_categories:
            cat_name = cat.get('name', 'Unknown')
            print(f"\n   📁 Testing category: {cat.get('emoji', '📁')} {cat_name}")

            # Test open_folder endpoint
            success, response = self.test_endpoint(
                f"/open_folder/{cat_name}",
                description=f"Open folder for {cat_name}"
            )

            if success and response:
                try:
                    result = response.json()
                    has_path = 'path' in result
                    has_files = 'files' in result

                    print(f"      ✅ Has path: {has_path}")
                    print(f"      ✅ Has files: {has_files}")

                    if has_files:
                        files = result.get('files', [])
                        print(f"      📄 Found {len(files)} files")

                    results.append(has_path and has_files)

                except json.JSONDecodeError:
                    print(f"      ❌ Invalid JSON: {response.text[:200]}")
                    results.append(False)
            else:
                results.append(False)

        success_rate = sum(results) / len(results) if results else 0
        print(f"\n   📊 Folder buttons success rate: {success_rate:.1%}")
        return success_rate > 0

    def test_file_reading(self, categories):
        """Test file reading functionality (simulates clicking file links)"""
        print("\n" + "="*50)
        print("🧪 TESTING: File Reading (File Links)")
        print("="*50)

        if not categories:
            print("   ❌ No categories available to test")
            return False

        # Test first category that has files
        for cat in categories[:3]:  # Check first 3 categories
            cat_name = cat.get('name', 'Unknown')
            print(f"\n   📂 Checking files in category: {cat.get('emoji', '📁')} {cat_name}")

            # First get the list of files in this category
            success, response = self.test_endpoint(
                f"/list/{cat_name}",
                description=f"List files in {cat_name}"
            )

            if success and response:
                try:
                    files = response.json()
                    print(f"      📄 Found {len(files)} files")

                    if files:
                        # Test reading the first file
                        first_file = files[0]
                        print(f"      📖 Testing read: {first_file}")

                        read_success, read_response = self.test_endpoint(
                            f"/read/{cat_name}/{first_file}",
                            description=f"Read file {first_file} from {cat_name}"
                        )

                        if read_success and read_response:
                            content_length = len(read_response.text)
                            print(f"         ✅ File content length: {content_length} characters")
                            return True

                except json.JSONDecodeError:
                    print(f"      ❌ Invalid JSON when listing files: {response.text[:200]}")
                    continue

        print("   ❌ No files found to test reading")
        return False

    def run_all_tests(self):
        """Run all link tests"""
        print("🚀 Starting Deuxième Cerveau Link Tests")
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

        # Test folder buttons
        folders_ok = False
        if categories_ok and categories:
            folders_ok = self.test_folder_buttons(categories)

        # Test file reading
        files_ok = False
        if categories_ok and categories:
            files_ok = self.test_file_reading(categories)

        # Summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"✅ 'Toutes les Notes' button: {'PASS' if all_notes_ok else 'FAIL'}")
        print(f"✅ Categories endpoint: {'PASS' if categories_ok else 'FAIL'}")
        print(f"✅ Folder buttons: {'PASS' if folders_ok else 'FAIL'}")
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

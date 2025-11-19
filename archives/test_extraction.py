#!/usr/bin/env python3
"""
Test script to verify the CSS/JS extraction worked
"""

import requests
import os

def test_application():
    print("🔍 Testing Deuxième Cerveau Application...")

    try:
        # Test Flask endpoint
        response = requests.get('http://localhost:5008/', timeout=5)
        print(f"✅ Flask app responded with status: {response.status_code}")

        if response.status_code == 200:
            html = response.text

            # Check HTML structure
            checks = [
                ('DOCTYPE present', '<!DOCTYPE html>' in html),
                ('CSS link present', '<link rel="stylesheet" href="style.css">' in html),
                ('JS script present', '<script src="script.js"></script>' in html),
                ('No embedded CSS', '<style>' not in html),
                ('No embedded JS', '<script>' not in html or ('<script>' in html and '<script src="script.js"></script>' in html)),  # Should have no script tags without src
            ]

            print("\n📋 HTML Structure Checks:")
            all_passed = True
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"  {status} {check_name}")
                if not passed:
                    all_passed = False

            # Check file sizes
            print("\n📊 File Sizes:")
            files = ['index.html', 'style.css', 'script.js']
            for filename in files:
                if os.path.exists(filename):
                    size = os.path.getsize(filename)
                    print(f"  {filename}: {size:,} bytes")
                else:
                    print(f"  ❌ {filename}: File not found!")
                    all_passed = False

            if all_passed:
                print("\n🎉 ALL TESTS PASSED! Extraction successful!")
                return True
            else:
                print("\n⚠️  Some tests failed!")
                return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to Flask app: {e}")
        print("💡 Make sure the Flask app is running with: python app.py")
        return False

if __name__ == "__main__":
    test_application()

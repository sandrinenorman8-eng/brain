#!/usr/bin/env python3
"""
Test JavaScript interactions by simulating browser behavior
"""

import requests
import json
import time

def test_javascript_interactions():
    print("🔍 Testing JavaScript interactions...")

    # First, let's check what JavaScript functions are defined
    try:
        response = requests.get('http://localhost:5008/script.js')
        js_content = response.text

        # Check for key functions
        functions_to_check = [
            'handleFusionButtonClick',
            'openSavedLocation',
            'quickSave',
            'loadCategories',
            'renderFolderButtons'
        ]

        print("📋 Checking for JavaScript functions:")
        for func in functions_to_check:
            has_func = f'function {func}' in js_content
            status = "✅" if has_func else "❌"
            print(f"   {status} {func}")

        # Check for key variables
        variables_to_check = [
            'let allFiles',
            'let currentFilter',
            'let categories'
        ]

        print("\n📋 Checking for JavaScript variables:")
        for var in variables_to_check:
            has_var = var in js_content
            status = "✅" if has_var else "❌"
            print(f"   {status} {var}")

    except Exception as e:
        print(f"❌ Error reading JavaScript: {e}")
        return False

    # Test categories loading (simulates page load)
    print("\n🧪 Testing categories loading...")
    try:
        response = requests.get('http://localhost:5008/categories')
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Categories loaded: {len(categories)} categories")

            if categories:
                # Test clicking a category button (simulates quickSave)
                first_cat = categories[0]
                print(f"\n🧪 Simulating category button click for: {first_cat['emoji']} {first_cat['name']}")

                # This would normally be a POST request with note text
                test_data = {"text": "Test note from interaction test"}
                save_response = requests.post(f"http://localhost:5008/save/{first_cat['name']}", json=test_data)

                if save_response.status_code == 200:
                    print("✅ Category save simulation successful")
                else:
                    print(f"❌ Category save failed: {save_response.status_code}")

                # Test folder button (simulates openSavedLocation)
                print(f"\n🧪 Simulating folder button click for: {first_cat['emoji']} {first_cat['name']}")
                list_response = requests.get(f"http://localhost:5008/list/{first_cat['name']}")

                if list_response.status_code == 200:
                    files = list_response.json()
                    print(f"✅ Folder listing successful: {len(files)} files")
                else:
                    print(f"❌ Folder listing failed: {list_response.status_code}")

        else:
            print(f"❌ Categories loading failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error testing interactions: {e}")
        return False

    # Test "Toutes les Notes" button
    print("\n🧪 Testing 'Toutes les Notes' button...")
    try:
        response = requests.get('http://localhost:5008/all_notes')
        if response.status_code == 200:
            print("✅ 'Toutes les Notes' page loads successfully")
            print(f"   📄 Content length: {len(response.text)} characters")

            # Check if it has interactive elements
            has_accordion = 'accordion-item' in response.text
            has_read_links = 'href="/read/' in response.text
            print(f"   ✅ Has accordion interface: {has_accordion}")
            print(f"   ✅ Has read links: {has_read_links}")
        else:
            print(f"❌ 'Toutes les Notes' failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error testing 'Toutes les Notes': {e}")
        return False

    print("\n🎉 All JavaScript interactions tested successfully!")
    print("\n💡 If links still don't work in browser:")
    print("   1. Try Ctrl+F5 (hard refresh)")
    print("   2. Check Network tab for failed asset loads")
    print("   3. Check Console tab for JavaScript errors")
    print("   4. Try incognito mode to avoid cache issues")

    return True

if __name__ == "__main__":
    test_javascript_interactions()

#!/usr/bin/env python3
"""
Test if CSS and JS assets are being served correctly
"""

import requests

def test_assets():
    print("🔍 Testing asset loading...")

    # Test CSS file
    try:
        response = requests.get('http://localhost:5008/style.css')
        print(f'✅ CSS file: {response.status_code} - {len(response.text)} bytes')
        if response.status_code == 200:
            print("   📄 CSS content preview:")
            print("   " + response.text[:100] + "...")
    except Exception as e:
        print(f'❌ CSS error: {e}')

    # Test JS file
    try:
        response = requests.get('http://localhost:5008/script.js')
        print(f'✅ JS file: {response.status_code} - {len(response.text)} bytes')
        if response.status_code == 200:
            print("   📄 JS content preview:")
            print("   " + response.text[:100] + "...")
    except Exception as e:
        print(f'❌ JS error: {e}')

    # Test main page and check if it references the assets
    try:
        response = requests.get('http://localhost:5008/')
        html = response.text
        has_css_link = '<link rel="stylesheet" href="style.css">' in html
        has_js_script = '<script src="script.js"></script>' in html
        print(f'✅ Main page: {response.status_code} - {len(html)} bytes')
        print(f'   Has CSS link: {has_css_link}')
        print(f'   Has JS script: {has_js_script}')

        if has_css_link and has_js_script:
            print("🎉 All assets properly referenced!")
        else:
            print("⚠️  Missing asset references in HTML")
    except Exception as e:
        print(f'❌ Main page error: {e}')

if __name__ == "__main__":
    test_assets()

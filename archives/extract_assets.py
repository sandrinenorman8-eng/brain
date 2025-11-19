#!/usr/bin/env python3
"""
Extract CSS and JS from HTML file and create external files
"""

import re

def extract_css_and_js():
    # Read the HTML file
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Original HTML file size: {len(content)} characters")

    # Extract CSS between <style> and </style>
    css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if css_match:
        css_content = css_match.group(1).strip()

        # Write CSS to style.css
        with open('style.css', 'w', encoding='utf-8') as f:
            f.write(css_content)

        print(f'✅ Extracted {len(css_content)} characters of CSS to style.css')

        # Remove the <style> block from HTML
        content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
        print('✅ Removed embedded CSS from HTML')
    else:
        print('❌ No CSS found in HTML file')

    # Extract JS between <script> and </script> (excluding external script tags)
    # Find all script tags that don't have src attribute
    script_pattern = r'<script>(.*?)</script>'
    scripts = re.findall(script_pattern, content, re.DOTALL)

    if scripts:
        # Combine all embedded scripts
        js_content = '\n'.join(script.strip() for script in scripts if script.strip())

        # Write JS to script.js
        with open('script.js', 'w', encoding='utf-8') as f:
            f.write(js_content)

        print(f'✅ Extracted {len(js_content)} characters of JS to script.js')

        # Remove embedded script blocks (but keep external script tags)
        content = re.sub(r'<script>(.*?)</script>', '', content, flags=re.DOTALL)
        print('✅ Removed embedded JS from HTML')
    else:
        print('❌ No embedded JS found in HTML file')

    # Add CSS link in head if not already present
    if '<link rel="stylesheet" href="style.css">' not in content:
        # Find head section and add CSS link after title
        head_pattern = r'(<head>.*?<title>.*?</title>)(.*?</head>)'
        match = re.search(head_pattern, content, re.DOTALL)
        if match:
            before_title, after_head = match.groups()
            new_head_start = before_title + '\n    <link rel="stylesheet" href="style.css">'
            content = content.replace(match.group(0), new_head_start + after_head)
            print('✅ Added CSS link to HTML head')

    # Add JS script tag before closing body if not already present
    if '<script src="script.js"></script>' not in content:
        # Find closing body tag and add script before it
        body_end_pattern = r'(</body>)'
        if re.search(body_end_pattern, content):
            content = re.sub(body_end_pattern, '    <script src="script.js"></script>\n\\1', content)
            print('✅ Added JS script link before closing body tag')

    # Write back the modified HTML
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Updated HTML file size: {len(content)} characters")
    print("🎉 Asset extraction completed!")

if __name__ == "__main__":
    extract_css_and_js()

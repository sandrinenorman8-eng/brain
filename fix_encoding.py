#!/usr/bin/env python3
"""
Script to fix encoding issues in existing files
"""

import os
import glob

def fix_file_encoding(filepath):
    """Fix encoding issues in a file"""
    try:
        print(f"🔧 Fixing encoding in: {filepath}")

        # Try different encodings
        encodings_to_try = ['utf-8', 'utf-8-sig', 'cp1252', 'latin-1', 'iso-8859-1']

        for encoding in encodings_to_try:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Warning: Error reading {filepath} with {encoding}: {e}")
                continue

        if content is None:
            print(f"❌ Could not read {filepath}")
            return

        # Fix problematic characters - multiple passes for better coverage
        replacements = {
            # Common French characters
            '�': 'é', '�': 'à', '�': 'â', '�': 'ê', '�': 'î', '�': 'ô',
            '�': 'û', '�': 'ç', '�': 'ë', '�': 'ï', '�': 'ü',
            'Ã§': 'ç', 'Ã©': 'é', 'Ã': 'à', 'Ã¢': 'â', 'Ãª': 'ê', 'Ã®': 'î',
            'Ã´': 'ô', 'Ã»': 'û', 'Ã«': 'ë', 'Ã¯': 'ï', 'Ã¼': 'ü',

            # Special characters and formatting
            'â€‹': ' ', 'â€': '"', 'â€œ': '"', 'â€¢': '"', 'â€': "'",
            'â€™': "'", 'â€¢': '•', 'â€"': '–', 'â€¢': '…', 'â€¢': '™', 'â€¢': '®',
            'â€¢': '™', 'â€¢': '®', 'â€¢': '•', 'â€¢': '–', 'â€¢': '…',
            '├': '', 'â': "'", '€': '€', '™': '™', '®': '®',

            # Additional problematic sequences - more comprehensive
            '├â': 'à', '├â€': 'à', '├â€¢': 'à', '├â€œ': 'à', '├â€™': 'à',
            '├é': 'é', '├â€': 'é', '├â€¢': 'é', '├â€œ': 'é', '├â€™': 'é',
            '├ç': 'ç', '├â€': 'ç', '├â€¢': 'ç', '├â€œ': 'ç', '├â€™': 'ç',
            '├ï': 'ï', '├â€': 'ï', '├â€¢': 'ï', '├â€œ': 'ï', '├â€™': 'ï',
            '├»': 'û', '├â€': 'û', '├â€¢': 'û', '├â€œ': 'û', '├â€™': 'û',
            '├º': 'à', '├©': 'é', '├®': '®', '├™': '™', '├«': '«', '├»': '»',
            '├ó': 'ó', '├¡': 'í', '├³': 'ó', '├º': 'ú', '├±': 'ñ',
            '├': '', 'â': "'", '€': '€', '™': '™', '®': '®', '•': '•', '–': '–', '—': '—', '…': '…',
        }

        for old, new in replacements.items():
            content = content.replace(old, new)

        # Write back with proper encoding
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Fixed encoding in: {filepath}")
        return True

    except Exception as e:
        print(f"❌ Error fixing {filepath}: {e}")
        return False

def main():
    """Fix encoding in all text files in scenario folder"""
    scenario_folder = "deuxieme_cerveau/scénario"

    if not os.path.exists(scenario_folder):
        print(f"❌ Folder not found: {scenario_folder}")
        return

    print(f"🔍 Scanning folder: {scenario_folder}")

    # Find all .txt files
    txt_files = glob.glob(os.path.join(scenario_folder, "*.txt"))

    print(f"📁 Found {len(txt_files)} text files")

    fixed_count = 0
    for filepath in txt_files:
        if fix_file_encoding(filepath):
            fixed_count += 1

    print("\n🎉 Encoding fix completed!")
    print(f"✅ Fixed {fixed_count} out of {len(txt_files)} files")

if __name__ == "__main__":
    main()

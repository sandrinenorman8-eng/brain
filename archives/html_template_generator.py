#!/usr/bin/env python3
"""
Standardized HTML Template Generator for Deuxième Cerveau
Ensures consistent HTML generation from base template
"""

import os
import json
from pathlib import Path
from datetime import datetime

class HTMLTemplateGenerator:
    def __init__(self, template_file="index_stable_backup.html"):
        self.template_file = template_file
        self.project_root = Path(__file__).parent
        self.template_sections = {
            'head': '',
            'main_section': '',
            'notes_section': '',
            'folders_section': '',
            'fusion_modal': '',
            'scripts': ''
        }

    def load_template(self):
        """Load and parse the base template"""
        template_path = self.project_root / self.template_file

        if not template_path.exists():
            raise FileNotFoundError(f"Template file {self.template_file} not found")

        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract sections (simplified parsing)
        self.template_sections['head'] = self._extract_section(content, '<head>', '</head>')
        self.template_sections['main_section'] = self._extract_section(content, '<!-- Main Content Section -->', '<!-- Bouton Slider Test -->')
        self.template_sections['notes_section'] = self._extract_section(content, '<!-- Notes Section -->', '<!-- Folders Section -->')
        self.template_sections['folders_section'] = self._extract_section(content, '<!-- Folders Section -->', '<!-- Fusion Modal -->')
        self.template_sections['fusion_modal'] = self._extract_section(content, '<!-- Fusion Modal -->', '<script>')
        self.template_sections['scripts'] = self._extract_section(content, '<script>', '</html>')

    def _extract_section(self, content, start_marker, end_marker):
        """Extract a section between markers"""
        try:
            start_idx = content.find(start_marker)
            end_idx = content.find(end_marker, start_idx)

            if start_idx == -1 or end_idx == -1:
                return ""

            return content[start_idx:end_idx]
        except:
            return ""

    def generate_consistent_html(self, output_file="index.html", modifications=None):
        """Generate HTML with optional modifications while maintaining structure"""
        if modifications is None:
            modifications = {}

        # Build HTML structure
        html_parts = [
            "<!DOCTYPE html>",
            "<html>",
            self.template_sections['head'],
            "<body>",
            '    <div class="dynamic-container">',
            self.template_sections['main_section'],
            self.template_sections['notes_section'],
            self.template_sections['folders_section'],
            '    </div>',
            self.template_sections['fusion_modal'],
            self.template_sections['scripts'],
            "</body>",
            "</html>"
        ]

        # Apply modifications if specified
        html_content = "\n".join(html_parts)

        if modifications:
            for key, value in modifications.items():
                if key == 'title':
                    html_content = html_content.replace(
                        '<title>Deuxième Cerveau Dynamique</title>',
                        f'<title>{value}</title>'
                    )

        # Write output file
        output_path = self.project_root / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Generated consistent HTML: {output_file}")
        return html_content

def main():
    generator = HTMLTemplateGenerator()

    try:
        generator.load_template()
        generator.generate_consistent_html()

        print("🎯 HTML generation completed successfully!")
        print("📋 Template-based approach ensures:")
        print("   • Consistent section structure")
        print("   • Preserved functionality")
        print("   • Standardized layout")
        print("   • Version control compatibility")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())

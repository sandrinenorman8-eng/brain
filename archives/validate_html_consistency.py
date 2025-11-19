#!/usr/bin/env python3
"""
HTML Consistency Validator for Deuxième Cerveau Project
Validates HTML structure against base template to prevent degradation
"""

import os
import hashlib
from bs4 import BeautifulSoup
from pathlib import Path

class HTMLValidator:
    def __init__(self, base_file="index_stable_backup.html"):
        self.base_file = base_file
        self.project_root = Path(__file__).parent

    def calculate_file_hash(self, filepath):
        """Calculate SHA256 hash of file content"""
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def validate_structure(self):
        """Validate HTML structure against base template"""
        base_path = self.project_root / self.base_file
        current_path = self.project_root / "index.html"

        if not base_path.exists():
            return {"error": f"Base file {self.base_file} not found"}

        if not current_path.exists():
            return {"error": "Current index.html not found"}

        # Parse HTML files
        with open(base_path, 'r', encoding='utf-8') as f:
            base_soup = BeautifulSoup(f.read(), 'html.parser')

        with open(current_path, 'r', encoding='utf-8') as f:
            current_soup = BeautifulSoup(f.read(), 'html.parser')

        issues = []

        # Check critical sections exist
        critical_sections = ['main-section', 'notes-section', 'folders-section']
        for section_id in critical_sections:
            base_section = base_soup.find(id=section_id)
            current_section = current_soup.find(id=section_id)

            if not base_section:
                issues.append(f"CRITICAL: Base missing section {section_id}")
            if not current_section:
                issues.append(f"CRITICAL: Current missing section {section_id}")

        # Check fusion modal
        if not current_soup.find(id="fusionModal"):
            issues.append("CRITICAL: Fusion modal missing")

        # Check script references
        if not current_soup.find('script', src="script.js"):
            issues.append("CRITICAL: script.js reference missing")

        # Check CSS references (should be embedded, not external)
        if current_soup.find('link', rel="stylesheet"):
            issues.append("WARNING: External CSS reference found (should be embedded)")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "base_hash": self.calculate_file_hash(base_path),
            "current_hash": self.calculate_file_hash(current_path)
        }

def main():
    validator = HTMLValidator()
    result = validator.validate_structure()

    print("🔍 HTML Consistency Validation Report")
    print("=" * 50)

    if result["valid"]:
        print("✅ HTML structure is consistent with base template")
    else:
        print("❌ HTML structure issues found:")
        for issue in result["issues"]:
            print(f"  - {issue}")

    print(f"\n📋 Base template hash: {result['base_hash'][:16]}...")
    print(f"📋 Current file hash: {result['current_hash'][:16]}...")

    if result["base_hash"] == result["current_hash"]:
        print("✅ Files are identical")
    else:
        print("⚠️  Files differ - review changes carefully")

if __name__ == "__main__":
    main()

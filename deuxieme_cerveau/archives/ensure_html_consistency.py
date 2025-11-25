#!/usr/bin/env python3
"""
Comprehensive HTML Consistency Assurance System
Combines validation, generation, and maintenance tools
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

class HTMLConsistencyManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.config_file = self.project_root / "html_config.json"
        self.base_template = self.project_root / "index_stable_backup.html"
        self.current_html = self.project_root / "index.html"

        # Load configuration
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def run_full_consistency_check(self):
        """Run complete consistency check and report"""
        print("🔍 Running Full HTML Consistency Check")
        print("=" * 50)

        issues = []
        recommendations = []

        # 1. Check file existence
        if not self.base_template.exists():
            issues.append("CRITICAL: Base template missing")
            return issues, recommendations

        if not self.current_html.exists():
            issues.append("CRITICAL: Current HTML file missing")
            return issues, recommendations

        # 2. Check file sizes (rough degradation indicator)
        base_size = self.base_template.stat().st_size
        current_size = self.current_html.stat().st_size

        if current_size < base_size * 0.8:
            issues.append(f"WARNING: Current file is {current_size/base_size:.1%} of base size - possible degradation")

        # 3. Check for required sections
        with open(self.current_html, 'r', encoding='utf-8') as f:
            content = f.read()

        required_sections = self.config.get('structure_requirements', {}).get('critical_sections', [])
        for section in required_sections:
            if f'id="{section}"' not in content:
                issues.append(f"CRITICAL: Missing section {section}")

        # 4. Check for required elements
        required_elements = self.config.get('structure_requirements', {}).get('required_elements', [])
        for element in required_elements:
            if element not in content:
                if element == 'embedded_css':
                    if '<style>' not in content:
                        issues.append("CRITICAL: Missing embedded CSS")
                elif element == 'script.js':
                    if 'script.js' not in content:
                        issues.append("CRITICAL: Missing script.js reference")
                else:
                    if f'id="{element}"' not in content:
                        issues.append(f"CRITICAL: Missing element {element}")

        # 5. Check for forbidden elements
        forbidden_elements = self.config.get('structure_requirements', {}).get('forbidden_elements', [])
        for element in forbidden_elements:
            if element == 'external_css_link':
                if '<link rel="stylesheet"' in content:
                    issues.append("WARNING: External CSS link found (should be embedded)")

        # Generate recommendations
        if issues:
            recommendations.append("🔧 Run: python validate_html_consistency.py")
            recommendations.append("🔧 Run: python html_template_generator.py")
            recommendations.append("🔧 Check: html_config.json for requirements")

            if any("CRITICAL" in issue for issue in issues):
                recommendations.append("🚨 CRITICAL ISSUES: Restore from stable backup immediately")
        else:
            recommendations.append("✅ HTML structure is consistent")
            recommendations.append("🔄 Consider creating backup of current stable version")

        return issues, recommendations

    def create_backup_with_timestamp(self):
        """Create timestamped backup of current HTML"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"index_backup_{timestamp}.html"

        if self.current_html.exists():
            shutil.copy2(self.current_html, self.project_root / backup_name)
            print(f"💾 Backup created: {backup_name}")

        return backup_name

    def generate_from_template(self):
        """Generate HTML from stable template"""
        if not self.base_template.exists():
            print("❌ Base template not found")
            return False

        try:
            shutil.copy2(self.base_template, self.current_html)
            print("✅ HTML regenerated from stable template")
            return True
        except Exception as e:
            print(f"❌ Error regenerating HTML: {e}")
            return False

def main():
    manager = HTMLConsistencyManager()

    # Run full consistency check
    issues, recommendations = manager.run_full_consistency_check()

    print("\n📊 CONSISTENCY REPORT")
    print("=" * 30)

    if issues:
        print("❌ ISSUES FOUND:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("✅ NO ISSUES FOUND")

    print("\n💡 RECOMMENDATIONS:")
    for rec in recommendations:
        print(f"  • {rec}")

    # Auto-fix critical issues
    critical_issues = [i for i in issues if "CRITICAL" in i]
    if critical_issues:
        print("\n🔧 AUTO-FIXING CRITICAL ISSUES...")
        manager.create_backup_with_timestamp()

        if manager.generate_from_template():
            print("✅ Auto-fix completed - HTML restored from stable template")
        else:
            print("❌ Auto-fix failed - manual intervention required")

    return len(issues)

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

# Quick usage examples:
# python ensure_html_consistency.py                    # Full check + auto-fix
# python validate_html_consistency.py                  # Just validation
# python html_template_generator.py                    # Regenerate from template

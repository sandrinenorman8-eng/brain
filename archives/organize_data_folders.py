"""
Utility script to organize and validate the hierarchical data folder structure
Provides methods to scan, list, and validate the folder organization
"""

import os
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime


class DataFolderOrganizer:
    """Manages hierarchical folder structure in data/ directory"""
    
    def __init__(self, base_path='data'):
        self.base_path = Path(base_path)
        self.structure = {}
    
    def scan_structure(self):
        """Scan and build complete folder structure"""
        self.structure = {}
        
        if not self.base_path.exists():
            print(f"❌ Base path {self.base_path} does not exist")
            return self.structure
        
        for category_dir in self.base_path.iterdir():
            if category_dir.is_dir():
                category_name = category_dir.name
                self.structure[category_name] = self._scan_category(category_dir)
        
        return self.structure
    
    def _scan_category(self, category_path):
        """Recursively scan a category folder"""
        result = {
            'path': str(category_path),
            'subfolders': {},
            'files': [],
            'total_files': 0
        }
        
        for item in category_path.rglob('*'):
            if item.is_file() and item.suffix == '.txt':
                rel_path = item.relative_to(category_path)
                result['files'].append({
                    'name': item.name,
                    'path': str(rel_path).replace('\\', '/'),
                    'subfolder': str(rel_path.parent).replace('\\', '/') if rel_path.parent != Path('.') else None,
                    'size': item.stat().st_size,
                    'modified': datetime.fromtimestamp(item.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
                result['total_files'] += 1
        
        # Build subfolder tree
        for item in category_path.iterdir():
            if item.is_dir():
                subfolder_name = item.name
                result['subfolders'][subfolder_name] = self._count_files_recursive(item)
        
        return result
    
    def _count_files_recursive(self, folder_path):
        """Count files recursively in a folder"""
        count = 0
        for item in folder_path.rglob('*.txt'):
            if item.is_file():
                count += 1
        return count
    
    def print_structure(self):
        """Print the folder structure in a readable format"""
        if not self.structure:
            self.scan_structure()
        
        print("\n" + "="*80)
        print("📁 DATA FOLDER STRUCTURE")
        print("="*80)
        
        for category, data in sorted(self.structure.items()):
            print(f"\n📂 {category.upper()}")
            print(f"   Total files: {data['total_files']}")
            
            if data['subfolders']:
                print(f"   Subfolders:")
                for subfolder, file_count in sorted(data['subfolders'].items()):
                    print(f"      └─ {subfolder} ({file_count} files)")
            
            if data['files']:
                print(f"   Files:")
                for file_info in sorted(data['files'], key=lambda x: x['modified'], reverse=True)[:5]:
                    subfolder_display = f" [{file_info['subfolder']}]" if file_info['subfolder'] else ""
                    print(f"      • {file_info['name']}{subfolder_display}")
                
                if len(data['files']) > 5:
                    print(f"      ... and {len(data['files']) - 5} more files")
        
        print("\n" + "="*80)
        total_files = sum(data['total_files'] for data in self.structure.values())
        print(f"📊 TOTAL: {len(self.structure)} categories, {total_files} files")
        print("="*80 + "\n")
    
    def export_to_json(self, output_file='data_structure.json'):
        """Export structure to JSON file"""
        if not self.structure:
            self.scan_structure()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.structure, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Structure exported to {output_file}")
    
    def get_all_files_flat(self):
        """Get a flat list of all files with their full paths"""
        if not self.structure:
            self.scan_structure()
        
        all_files = []
        for category, data in self.structure.items():
            for file_info in data['files']:
                all_files.append({
                    'category': category,
                    'filename': file_info['name'],
                    'path': file_info['path'],
                    'subfolder': file_info['subfolder'],
                    'full_path': f"data/{category}/{file_info['path']}",
                    'size': file_info['size'],
                    'modified': file_info['modified']
                })
        
        return all_files
    
    def validate_structure(self):
        """Validate folder structure and report issues"""
        if not self.structure:
            self.scan_structure()
        
        issues = []
        
        for category, data in self.structure.items():
            # Check for empty categories
            if data['total_files'] == 0:
                issues.append(f"⚠️  Category '{category}' is empty")
            
            # Check for files with invalid names
            for file_info in data['files']:
                if not file_info['name'].endswith('.txt'):
                    issues.append(f"⚠️  Invalid file extension: {file_info['path']}")
                
                # Check for special characters that might cause issues
                if any(char in file_info['name'] for char in ['<', '>', ':', '"', '|', '?', '*']):
                    issues.append(f"⚠️  Invalid characters in filename: {file_info['name']}")
        
        if issues:
            print("\n🔍 VALIDATION ISSUES:")
            for issue in issues:
                print(f"   {issue}")
        else:
            print("\n✅ No validation issues found!")
        
        return issues
    
    def get_category_stats(self):
        """Get statistics for each category"""
        if not self.structure:
            self.scan_structure()
        
        stats = []
        for category, data in self.structure.items():
            total_size = sum(f['size'] for f in data['files'])
            stats.append({
                'category': category,
                'files': data['total_files'],
                'subfolders': len(data['subfolders']),
                'total_size_kb': round(total_size / 1024, 2),
                'avg_file_size_kb': round(total_size / data['total_files'] / 1024, 2) if data['total_files'] > 0 else 0
            })
        
        return sorted(stats, key=lambda x: x['files'], reverse=True)


def main():
    """Main function to demonstrate usage"""
    organizer = DataFolderOrganizer('data')
    
    # Scan and print structure
    organizer.scan_structure()
    organizer.print_structure()
    
    # Validate
    organizer.validate_structure()
    
    # Export to JSON
    organizer.export_to_json('data_structure.json')
    
    # Print statistics
    print("\n📊 CATEGORY STATISTICS:")
    print("-" * 80)
    stats = organizer.get_category_stats()
    for stat in stats:
        print(f"{stat['category']:20} | Files: {stat['files']:4} | Subfolders: {stat['subfolders']:2} | "
              f"Size: {stat['total_size_kb']:8.2f} KB | Avg: {stat['avg_file_size_kb']:6.2f} KB")
    print("-" * 80)


if __name__ == '__main__':
    main()

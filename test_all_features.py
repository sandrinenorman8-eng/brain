#!/usr/bin/env python3
"""
Comprehensive Test Suite for Deuxième Cerveau
Tests all backend endpoints and functionality
"""

import requests
import json
from datetime import datetime
import sys

BASE_URL = "http://localhost:5008"
SEARCH_URL = "http://localhost:3008"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name, status, message=""):
    symbol = "✅" if status else "❌"
    color = Colors.GREEN if status else Colors.RED
    print(f"{symbol} {color}{name}{Colors.END} {message}")

def test_server_health():
    """Test if servers are running"""
    print(f"\n{Colors.BLUE}=== Testing Server Health ==={Colors.END}")
    
    try:
        response = requests.get(f"{BASE_URL}/categories", timeout=5)
        print_test("Flask Server", response.status_code == 200, f"(Status: {response.status_code})")
    except Exception as e:
        print_test("Flask Server", False, f"(Error: {str(e)})")
        return False
    
    try:
        response = requests.get(f"{SEARCH_URL}/status", timeout=5)
        data = response.json()
        print_test("Search Server", response.status_code == 200, 
                  f"({data.get('categories', 0)} categories indexed)")
    except Exception as e:
        print_test("Search Server", False, f"(Error: {str(e)})")
    
    return True

def test_categories():
    """Test category endpoints"""
    print(f"\n{Colors.BLUE}=== Testing Category Endpoints ==={Colors.END}")
    
    # Test GET /categories
    response = requests.get(f"{BASE_URL}/categories")
    data = response.json()
    success = data.get('success') and len(data.get('data', [])) > 0
    print_test("GET /categories", success, 
              f"({len(data.get('data', []))} categories loaded)")
    
    return data.get('data', [])

def test_note_operations(category_name="todo"):
    """Test note creation and reading"""
    print(f"\n{Colors.BLUE}=== Testing Note Operations ==={Colors.END}")
    
    # Test POST /save/<category>
    test_text = f"Automated test note - {datetime.now().strftime('%H:%M:%S')}"
    response = requests.post(
        f"{BASE_URL}/save/{category_name}",
        json={"text": test_text},
        headers={"Content-Type": "application/json"}
    )
    data = response.json()
    success = data.get('success')
    filename = data.get('data', {}).get('filename', 'N/A')
    print_test("POST /save/<category>", success, f"(File: {filename})")
    
    # Test GET /list/<category>
    response = requests.get(f"{BASE_URL}/list/{category_name}")
    data = response.json()
    files = data.get('data', [])
    success = data.get('success') and len(files) > 0
    print_test("GET /list/<category>", success, f"({len(files)} files found)")
    
    # Test GET /read/<category>/<filename>
    if files:
        first_file = files[0]
        response = requests.get(f"{BASE_URL}/read/{category_name}/{first_file}")
        success = response.status_code == 200 and len(response.text) > 0
        print_test("GET /read/<category>/<filename>", success, 
                  f"(Read {first_file})")
    
    return True

def test_all_files():
    """Test all files endpoint"""
    print(f"\n{Colors.BLUE}=== Testing All Files Endpoint ==={Colors.END}")
    
    response = requests.get(f"{BASE_URL}/all_files")
    data = response.json()
    all_files = data.get('data', [])
    success = data.get('success') and len(all_files) > 0
    print_test("GET /all_files", success, f"({len(all_files)} total files)")
    
    return all_files

def test_search():
    """Test search functionality"""
    print(f"\n{Colors.BLUE}=== Testing Search Functionality ==={Colors.END}")
    
    # Test with valid query
    response = requests.post(
        f"{SEARCH_URL}/search",
        json={"query": "test automated"},
        headers={"Content-Type": "application/json"}
    )
    data = response.json()
    print_test("POST /search (valid query)", response.status_code == 200, 
              f"({len(data.get('results', []))} results)")
    
    # Test with short query
    response = requests.post(
        f"{SEARCH_URL}/search",
        json={"query": "ab"},
        headers={"Content-Type": "application/json"}
    )
    data = response.json()
    print_test("POST /search (short query)", 
              "trop court" in data.get('message', '').lower(),
              "(Correctly rejected)")
    
    return True

def test_backup():
    """Test backup endpoint"""
    print(f"\n{Colors.BLUE}=== Testing Backup Endpoint ==={Colors.END}")
    
    try:
        # Correct endpoint is POST /api/backup_project
        response = requests.post(f"{BASE_URL}/api/backup_project", timeout=30)
        success = response.status_code == 200
        print_test("POST /api/backup_project", success, 
                  f"(Status: {response.status_code})")
    except Exception as e:
        print_test("POST /api/backup_project", False, f"(Error: {str(e)})")
    
    return True

def test_fusion():
    """Test fusion endpoints"""
    print(f"\n{Colors.BLUE}=== Testing Fusion Endpoints ==={Colors.END}")
    
    # Test global fusion - correct endpoint is POST /api/fusion/global
    response = requests.post(f"{BASE_URL}/api/fusion/global")
    success = response.status_code == 200
    print_test("POST /api/fusion/global", success, f"(Status: {response.status_code})")
    
    return True

def test_category_management():
    """Test category creation"""
    print(f"\n{Colors.BLUE}=== Testing Category Management ==={Colors.END}")
    
    # Test add category - correct endpoint is POST /api/add_category
    test_category = f"test_category_{datetime.now().strftime('%H%M%S')}"
    response = requests.post(
        f"{BASE_URL}/api/add_category",
        json={"name": test_category},
        headers={"Content-Type": "application/json"}
    )
    data = response.json()
    success = data.get('success')
    print_test("POST /api/add_category", success, f"(Created: {test_category})")
    
    # Clean up - delete test category - correct endpoint is DELETE /api/erase_category
    if success:
        response = requests.delete(f"{BASE_URL}/api/erase_category/{test_category}")
        data = response.json()
        print_test("DELETE /api/erase_category", data.get('success'), 
                  f"(Deleted: {test_category})")
    
    return True

def run_all_tests():
    """Run all tests"""
    print(f"\n{Colors.YELLOW}{'='*60}{Colors.END}")
    print(f"{Colors.YELLOW}  Deuxième Cerveau - Comprehensive Test Suite{Colors.END}")
    print(f"{Colors.YELLOW}  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    print(f"{Colors.YELLOW}{'='*60}{Colors.END}")
    
    # Check if servers are running
    if not test_server_health():
        print(f"\n{Colors.RED}❌ Servers not running. Please start the application first.{Colors.END}")
        sys.exit(1)
    
    # Run all tests
    categories = test_categories()
    test_note_operations()
    test_all_files()
    test_search()
    test_backup()
    test_fusion()
    test_category_management()
    
    print(f"\n{Colors.YELLOW}{'='*60}{Colors.END}")
    print(f"{Colors.GREEN}✅ All tests completed!{Colors.END}")
    print(f"{Colors.YELLOW}{'='*60}{Colors.END}\n")

if __name__ == "__main__":
    run_all_tests()

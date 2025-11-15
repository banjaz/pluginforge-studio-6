"""
Comprehensive Test Script for PluginForge Studio UI/UX Upgrades
Tests all 6 upgrades and subscription functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:5002"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.END}" if passed else f"{Colors.RED}✗ FAIL{Colors.END}"
    print(f"{status} | {name}")
    if details:
        print(f"     {Colors.BLUE}{details}{Colors.END}")

def test_upgrade_1_login_page():
    """Test Upgrade 1: Formal Login Page"""
    print(f"\n{Colors.YELLOW}=== Testing Upgrade 1: Formal Login/Register Pages ==={Colors.END}")
    
    # Test login page loads
    response = requests.get(f"{BASE_URL}/login")
    print_test("Login page loads", response.status_code == 200)
    
    # Check for key elements
    content = response.text
    has_logo = "PluginForge Studio" in content
    has_professional_text = "Professional Plugin Development Platform" in content
    has_dark_theme = "#3E4146" in content or "#2F3338" in content
    has_orange_color = "#FC8805" in content
    
    print_test("Logo and branding present", has_logo)
    print_test("Professional subtitle present", has_professional_text)
    print_test("Dark theme colors applied", has_dark_theme)
    print_test("Orange accent color present", has_orange_color)
    
    # Test register page
    response = requests.get(f"{BASE_URL}/register")
    print_test("Register page loads", response.status_code == 200)

def test_upgrade_2_color_scheme():
    """Test Upgrade 2: Complete Site Color Update"""
    print(f"\n{Colors.YELLOW}=== Testing Upgrade 2: Site Color Update ==={Colors.END}")
    
    # Check CSS file
    response = requests.get(f"{BASE_URL}/static/style.css")
    css_content = response.text
    
    has_primary_orange = "#FC8805" in css_content
    has_dark_bg = "#3E4146" in css_content
    has_near_black = "#2F3338" in css_content
    has_pale_yellow = "#FEE8B7" in css_content
    
    print_test("CSS contains primary orange (#FC8805)", has_primary_orange)
    print_test("CSS contains dark gray background (#3E4146)", has_dark_bg)
    print_test("CSS contains near black (#2F3338)", has_near_black)
    print_test("CSS contains pale yellow (#FEE8B7)", has_pale_yellow)

def test_upgrade_5_plans_page():
    """Test Upgrade 5: Plans Page"""
    print(f"\n{Colors.YELLOW}=== Testing Upgrade 5: Plans Page ==={Colors.END}")
    
    # Note: This requires authentication, but we can check if the route exists
    response = requests.get(f"{BASE_URL}/plans", allow_redirects=False)
    # Should redirect to login (302) if not authenticated
    print_test("Plans route exists", response.status_code in [200, 302])

def test_subscription_api():
    """Test Subscription API Endpoints"""
    print(f"\n{Colors.YELLOW}=== Testing Subscription API ==={Colors.END}")
    
    # Create a session and login
    session = requests.Session()
    
    # Login
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = session.post(f"{BASE_URL}/login", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        print_test("Login successful", data.get('success', False))
        
        # Test upgrade API
        upgrade_data = {"plan": "pro"}
        response = session.post(f"{BASE_URL}/api/subscription/upgrade", json=upgrade_data)
        
        if response.status_code == 200:
            data = response.json()
            print_test("Subscription upgrade API works", data.get('success', False))
            print_test("Plan upgraded to Pro", data.get('plan') == 'pro', 
                       details=f"Response: {data.get('message', '')}")
        else:
            print_test("Subscription upgrade API works", False, 
                       details=f"Status: {response.status_code}")
        
        # Test dashboard to see if plan is reflected
        response = session.get(f"{BASE_URL}/dashboard")
        if response.status_code == 200:
            content = response.text
            # Check if PRO PLAN badge is shown
            has_pro_plan = "PRO PLAN" in content
            print_test("Dashboard shows upgraded plan", has_pro_plan)
    else:
        print_test("Login successful", False, details="Could not login for API tests")

def test_page_structure():
    """Test page structure and elements"""
    print(f"\n{Colors.YELLOW}=== Testing Page Structure ==={Colors.END}")
    
    session = requests.Session()
    
    # Login first
    login_data = {"username": "admin", "password": "admin123"}
    response = session.post(f"{BASE_URL}/login", json=login_data)
    
    if response.status_code == 200 and response.json().get('success'):
        # Test dashboard
        response = session.get(f"{BASE_URL}/dashboard")
        content = response.text
        
        # Check for fixed header elements
        has_logo = "PluginForge" in content
        has_upgrade_button = "Upgrade" in content
        has_navigation = "Dashboard" in content and "Plans" in content
        
        print_test("Fixed header with logo", has_logo)
        print_test("Upgrade button present", has_upgrade_button)
        print_test("Navigation links present", has_navigation)
        
        # Check for loading indicators
        has_loading = "Refreshing dashboard" in content or "loading-spinner" in content
        print_test("Loading indicators implemented", has_loading)

def run_all_tests():
    """Run all tests"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}  PluginForge Studio - Comprehensive Test Suite{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    
    try:
        # Wait for server to be ready
        print("Waiting for server to be ready...")
        time.sleep(1)
        
        # Run all tests
        test_upgrade_1_login_page()
        test_upgrade_2_color_scheme()
        test_upgrade_5_plans_page()
        test_subscription_api()
        test_page_structure()
        
        print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"{Colors.GREEN}  Test Suite Complete{Colors.END}")
        print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
        
    except requests.exceptions.ConnectionError:
        print(f"\n{Colors.RED}ERROR: Could not connect to server at {BASE_URL}{Colors.END}")
        print(f"Please ensure the server is running.")
    except Exception as e:
        print(f"\n{Colors.RED}ERROR: {e}{Colors.END}")

if __name__ == "__main__":
    run_all_tests()

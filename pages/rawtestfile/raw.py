import sys
import os
from playwright.sync_api import sync_playwright, Page, expect

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Expected URLs
GOOGLE_AUTH_URL = "https://accounts.google.com/"
LINKEDIN_AUTH_URL = "https://www.linkedin.com/"

def navigate_to_signup(page: Page) -> None:
    """Navigates to the signup page and verifies the URL."""
    page.goto("https://dev.agents.agencyheight.com/signup")
    expect(page).to_have_url("https://dev.agents.agencyheight.com/signup")
    print("✅ Signup page loaded successfully.")

def test_signup_buttons(page: Page) -> None:
    """Verifies signup button functionality."""
    try:
        navigate_to_signup(page)
        
        # Test Google button
        with page.expect_popup() as popup_info:
            page.click("button:has-text('Sign up with Google')")
        google_page = popup_info.value
        google_page.wait_for_load_state()
        assert GOOGLE_AUTH_URL in google_page.url
        print("✅ Google auth page opened successfully")
        
        # Test LinkedIn button
        with page.expect_popup() as popup_info:
            page.click("button:has-text('Sign up with Linkedin')")
        linkedin_page = popup_info.value
        linkedin_page.wait_for_load_state()
        assert LINKEDIN_AUTH_URL in linkedin_page.url
        print("✅ LinkedIn auth page opened successfully")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise

# Test Case 4: Verify Signup page Redirection    
def test_login_page_redirection(page: Page) -> None:
    """Tests if clicking the 'Login now' button redirects to the login page correctly."""

    try:
        # Navigate to signup page
        navigate_to_signup(page)

        # Click on "Login now" button
        page.get_by_role("button", name="Login now", exact=True).click()
        print("✅ Clicked on 'Login now' button.")

        # Wait for navigation to the login page
        page.wait_for_url("https://dev.agents.agencyheight.com/login", timeout=5000)

        # Assertion to verify the correct page is loaded
        assert page.url == "https://dev.agents.agencyheight.com/login", \
            f"❌ Test Failed: Incorrect URL. Expected: https://dev.agents.agencyheight.com/login, Found: {page.url}"

        print("🎯 Login Page Redirection Test Passed Successfully!")

    except Exception as e:
        print(f"❌ Test Failed: {e}")
        raise      

import sys
import os
from playwright.sync_api import sync_playwright, Page, expect

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Expected URLs
GOOGLE_AUTH_URL = "https://accounts.google.com/"
LINKEDIN_AUTH_URL = "https://www.linkedin.com/"


def navigate_to_signup(page: Page) -> None:
    """Navigates to the signup page and verifies the URL."""
    page.goto("https://dev.agents.agencyheight.com/signup")
    expect(page).to_have_url("https://dev.agents.agencyheight.com/signup")
    print("✅ Signup page loaded successfully.")


def test_signup_buttons(page: Page) -> None:
    """Verifies signup button functionality."""
    try:
        navigate_to_signup(page)
        
        # Test Google button
        with page.expect_popup() as popup_info:
            page.click("button:has-text('Sign up with Google')")
        google_page = popup_info.value
        google_page.wait_for_load_state()
        assert GOOGLE_AUTH_URL in google_page.url, "Google auth page did not open correctly"
        print("✅ Google auth page opened successfully")
        
        # Test LinkedIn button
        with page.expect_popup() as popup_info:
            page.click("button:has-text('Sign up with Linkedin')")
        linkedin_page = popup_info.value
        linkedin_page.wait_for_load_state()
        assert LINKEDIN_AUTH_URL in linkedin_page.url, "LinkedIn auth page did not open correctly"
        print("✅ LinkedIn auth page opened successfully")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


def test_login_page_redirection(page: Page) -> None:
    """Tests if clicking the 'Login now' button redirects to the login page correctly."""
    try:
        navigate_to_signup(page)

        # Click on "Login now" button
        page.get_by_role("button", name="Login now", exact=True).click()
        print("✅ Clicked on 'Login now' button.")

        # Wait for navigation to the login page
        page.wait_for_url("https://dev.agents.agencyheight.com/login", timeout=5000)

        # Assertion to verify the correct page is loaded
        assert page.url == "https://dev.agents.agencyheight.com/login", (
            f"❌ Test Failed: Incorrect URL. Expected: https://dev.agents.agencyheight.com/login, Found: {page.url}"
        )

        print("🎯 Login Page Redirection Test Passed Successfully!")

    except Exception as e:
        print(f"❌ Test Failed: {e}")
        raise


def run_tests():
    """Runs all tests across multiple browsers."""
    browsers = [
        ("Chrome", "chromium", {"channel": "chrome"}),
        ("Edge", "chromium", {"channel": "msedge"}),
        ("Firefox", "firefox", {}),
        ("Safari", "webkit", {})
    ]
    
    test_cases = [test_signup_buttons, test_login_page_redirection]
    
    with sync_playwright() as p:
        for browser_name, browser_type, launch_options in browsers:
            print(f"\n🚀 Running tests in {browser_name}...\n")
            try:
                browser = getattr(p, browser_type).launch(headless=False, **launch_options)
                context = browser.new_context()
                page = context.new_page()
                
                for test_case in test_cases:
                    print(f"🎯 Running {test_case.__name__} in {browser_name}")
                    try:
                        test_case(page)
                        print(f"✅ {test_case.__name__} passed in {browser_name}\n")
                    except Exception as e:
                        print(f"❌ {test_case.__name__} failed in {browser_name}: {e}\n")
                
                context.close()
                browser.close()
            except Exception as e:
                print(f"❌ Failed to initialize {browser_name}: {e}")

if __name__ == "__main__":
    run_tests()

import sys
import os
from playwright.sync_api import sync_playwright, Page, expect

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import utility functions
from utils.randomgenerator import *
from playwright.sync_api import sync_playwright, Page, expect

# Expected URLs for third-party auth redirects
GOOGLE_AUTH_URL = "https://accounts.google.com/"
LINKEDIN_AUTH_URL = "https://www.linkedin.com/"

# Helper Function: Navigate to Login Page
def navigate_to_login(page: Page) -> None:
    """Navigates to the login page and verifies the URL."""
    page.goto("https://dev.agents.agencyheight.com/login")
    expect(page).to_have_url("https://dev.agents.agencyheight.com/login")
    print("✅ Login page loaded successfully.")

def choose_browser() -> str:
    """Prompts user for browser choice and returns the selected browser."""
    print("Please choose a browser:")
    print("1: Chrome")
    print("2: Firefox")
    print("3: Safari")
    print("4: Edge")
    
    choice = input("Enter the number of your choice: ")
    
    browser_map = {
        "1": "chrome",
        "2": "firefox",
        "3": "safari",
        "4": "edge"
    }
    
    return browser_map.get(choice, "chrome")  # Default to chrome


# Test Case 1: Valid Login Test
def test_login_validdata(page: Page) -> None:
    """Tests logging in with valid credentials."""
    try:
        #Inputdata
        email = "gyvylucen@yopmail.com"
        password = "Enter@123"

        #Navigate to Login
        navigate_to_login(page)
        page.wait_for_load_state("networkidle")

        # Fill login form
        page.locator("input[name='email']").fill(email)
        page.locator("input[name='password']").fill(password)
        page.get_by_role("button", name="Log In", exact=True).click()

        # Wait for the dashboard page
        page.wait_for_url("https://dev.agents.agencyheight.com/dashboard", timeout=20000)

        print("✅ Test Passed: Valid login.")
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        raise

# Test Case 2: Empty Fields Login Test
def test_login_emptyfields(page: Page) -> None:
    """Tests login with empty fields."""
    try:
        #Navigate to Login
        navigate_to_login(page)
        page.get_by_role("button", name="Log In", exact=True).click()

        error_message_email = page.get_by_text("Invalid email")
        error_message_password = page.get_by_text("String must contain at least 2 character(s)")

        expect(error_message_email).to_be_visible()
        expect(error_message_password).to_be_visible()

        print("✅ Test Passed: Empty field validation.")
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        raise

# Test Case 3: Unregistered Email Login Test
def test_login_invalid_credentials(page: Page) -> None:
    """Tests login with an unregistered email."""
    try:
        #Inputdata
        email = "Nonexisting@yopmail.com"
        password = "Enter@123"

        #Navigate to Login
        navigate_to_login(page)
        page.wait_for_load_state("networkidle")

        page.locator("input[name='email']").fill(email)
        page.locator("input[name='password']").fill(password)
        page.get_by_role("button", name="Log In", exact=True).click()

        error_message_email = page.get_by_text("User Not Found!!!")
        expect(error_message_email).to_be_visible()

        print("✅ Test Passed: Unregistered email validation.")
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        raise

# Test Case 4: Password Show/Hide Feature
def test_login_show_hide_password(page: Page) -> None:
    """Tests password show/hide functionality."""
    try:
        #Navigate to Login
        navigate_to_login(page)

        #Inputdata
        password = "Enter@123"

        password_input = page.locator("input[name='password']")
        password_input.fill(password)

        assert password_input.get_attribute("type") == "password"

        page.get_by_role("button", name="Show").click()
        assert password_input.get_attribute("type") == "text"

        page.get_by_role("button", name="Hide").click()
        assert password_input.get_attribute("type") == "password"

        print("✅ Test Passed: Password show/hide feature works correctly.")
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        raise

# Test Case 5: Verify Forgot Password Redirection
def test_forgot_password_redirection(page: Page) -> None:
    """Tests Forgot Password link redirection."""
    try:
        #Navigate to Login
        navigate_to_login(page)
        page.get_by_role("button", name="Forgot Password?").click()
        page.wait_for_url("https://dev.agents.agencyheight.com/forgot-password", timeout=10000)

        print("✅ Test Passed: Forgot password redirection successful.")
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        raise

# Test Case 6: Verify Signup Page Redirection
def test_signup_page_redirection(page: Page) -> None:
    """Tests Signup page redirection."""
    try:
        #Navigate to Login
        navigate_to_login(page)
        page.get_by_role("button", name="Sign Up").click()
        page.wait_for_url("https://dev.agents.agencyheight.com/signup", timeout=5000)

        print("✅ Test Passed: Signup page redirection successful.")
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        raise

# Test Case 7: Verify Login Buttons for Google & LinkedIn
def test_social_login_buttons(page: Page) -> None:
    """Verifies 'Login with Google' and 'Login with LinkedIn' buttons open a new tab."""
    try:

        #Navigate to Login
        navigate_to_login(page)
        page.wait_for_load_state("networkidle")

        google_button = page.locator("button:has-text('Log in with Google')")
        linkedin_button = page.locator("button:has-text('Log in with Linkedin')")

        with page.expect_popup() as google_popup:
            google_button.click()
        google_page = google_popup.value
        google_page.wait_for_load_state("domcontentloaded")
        assert GOOGLE_AUTH_URL in google_page.url

        with page.expect_popup() as linkedin_popup:
            linkedin_button.click()
        linkedin_page = linkedin_popup.value
        linkedin_page.wait_for_load_state("domcontentloaded")
        assert LINKEDIN_AUTH_URL in linkedin_page.url

        print("✅ Test Passed: Social login buttons work correctly.")
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        raise
   

# Test Case 8: registered email butwrong password Login Test
def test_login_wrong_password(page: Page) -> None:
    """Tests login with a registered email but an incorrect password."""
    try:

        # Input Data
        email = "parsa@yopmail.com"
        password = "Enter@12sss3"

        navigate_to_login(page)
        page.wait_for_load_state("networkidle")

        # Fill in login details
        page.locator("input[name='email']").fill(email)
        page.locator("input[name='password']").fill(password)
        page.get_by_role("button", name="Log In", exact=True).click()

        # Wait for the error message
        page.wait_for_load_state("networkidle")
        error_message = page.get_by_text("Invalid username or password")

        # Validate error message
        expect(error_message).to_be_visible()
        assert error_message.inner_text() == "Invalid username or password", "❌ Test Failed: Incorrect error message displayed."

        print("✅ Test Passed: Correct error message displayed.")

    except Exception as e:
        print(f"❌ Test Failed: {e}")
        raise

# Test Case 9: Email is Converted to Lowercase Automatically
def test_login_convert_entered_email_to_lowercase(page: Page) -> None:
    """Tests whether the entered email is automatically converted to lowercase before submission."""
    try:

        navigate_to_login(page)

        # Input Data
        email = "PARSA@yopmail.com"  # Uppercase email
        password = "Enter@123"

        page.locator("input[name='email']").fill(email)
        page.locator("input[name='password']").fill(password)

        # Intercept request to check if email is converted to lowercase
        def intercept_request(route):
            request = route.request
            if "/login" in request.url and request.method == "POST":
                request_payload = request.post_data_json()
                submitted_email = request_payload.get("email")

                # Assert that the submitted email is in lowercase
                assert submitted_email == email.lower(), f"❌ Test Failed: Email sent in uppercase. Found: {submitted_email}"
                print("✅ Test Passed: Email submitted in lowercase.")

            route.continue_()

        # Apply request interception
        page.route("**/login", intercept_request)

        # Submit the form
        page.get_by_role("button", name="Log In", exact=True).click()

        # Wait for successful login redirection
        page.wait_for_url("https://dev.agents.agencyheight.com/dashboard", timeout=15000)

        print("✅ Test Passed: Login successful with auto-lowercase conversion.")

    except Exception as e:
        print(f"❌ Test Failed: {e}")
        raise

# Main Function to Run All Tests
def run_tests():
    """Runs all test cases and ensures browser closes properly."""
    with sync_playwright() as playwright:
        for test_case in [     
            test_login_validdata,
            test_login_emptyfields,
            test_login_invalid_credentials,
            test_login_show_hide_password,
            test_forgot_password_redirection,
            test_signup_page_redirection,
            test_social_login_buttons,
            test_login_wrong_password,
            test_login_convert_entered_email_to_lowercase
            ]:
            
            print(f"\n🎯 Executing test: {test_case.__name__}")

    browser_choice = choose_browser()
    
    with sync_playwright() as p:
        # Launch selected browser
        if browser_choice == "firefox":
            browser = p.firefox.launch(headless=False)
        elif browser_choice == "safari":
            browser = p.webkit.launch(headless=False)
        elif browser_choice == "edge":
            browser = p.chromium.launch(channel="msedge", headless=False)
        else:  # Default to Chrome
            browser = p.chromium.launch(channel="chrome", headless=False)
            
        context = browser.new_context()
        page = context.new_page()

        try:
            test_case(page)
            print(f"✅ Completed test: {test_case.__name__}\n")
        except Exception as e:
            print(f"❌ Test Execution Failed in {test_case.__name__}: {e}")
        finally:
                context.close()
                browser.close()

if __name__ == "__main__":
    run_tests()

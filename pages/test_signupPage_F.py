import sys
import os
from playwright.sync_api import sync_playwright, Page, expect

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import utility functions
from utils.randomgenerator import *

# Expected URLs (Modify if the login providers use different redirect URLs)
GOOGLE_AUTH_URL = "https://accounts.google.com/"
LINKEDIN_AUTH_URL = "https://www.linkedin.com/"

# Helper Function: Navigate to Signup Page
def navigate_to_signup (page: Page) -> None:
    """Navigates to the signup page and verifies the URL."""
    page.goto("https://dev.agents.agencyheight.com/signup")
    expect(page).to_have_url("https://dev.agents.agencyheight.com/signup")
    print("✅ Signup page loaded successfully.")
    
# Test Case 1: Valid Signup test (signup page and basicinfo page)
def test_signup(page: Page) -> None:
    try:
    # Input Data
        email = generate_random_email()
        password = "Enter@123"
        full_name = generate_unique_fullname()
        agency_name = generate_random_word_with_inc()
        phone_number = generate_random_phone()
        if len(phone_number) != 10:
            raise ValueError("Generated phone number is not 10 digits")
        location = "30017"
        apt = "2B"
        image_path = os.path.abspath("utils/images/TinyTake31-12-2024-12-00-55.png")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Navigate to Signup Page
        navigate_to_signup(page)

        # Fill Signup For
        page.locator("label").first.click()
        page.locator("input[name='email']", ).fill(email)
        page.locator("input[name='password']").fill(password)
        page.get_by_role("button", name="Sign up now", exact=True).click()
        page.wait_for_load_state("networkidle")

        # Fill Additional Form Fields
        page.locator("input[name='fullName']").fill(full_name)
        page.locator("input[name='agencyName']").fill(agency_name)

        # fill phone field
        phone_input = page.locator("input[name='phoneNumber']")
        phone_input.type(phone_number, delay=200)

        # Verify formatted value
        expected_format = f"({phone_number[:3]}) {phone_number[3:6]} {phone_number[6:]}"
        expect(phone_input).to_have_value(expected_format)

        # Optional: Debug output
        print(f"Formatted Phone Number: {phone_input.input_value()}")
        # Add validation
        # current_value = phone_input.input_value()
        # assert current_value == phone_number, f"Phone number mismatch. Expected {phone_number}, got {current_value}"

        # page.locator("input[name='phoneNumber']").type(phone_number, delay=200)
        page.locator("input[name='location.address']").type(location, delay=200)
        page.wait_for_selector("div.pac-container div.pac-item", timeout=7000)
        for _ in range(3):
            page.locator("input[name='location.address']").press("ArrowDown")
        page.locator("input[name='location.address']").press("Enter")
        page.get_by_label("Apt").fill(apt)
        checkbox = page.get_by_role("checkbox")
        expect(checkbox).to_be_visible()
        checkbox.check()

        # Upload Image
        page.locator("input[type='file']").set_input_files(image_path)
        page.locator("//span[normalize-space()='Save changes']").click()

        # Submit the Form
        page.get_by_role("button", name="Finish Setup").click()
        page.wait_for_url("https://dev.agents.agencyheight.com/dashboard", timeout=15000)
        expect(page.get_by_role("heading", name="QR unlocked 🔓")).to_be_visible()

        # Logout Flow
        page.get_by_role("button", name="Close").click()
        page.locator("div[class='mantine-11p3gcw']").click()
        page.get_by_role("button", name="Log Out").click()
        expect(page).to_have_url("https://dev.agents.agencyheight.com/login")

        print("✅ Signup Test Passed: User successfully signed up and logged out.")

    except Exception as e:
        print(f"❌ Signup Test Failed: {e}")
        raise    
   
# Test Case 2: Verify Sign Up Button Disabled Until Fields Are Filled
def test_signup_button_disabled(page: Page) -> None:
    try:

        navigate_to_signup(page)

        # Locate the "Sign Up" button
        sign_up_button = page.get_by_role("button", name="Sign up now")
        
        # Assert the button is disabled initially
        expect(sign_up_button).to_be_disabled()

        # Fill only the email field
        page.locator("input[name='email']").fill("testuser@yopmail.com")
        
        # Assert button is still disabled
        expect(sign_up_button).to_be_disabled()

        # Fill the password field
        page.locator("input[name='password']").fill("Enter@123")
        
        # Assert button is now enabled
        expect(sign_up_button).not_to_be_disabled()

        print("✅ Sign-Up button is enabled after filling all required fields.")

    except Exception as e:
        print(f"❌ Test Failed: {e}")
        raise      

# Test Case 3: Password show/hide icon  
def test_login_show_hide_password(page: Page) -> None:
    """Tests the show/hide functionality of the password input field."""

    try:
        # Navigate to signup page
        navigate_to_signup(page)

        # Input Data
        password = "Enter@123"

        # Fill password field
        password_input = page.locator("input[name='password']")
        password_input.fill(password)

        # Assert initial state (password should be hidden by default)
        assert password_input.get_attribute("type") == "password", "❌ Test Failed: Password field should be hidden initially."
        print("✅ Password field is initially hidden.")

        # Click 'Show' button to reveal password
        show_button = page.get_by_role("button", name="Show")
        show_button.click()

        # Assert password field should now be visible (type='text')
        assert password_input.get_attribute("type") == "text", "❌ Test Failed: Password field should be visible after clicking Show."
        print("✅ Password field is visible after clicking 'Show' button.")

        # Click 'Hide' button to hide password
        hide_button = page.get_by_role("button", name="Hide")
        hide_button.click()

        # Assert password field should be hidden again (type='password')
        assert password_input.get_attribute("type") == "password", "❌ Test Failed: Password field should be hidden after clicking Hide."
        print("✅ Password field is hidden again after clicking 'Hide' button.")

        print("🎯 Password Show/Hide Test Passed Successfully!")

    except Exception as e:
        print(f"❌ Test Failed: {e}")
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

# Test Case 5: Verify Signup button Redirection  
def test_signup_buttons(page: Page) -> None:
    """Verifies that clicking the 'Sign up with Google' and 'Sign up with LinkedIn' buttons opens a new tab correctly."""
    
    try:
    
        # Navigate to signup page
        navigate_to_signup(page)

        # Identify Buttons
        google_button = page.locator("button:has-text('Sign up with Google')")
        linkedin_button = page.locator("button:has-text('Sign up with Linkedin')")

        # Check if "Sign up with Google" button opens a new tab
        with page.expect_popup() as google_popup:
            google_button.click()
        google_page = google_popup.value
        google_page.wait_for_load_state("domcontentloaded")

        assert GOOGLE_AUTH_URL in google_page.url, \
            f"❌ Test Failed: Google auth URL not opened. Found {google_page.url}"
        print("✅ Google sign-up button opened the correct authentication page.")

        # Check if "Sign up with LinkedIn" button opens a new tab
        with page.expect_popup() as linkedin_popup:
            linkedin_button.click()
        linkedin_page = linkedin_popup.value
        linkedin_page.wait_for_load_state("domcontentloaded")

        assert LINKEDIN_AUTH_URL in linkedin_page.url, \
            f"❌ Test Failed: LinkedIn auth URL not opened. Found {linkedin_page.url}"
        print("✅ LinkedIn sign-up button opened the correct authentication page.")

        print("🎯 Sign-Up Buttons Test Passed Successfully!")

    except Exception as e:
        print(f"❌ Test Failed: {e}")
        raise
       
# Main Function to Run All Tests
def run_tests():
    """Runs all test cases and ensures browser closes properly."""
    with sync_playwright() as playwright:
        for test_case in [
                      test_signup,
                      test_signup_button_disabled,
                      test_login_show_hide_password,
                      test_login_page_redirection,
                      test_signup_buttons
                      ]:
            print(f"\n🎯 Executing test: {test_case.__name__}")

            browser = playwright.chromium.launch(headless=False)
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




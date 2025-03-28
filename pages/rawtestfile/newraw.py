import os
import pytest
from playwright.sync_api import sync_playwright, Page, expect

# Add project root to sys.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import utility functions
from utils.randomgenerator import *

# Helper Function: Navigate to Signup Page
def navigate_to_signup(page: Page) -> None:
    """Navigates to the signup page and verifies the URL."""
    page.goto("https://dev.agents.agencyheight.com/signup")
    expect(page).to_have_url("https://dev.agents.agencyheight.com/signup")
    print("✅ Signup page loaded successfully.")

# Helper Function: Fill Basic Signup Form
def fill_signup_form(page: Page, email: str, password: str) -> None:
    """Fills out the basic signup form."""
    page.locator("label").first.click()
    page.locator("input[name='email']").fill(email)
    page.locator("input[name='password']").fill(password)
    page.get_by_role("button", name="Sign up now", exact=True).click()

# Helper Function: Fill Additional Form Fields
def fill_additional_form(page: Page, full_name: str, agency_name: str, phone_number: str, location: str, apt: str, image_path: str) -> None:
    """Fills additional form fields."""
    # Upload Image
    page.locator("input[type='file']").set_input_files(image_path)
    page.locator("//span[normalize-space()='Save changes']").click()

    # Fill Additional Form Fields
    page.locator("input[name='fullName']").fill(full_name)
    page.locator("input[name='agencyName']").fill(agency_name)

    # Fill Phone Field and Verify Formatting
    phone_input = page.locator("input[name='phoneNumber']")
    phone_input.type(phone_number, delay=300)
    expected_format = f"({phone_number[:3]}) {phone_number[3:6]} {phone_number[6:]}"
    expect(phone_input).to_have_value(expected_format)

    page.locator("input[name='location.address']").type(location, delay=200)
    page.wait_for_selector("div.pac-container div.pac-item", timeout=7000)
    for _ in range(3):
        page.locator("input[name='location.address']").press("ArrowDown")
    page.locator("input[name='location.address']").press("Enter")
    page.get_by_label("Apt").fill(apt)

    # Check Checkbox
    checkbox = page.get_by_role("checkbox")
    expect(checkbox).to_be_visible()
    checkbox.check()

# Test Case: Valid Signup Test (Signup page and basic info page)
def test_signup(page: Page) -> None:
    """Test the signup process."""
    try:
        # Generate Input Data
        email = generate_random_email()
        password = "Enter@123"
        full_name = generate_unique_fullname()
        agency_name = generate_random_word_with_inc()
        phone_number = generate_random_phone()
        location = "30017"
        apt = "2B"
        image_path = os.path.abspath("utils/images/TinyTake31-12-2024-12-00-55.png")

        if len(phone_number) != 10:
            raise ValueError("Generated phone number is not 10 digits")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Navigate to Signup Page
        navigate_to_signup(page)

        # Fill Signup Form
        fill_signup_form(page, email, password)
        page.wait_for_url("https://dev.agents.agencyheight.com/basic-info", timeout=15000)

        # Fill Additional Form Fields
        fill_additional_form(page, full_name, agency_name, phone_number, location, apt, image_path)

        # Submit the Form
        page.get_by_role("button", name="Finish Setup").click()
        page.wait_for_load_state("networkidle")
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

# Main Function to Run All Tests using pytest
def run_tests():
    """Runs all test cases and ensures browser closes properly."""
    with sync_playwright() as playwright:
        try:
            # Launch Browser
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()

            # Run Tests
            for test_case in [test_signup]:
                print(f"\n🎯 Executing test: {test_case.__name__}")
                page = context.new_page()

                try:
                    test_case(page)
                    print(f"✅ Completed test: {test_case.__name__}\n")
                except Exception as e:
                    print(f"❌ Test Execution Failed in {test_case.__name__}: {e}")
                finally:
                    page.close()

            # Close Browser Context
            context.close()
            browser.close()

        except Exception as e:
            print(f"❌ Browser launch failed: {e}")

if __name__ == "__main__":
    run_tests()

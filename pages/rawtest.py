import sys
import os

from playwright.sync_api import sync_playwright, Page, expect

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import utility functions
from utils.randomgenerator import *


# Helper Function: Navigate to Login Page


def navigate_to_signup (page: Page) -> None:
    """Navigates to the signup page and verifies the URL."""
    page.goto("https://dev.agents.agencyheight.com/signup")
    expect(page).to_have_url("https://dev.agents.agencyheight.com/signup")
    print("✅ Signup page loaded successfully.")    
    

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

# Main Function to Run All Tests
def run_tests():
    """Runs all test cases and ensures browser closes properly."""
    with sync_playwright() as playwright:
        for test_case in [
            
            test_signup
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
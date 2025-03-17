import sys
import os

from playwright.sync_api import sync_playwright, Page, expect

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import utility functions
from utils.randomgenerator import *


# Helper Function: Navigate to Login Page
def navigate_to_search_home(page: Page) -> None:
    """Navigates to the login page and verifies the URL."""
    page.goto("https://dev.agents.agencyheight.com/")
    expect(page).to_have_url("https://dev.agents.agencyheight.com/")
    print("✅ Search home page loaded successfully.")
    

# Test Case 2: Request a quote for multi agent
def test_information_modal_prefill(page: Page) -> None:
    try :

        # Input Data
        email = generate_random_email()
       
        full_name = generate_unique_fullname()
    
        phone_number = generate_random_phone()
        if len(phone_number) != 10:
            raise ValueError("Generated phone number is not 10 digits")
    # Navigate to Search home
        navigate_to_search_home(page)
        page.wait_for_load_state("networkidle")

        # Fill out search fields
        page.get_by_placeholder("Zip code").click()
        page.get_by_placeholder("Zip code").fill("48082")
        page.get_by_placeholder("Policy you are looking for").click()
        page.get_by_placeholder("Policy you are looking for").fill("p")
        page.locator("label").nth(3).click()
        page.get_by_text("Personal Auto", exact=True).click()
        page.get_by_role("button", name="Search agents").click()
        page.wait_for_load_state("networkidle")

        # Fill out client info form
        page.get_by_placeholder("Full name").fill(full_name)
        page.get_by_placeholder("Full name").press("Tab")
        page.get_by_placeholder("Email").fill(email)
        page.get_by_placeholder("Email").press("Tab")
        page.get_by_placeholder("Phone number").type(phone_number, delay=200)
        page.get_by_role("button", name="Find agents").click()

        page.get_by_role("heading", name="Update your information").click()
    
        # Verify all fields are prefilled
        # Store expected values
        expected_values = {
            "Full name": full_name,
            "Email": email,
            "Phone number": str(phone_number)
        }
        
        # Verification steps
        assert page.get_by_placeholder("Full name").input_value() == expected_values["Full name"], \
            f"Expected full name to be {expected_values['Full name']}"
        assert page.get_by_placeholder("Email").input_value() == expected_values["Email"], \
            f"Expected email to be {expected_values['Email']}"
        assert page.get_by_placeholder("Phone number").input_value() == expected_values["Phone number"], \
            f"Expected phone number to be {expected_values['Phone number']}"
        print(phone_number)
    
         # Proceed with final submission
        page.get_by_role("button", name="Find agents").click()

        # # Ensure the agent list is loaded
        # page.wait_for_selector("button:has-text('Request a quote')", state="visible", timeout=5000)

        # # Request a quote for the 3rd agent
        # page.get_by_role("button", name="Request a quote").nth(2).click()
        # page.wait_for_selector("button:has-text('Quote requested')", state="visible", timeout=5000)
        
        # # Click "View more" twice
        # page.get_by_role("button", name="View more").click()
        # # page.get_by_role("button", name="View more").click()

        # # Wait for the 5th "Request a quote" button to be available
        # page.wait_for_selector('button:has-text("Request a quote")', state="visible", timeout=10000)
        # page.get_by_role("button", name="Request a quote").nth(4).click()

    except Exception as e:
        print(f"❌ Test Failed: {e}")
        raise     

# Main Function to Run All Tests
def run_tests():
    """Runs all test cases and ensures browser closes properly."""
    with sync_playwright() as playwright:
        for test_case in [
            
            test_information_modal_prefill
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
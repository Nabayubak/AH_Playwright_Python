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
    

def test_search_agent_commercial(page: Page) -> None:
    try :
    # Navigate to Search home
        navigate_to_search_home(page)
        page.wait_for_load_state("networkidle")

        # page.get_by_text("Life", exact=True).click()
        page.locator("//div[p[text()='Commercial']]").click()
        page.get_by_placeholder("Zip code").click()
        page.get_by_placeholder("Zip code").fill("30017")
        page.locator("label").nth(3).click()
        page.get_by_text("Workers Compensation", exact=True).click()
        page.get_by_role("button", name="Search agents").click()

    # Ensure the agent list is loaded
        page.wait_for_selector("button:has-text('Request a quote')", state="visible", timeout=5000)
        

    except Exception as e:
        print(f"❌ Test Failed: {e}")
        raise

# Main Function to Run All Tests
def run_tests():
    """Runs all test cases and ensures browser closes properly."""
    with sync_playwright() as playwright:
        for test_case in [
            
            test_search_agent_commercial
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
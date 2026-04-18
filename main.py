import os
import random

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv("secrets.env")

bio_list_path = "bios_list.txt"

with open(bio_list_path, "r") as f:
    BIO_LIST = f.read().splitlines()

# --Configurations and Constants--
# LINKEDIN_CREDS
LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

LINKEDIN_URL = f"https://www.linkedin.com/in/{LINKEDIN_USERNAME}/"
LINKEDIN_EDIT_BIO_URL = f"https://www.linkedin.com/in/{LINKEDIN_USERNAME}/edit/intro/"

BROWSER_STATE_PATH = "playwright/.auth/state.json"


def main():
    """
    Main function to automate the process of updating the LinkedIn bio.

    This function uses Playwright to:
    1. Navigate to the user's LinkedIn profile edit page.
    2. Check for existing browser state (cookies/login).
    3. Log in if necessary, saving the state for future runs.
    4. Update the headline with a random bio from the provided list.
    5. Fill in required fields (like Industry).
    6. Save the changes and update the browser state.
    """
    print("Hello from linkedin-bio-swapper!")

    if not human_verification(
        "Are you sure you want to change your LinkedIn bio? Type 'yes' to confirm: "
    ):
        print("Bio update cancelled by user.")
        return

    # 1. Using playwright, navigate to linkedin.com, profile, and log in with the provided credentials.
    with sync_playwright() as p:
        # Launch the Chromium browser instance. headless=False allows visual confirmation of actions.
        browser = p.chromium.launch(headless=False, slow_mo=100)

        # --- State Management ---
        # Check if a saved browser state exists. If so, load it to maintain the logged-in session.
        # If not, the script must proceed to the login flow.
        # ADD LOGIC TO SEE IF STATE.JSON EXISTS, IF YES THEN LOAD THE COOKIES, ELSE PROCEED TO LOGIN.
        # ADD HERE

        # Create a new browser context using the saved state.
        context = browser.new_context(storage_state=BROWSER_STATE_PATH)
        page = context.new_page()

        # Navigate to the bio editing page.
        page.goto(LINKEDIN_EDIT_BIO_URL)

        print("Checking if user is already logged in...")
        # Check for a visible element that confirms the user is logged in (e.g., the 'Me' button).

        if not check_logged_in(page):
            print("User is not logged in. Logging in...")

            # --- Login Implementation ---
            page.goto(LINKEDIN_URL)
            page.wait_for_timeout(3000)  # Wait for 3 seconds to allow the page to load.
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("textbox", name="Email or phone").click()
            page.get_by_role("textbox", name="Email or phone").fill(EMAIL)
            page.get_by_role("textbox", name="Password").click()
            page.get_by_role("textbox", name="Password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_timeout(5000)  # Wait for 5 seconds to allow login to process.

            # Recheck if login was successful by looking for the 'Me' button again.
            if not check_logged_in(page):
                print(
                    "Login failed. Please check your credentials and try again. Or login manually and save the browser state."
                )
                page.wait_for_timeout(
                    40000
                )  # Wait for a 40 seconds to allow user to log in manually if automatic login fails.
                # Save current browser state after manual login attempt.
                context.storage_state(path=BROWSER_STATE_PATH)
                return

            print("Login successful! Navigating to the bio edit page...")
            page.goto(LINKEDIN_EDIT_BIO_URL)

        else:
            print("User is already logged in. Proceeding to update bio...")

        # 2. Edit the bio, with a random bio from the list of bios.
        # Select the headline text box element.
        headline = page.get_by_test_id(
            "ui-core-tiptap-text-editor-wrapper"
        ).get_by_role("textbox")

        # Clear any existing content and fill it with a random bio.
        headline.clear()
        bio_choice = random.choice(BIO_LIST)
        headline.fill(bio_choice)
        print(f"Updated bio to: {bio_choice}")

        # Linkedin forces you to input industry when changing the headline, so we need to select an industry as well.
        # Locate and fill the required Industry field.
        page.get_by_role("textbox", name="Industry*").click()
        page.get_by_role("textbox", name="Industry*").fill("cooking 👨🏼‍🍳")

        # 3. Save the changes.
        # Locate and click the Save button.
        save_button = page.get_by_role("button", name="Save")
        save_button.click()

        # Wait for a few seconds to allow the page to process the save action.
        page.wait_for_timeout(3000)

        # Save the current browser context state (cookies, local storage) for future runs.
        storage = context.storage_state(path=BROWSER_STATE_PATH)


def human_verification(
    prompt="Are you sure you want to change your LinkedIn bio? Type 'yes' to confirm: ",
):
    """
    Add check if human truly wants to change the bio. This is a safety measure to prevent accidental changes to the LinkedIn profile.
    """
    return input(prompt).lower() == "yes"


def check_logged_in(page):
    """
    Check if the user is currently logged in to LinkedIn.

    This function looks for a specific element (the 'Me' button) that is only visible when a user is logged in.
    If the element is found and visible, it returns True, indicating that the user is logged in. Otherwise, it returns False.

    Args:
        page: The Playwright page object representing the current browser page.

    Returns:
        bool: True if the user is logged in, False otherwise.
    """
    return page.get_by_role("button", name="Me", exact=True).is_visible()


if __name__ == "__main__":
    main()

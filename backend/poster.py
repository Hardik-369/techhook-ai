from playwright.sync_api import sync_playwright
import time
import os
import random
from dotenv import load_dotenv

load_dotenv()

def post_to_linkedin(post_content, image_path, session_path="data/session.json"):
    """
    Posts content to LinkedIn using Playwright.
    Note: Requires a valid session.json or manual login first.
    """
    with sync_playwright() as p:
        # Launch browser in headed mode for debugging if needed, 
        # but headless for GitHub Actions
        browser = p.chromium.launch(headless=True)
        
        # Load storage state if it exists
        context_args = {}
        if os.path.exists(session_path):
            context_args["storage_state"] = session_path
            
        context = browser.new_context(**context_args)
        page = context.new_page()
        
        try:
            page.goto("https://www.linkedin.com/feed/")
            
            # Check if logged in
            if "login" in page.url:
                email = os.getenv("LINKEDIN_EMAIL")
                password = os.getenv("LINKEDIN_PASSWORD")
                
                if email and password:
                    print("Attempting auto-login...")
                    page.fill("input#username", email)
                    page.fill("input#password", password)
                    page.click("button[type='submit']")
                    page.wait_for_url("**/feed/")
                else:
                    print("Not logged in and no credentials found in .env. Manual login required.")
                    browser.close()
                    return False
            
            # Click "Start a post"
            page.wait_for_selector(".share-box-feed-entry__trigger, button.artdeco-button--tertiary.share-box-feed-entry__trigger")
            page.click(".share-box-feed-entry__trigger, button.artdeco-button--tertiary.share-box-feed-entry__trigger")
            
            # Wait for editor
            page.wait_for_selector(".ql-editor", state="visible")
            
            # Type post content with human-like delay
            for char in post_content:
                page.type(".ql-editor", char, delay=random.randint(10, 50))
            
            # Add image
            # Wait for media upload button
            page.click("button[aria-label='Add media']")
            
            # File input for image
            page.set_input_files("input[type='file']", image_path)
            
            # Wait for image to upload and click Next/Done
            # Button text might vary, often "Next" or "Done"
            page.wait_for_selector("button.share-box-footer__primary-btn:has-text('Next'), button.share-box-footer__primary-btn:has-text('Done')")
            page.click("button.share-box-footer__primary-btn:has-text('Next'), button.share-box-footer__primary-btn:has-text('Done')")
            
            # Final Post button
            page.wait_for_selector("button.share-actions__primary-action:has-text('Post')")
            
            # Random delay before final post
            time.sleep(random.randint(2, 5))
            
            # page.click("button.share-actions__primary-action:has-text('Post')")
            print("Post button clicked (simulated for now).")
            
            # Save storage state for next time
            context.storage_state(path=session_path)
            
            browser.close()
            return True
            
        except Exception as e:
            print(f"Error during LinkedIn posting: {e}")
            browser.close()
            return False

if __name__ == "__main__":
    # Test
    # post_to_linkedin("Testing TechHook AI Automation", "test_hook.png")
    pass

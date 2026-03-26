import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def main():
    prompts = [
        "US-29_prompt.txt",
        "US-33_prompt.txt",
        "US-35_prompt.txt",
        "US-36_prompt.txt"
    ]
    
    prompt_dir = Path("srs_docs/ready_prompts")
    review_dir = Path("reviews")
    review_dir.mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        try:
            print("Launching Edge browser...")
            user_data_dir = str(Path().absolute() / ".edge_data")
            # Launch persistent context with Edge
            ctx = p.chromium.launch_persistent_context(
                user_data_dir,
                channel="msedge",
                headless=False,
                viewport={"width": 1280, "height": 720},
                args=["--disable-blink-features=AutomationControlled"]
            )
            print("Browser launched.")
        except Exception as e:
            print(f"Failed to launch Edge: {e}")
            return
            
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        
        # Navigate to Claude.ai
        print("Navigating to Claude.ai...")
        try:
            page.goto("https://claude.ai/new", wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print(f"Failed to navigate to Claude.ai: {e}")
            ctx.close()
            return
            
        print("Please check the browser window. If you are not logged in to Claude.ai, log in now.")
        print("Waiting up to 60 seconds for the chat interface to appear...")
        
        # Wait for chat input to be visible (this indicates we are logged in)
        try:
            page.wait_for_selector('div[contenteditable="true"], .ProseMirror', state="visible", timeout=60000)
            print("Logged in successfully.")
        except Exception as e:
            print("Timeout waiting for chat interface. You might not be logged in.")
            ctx.close()
            return

        # Loop through prompts
        for prompt_file in prompts:
            prompt_name = prompt_file.replace("_prompt.txt", "")
            prompt_path = prompt_dir / prompt_file
            out_file = review_dir / f"{prompt_name}_review.json"
            
            print(f"\nProcessing {prompt_name}...")
            
            # Navigate to new chat
            page.goto("https://claude.ai/new", wait_until="domcontentloaded", timeout=60000)
            print("Loaded /new. Waiting for input box...")
            try:
                page.wait_for_selector('div[contenteditable="true"], .ProseMirror', state="visible", timeout=60000)
                print("Input box found. Attaching file...")
            except Exception as e:
                print(f"Timeout waiting for Input box: {e}")
                page.screenshot(path=f"error_{prompt_name}.png", full_page=True)
                continue
            
            # Attach file using the file input if available
            try:
                # Find the file input (Claude usually has a hidden file input)
                file_input = page.locator('input[type="file"]')
                file_input.set_input_files(str(prompt_path.absolute()))
                time.sleep(2) # Wait for upload to register
            except Exception as e:
                print(f"Failed to attach file: {e}")
                continue
                
            # Type instruction
            instruction = "Evaluate this document strictly following its internal instructions. Return ONLY the JSON result. No markdown formatted code blocks, no conversational text. Just the `{}` or `[]` JSON."
            page.fill('div[contenteditable="true"], .ProseMirror', "")
            page.keyboard.insert_text(instruction)
            time.sleep(0.5)
            
            # Submit
            page.keyboard.press("Enter")
            print("Prompt submitted. Waiting for generation to complete...")
            
            # Wait for generation (we wait for the "Copy" button to appear on the last message, or generic wait)
            # Claude's stop generation button usually has aria-label="Stop generating" or similar, 
            # and when done, a "Copy" button appears.
            try:
                page.wait_for_selector('button[aria-label="Copy message"]', state="visible", timeout=120000)
                print("Generation complete.")
            except Exception as e:
                print("Timeout waiting for generation to complete, or could not find the Copy button.")
                # We'll just try to extract the last message text anyway
                time.sleep(5)
                
            # Extract last message
            try:
                messages = page.locator('.font-claude-message, .whitespace-pre-wrap')
                count = messages.count()
                if count > 0:
                    last_msg = messages.nth(count - 1).inner_text()
                    out_file.write_text(last_msg, encoding="utf-8")
                    print(f"Saved {len(last_msg)} chars to {out_file}")
                else:
                    print(f"Could not find any message text for {prompt_name}.")
            except Exception as e:
                print(f"Failed to extract message: {e}")
            
            time.sleep(2)
            
        print("\nAll files processed.")
        ctx.close()

if __name__ == "__main__":
    main()

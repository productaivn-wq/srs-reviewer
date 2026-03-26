from playwright.sync_api import sync_playwright

def snapshot_hanging_tab():
    with sync_playwright() as pw:
        # Connect to existing Chrome CDP
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        page = None
        for ctx in browser.contexts:
            for p in ctx.pages:
                if "claude.ai/code" in p.url.lower():
                    page = p
                    break
        if not page:
            print("No Claude page found.")
            return
            
        print("Page URL:", page.url)
        page.screenshot(path="claude_hanging.png")
        print("Saved snapshot to claude_hanging.png")
        
        # Look for stop or submit buttons
        buttons = page.locator('button').all()
        for b in buttons:
            try:
                if b.is_visible():
                    aria = b.get_attribute('aria-label') or ""
                    title = b.get_attribute('title') or ""
                    text = b.text_content() or ""
                    print(f"Button: text='{text}', aria='{aria}', title='{title}', disabled={b.is_disabled()}")
            except Exception:
                pass

if __name__ == "__main__":
    snapshot_hanging_tab()

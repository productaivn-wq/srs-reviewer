from playwright.sync_api import sync_playwright

def test_viewport():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        page = None
        for ctx in browser.contexts:
            for p in ctx.pages:
                if "claude" in p.url.lower():
                    page = p
                    break
                    
        if not page:
            return
            
        print("Old viewport:", page.viewport_size)
        page.set_viewport_size({"width": 1920, "height": 1080})
        print("New viewport:", page.viewport_size)
        
        # Also wait a moment for CSS relayout
        page.wait_for_timeout(1000)
        
        box = page.locator('.tiptap').first
        print("Box bounding rect:", box.bounding_box())
        print("Box visible?", box.is_visible())
        
        if box.is_visible():
            print("Clicking...")
            box.click()
            page.keyboard.type("Viewport resizing worked!")
            print("Typed successfully.")

if __name__ == "__main__":
    test_viewport()

import json
from playwright.sync_api import sync_playwright

p = sync_playwright().start()
b = p.chromium.connect_over_cdp('http://localhost:9333')
pages = [page for ctx in b.contexts for page in ctx.pages if 'claude' in page.url.lower()]

if not pages:
    print("No Claude pages")
else:
    page = pages[-1]
    
    html = page.evaluate('''() => {
        let res = {
            buttons: [],
            editors: [],
            last_text: ""
        };
        
        document.querySelectorAll('button, [role="button"], a').forEach(btn => {
            const rect = btn.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                res.buttons.push({
                    text: (btn.textContent || '').trim(),
                    aria: btn.getAttribute('aria-label') || '',
                    disabled: btn.disabled || false
                });
            }
        });
        
        document.querySelectorAll('div[contenteditable="true"], .tiptap').forEach(ed => {
            const rect = ed.getBoundingClientRect();
            res.editors.push({
                width: rect.width,
                height: rect.height,
                visible: rect.width > 0 && rect.height > 0
            });
        });
        
        const textBlocks = document.querySelectorAll('.font-claude-message, .prose, [class*="message"]');
        if (textBlocks.length > 0) {
            res.last_text = textBlocks[textBlocks.length - 1].textContent.trim().substring(0, 200);
        }
        
        return res;
    }''')
    
    print(json.dumps(html, indent=2))

p.stop()

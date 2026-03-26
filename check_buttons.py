import json
from playwright.sync_api import sync_playwright

p = sync_playwright().start()
b = p.chromium.connect_over_cdp('http://localhost:9333')
pages = [page for ctx in b.contexts for page in ctx.pages if 'claude' in page.url.lower()]
if not pages:
    with open('buttons.json', 'w', encoding='utf-8') as f:
        f.write('[]')
else:
    page = pages[0]
    btns = page.query_selector_all('button, [role="button"]')
    data = []
    for el in btns:
        data.append({
            'text': el.inner_text().strip() if el.inner_text() else '',
            'aria': el.get_attribute('aria-label') or '',
            'disabled': el.is_disabled(),
            'class': el.get_attribute('class') or '',
            'title': el.get_attribute('title') or ''
        })
    with open('buttons.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
p.stop()

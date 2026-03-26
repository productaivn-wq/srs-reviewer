import sys
import time
import os

sys.path.append(r"c:\Users\thanb\.gemini\antigravity\skills\TaskOrchestrator\scripts")
import claude_code_web

pw, browser, page = claude_code_web.connect_cdp(new_tab=True)
print("Connected to", page.url)

claude_code_web.paste_and_submit(page, "Write a 3 word poem.")

print("Submitted. Waiting 15s for completion...")
time.sleep(15)

info = page.evaluate('''() => {
    let res = [];
    document.querySelectorAll('button, [role="button"], a').forEach(btn => {
        const rect = btn.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0) {
            const aria = (btn.getAttribute('aria-label') || '').toLowerCase();
            const text = (btn.textContent || '').trim();
            res.push(`Text:"${text}" Aria:"${aria}" Disabled:${btn.disabled} classes:${btn.className}`);
        }
    });
    return res;
}''')

print("ALL VISIBLE BUTTONS:")
for b in info:
    print(b)

# Also let's check input boxes
inputs = page.evaluate('''() => {
    let res = [];
    document.querySelectorAll('div[contenteditable="true"]').forEach(el => {
        const rect = el.getBoundingClientRect();
        res.push(`ContentEditable w:${Math.round(rect.width)} h:${Math.round(rect.height)}`);
    });
    return res;
}''')
print("INPUTS:", inputs)

page.close()
pw.stop()

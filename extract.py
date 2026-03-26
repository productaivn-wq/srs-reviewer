import subprocess, sys, json, os
cmd = ['python', 'c:/Users/thanb/.gemini/antigravity/skills/PlaywrightBrowser/scripts/browser_cli.py', 'dom', 'body']
env = os.environ.copy()
env['PYTHONIOENCODING'] = 'utf-8'
res = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding='utf-8', errors='ignore')
if res.returncode != 0:
    print("FAILED")
    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)
    sys.exit(1)
data = json.loads(res.stdout)
text = data.get('data', {}).get('content', '')
with open(r'c:\Users\thanb\.gemini\projects\SRSReviewer\srs_docs\US-33_Quan_ly_Consent.md', 'w', encoding='utf-8') as f:
    f.write(text)
print("SUCCESS")

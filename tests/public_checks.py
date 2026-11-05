"""Verify the actual Pages release after a main push; never substitutes local routes."""
import hashlib,json,time,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1]
BASE='https://teruluce.github.io/disney-discovery/'
expected=hashlib.sha256((ROOT/'assets/css/magazine.css').read_bytes()).digest()
for attempt in range(40):
    try:
        req=urllib.request.Request(BASE+'assets/css/magazine.css',headers={'Cache-Control':'no-cache'})
        with urllib.request.urlopen(req,timeout=20) as r:
            if hashlib.sha256(r.read()).digest()==expected:
                with urllib.request.urlopen(urllib.request.Request(BASE,headers={'Cache-Control':'no-cache'}),timeout=20) as home:
                    if b'assets/css/magazine.css' in home.read():break
    except Exception as exc:
        print('Waiting for Pages release:',type(exc).__name__,flush=True)
    time.sleep(15)
else:raise SystemExit('Pages did not serve the expected release CSS within 10 minutes')
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(extra_http_headers={'Cache-Control':'no-cache'})
    for path in ['', 'articles/', 'articles/first-visit-checklist.html','articles/tdr-history-timeline.html','journal/','journal/resort-line-stamp-rally-2026.html','en/','en/articles/getting-there-by-train.html']:
        for width in (390,1440):
            page.set_viewport_size({'width':width,'height':900})
            response=page.goto(BASE+path,wait_until='networkidle')
            assert response.status==200,(path,response.status)
            assert page.locator('h1').is_visible()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),path
            assert page.locator('link[href$="magazine.css"]').count()==1
        print('LIVE PASS',path or '/',flush=True)
    page.goto(BASE)
    expect(page.locator('.cover-image img')).to_have_js_property('complete',True)
    assert page.locator('.cover-image img').evaluate('(e)=>e.naturalWidth>0')
    for width,prefix in [(390,''),(390,'en/')]:
        page.set_viewport_size({'width':width,'height':844});page.goto(BASE+prefix)
        page.locator('summary').focus();page.keyboard.press('Enter')
        assert page.locator('.nav-disclosure nav').is_visible()
    for path in ['articles/','en/articles/']:
        page.goto(BASE+path)
        page.locator('#article-query').fill('モバイルオーダー' if path=='articles/' else 'Suica')
        expect(page.locator('#article-list > li:visible a[href$="' + ('disney-mobile-order-guide.html' if path=='articles/' else 'suica-payment-guide.html') + '"]')).to_be_visible()
    transitions=json.loads((ROOT/'tests/fixtures/article-reorganization.json').read_text())['transitions']
    for path,row in transitions.items():
        page.goto(BASE+path)
        if row['action']=='merge':
            page.wait_for_url(BASE+row['target']+'#'+row['fragment'])
        else:
            assert page.locator('meta[name="robots"]').get_attribute('content')=='noindex,follow'
    for old,target in [('articles/chip-and-dale-difference.html','articles/chip-and-dale-guide.html'),('articles/disney-first-timer-app-day-plan.html','articles/first-visit-checklist.html'),('articles/resort-line-stamp-rally-2026.html','journal/resort-line-stamp-rally-2026.html')]:
        page.goto(BASE+old);page.wait_for_url('**/'+target+'*')
    browser.close()
print('LIVE PASS: deployed CSS matches release; responsive pages, images, Japanese/English menus, search, 11 notices and all 6 redirects',flush=True)

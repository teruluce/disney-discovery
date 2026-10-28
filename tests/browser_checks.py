"""Browser regressions for static pages. Run after installing tests/requirements.txt."""
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, unquote
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from site_support import BASE, ROOT, documents, is_redirect


def serve(route):
    url = urlsplit(route.request.url)
    if url.netloc != 'teruluce.github.io' or not url.path.startswith('/disney-discovery/'):
        route.abort()
        return
    relative = unquote(url.path[len('/disney-discovery/'):])
    if not relative or relative.endswith('/'):
        relative += 'index.html'
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT):
        route.abort()
        return
    exists = path.is_file()
    if not exists:
        path = ROOT / '404.html'
    kind = {'.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'application/javascript',
            '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml'}.get(path.suffix, 'text/plain')
    route.fulfill(status=200 if exists else 404, content_type=kind, body=path.read_bytes())


def visible(page):
    return page.locator('#article-list > li:visible').count()


def luminance(color):
    c = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return sum(x * weight for x, weight in zip(c, (.2126, .7152, .0722)))


def contrast(a, b):
    high, low = sorted([luminance(a), luminance(b)], reverse=True)
    return (high + .05) / (low + .05)


with sync_playwright() as p:
    engine = os.environ.get('BROWSER', 'chromium')
    kwargs = {'headless': True}
    if os.environ.get('CHROMIUM_PATH') and engine == 'chromium':
        kwargs.update(executable_path=os.environ['CHROMIUM_PATH'], args=['--no-sandbox'])
    browser = getattr(p, engine).launch(**kwargs)
    context = browser.new_context(viewport={'width': 390, 'height': 844})
    context.route('**/*', serve)
    page = context.new_page()
    page.set_default_timeout(5000)
    errors, failed = [], []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('console', lambda message: errors.append(message.text) if message.type == 'error' else None)
    page.on('requestfailed', lambda request: failed.append(request.url))
    # Every content page must render under the actual meta CSP and load its local resources.
    for path, doc in documents().items():
        if is_redirect(doc):
            continue
        response = page.goto(BASE + path, wait_until='load')
        assert response.status == 200, path
        assert page.locator('h1').is_visible(), path
    assert not errors and not failed, (errors, failed)
    print('PASS: all content pages render without script, CSP or resource errors')

    for path in ['', 'articles/', 'profile.html', 'articles/first-visit-checklist.html',
                 'articles/disney-mobile-order-guide.html', 'en/', 'en/articles/getting-there-by-train.html']:
        page.goto(BASE + path)
        for width in [320, 390, 768, 960, 1440]:
            page.set_viewport_size({'width': width, 'height': 900})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (path, width)
        page.set_viewport_size({'width': 390, 'height': 844})
        toggle = page.locator('summary.menu-toggle')
        toggle.focus()
        page.keyboard.press('Enter')
        assert page.locator('.nav-disclosure nav').is_visible(), path
        page.keyboard.press('Enter')
        assert not page.locator('.nav-disclosure nav').is_visible(), path
    print('PASS: seven page layouts at five widths; keyboard menu activation')

    page.goto(BASE + 'articles/')
    assert visible(page) == 51
    chips = page.locator('.filter-chip')
    assert sum(int(re.search(r'（(\d+)）', x).group(1)) for x in chips.all_text_contents()[1:]) == 51
    tips = page.locator('.filter-chip').filter(has_text='パークを楽しむヒント')
    tips.focus()
    page.keyboard.press('Enter')
    assert visible(page) == int(re.search(r'（(\d+)）', tips.inner_text()).group(1))
    assert page.locator('#article-list > li:visible a[href$="resort-line-stamp-rally-2026.html"]').count() == 1
    query = page.locator('#article-query')
    query.fill('見つからない記事 <script>alert(1)</script>')
    page.wait_for_timeout(250)
    assert visible(page) == 0 and page.locator('#article-empty').is_visible()
    page.locator('#article-reset').click()
    assert visible(page) == 51 and query.evaluate('(e) => document.activeElement === e')
    query.fill('ﾓﾊﾞｲﾙｵｰﾀﾞｰ')
    page.wait_for_timeout(250)
    assert visible(page) >= 1
    assert 'モバイルオーダー' in page.locator('#article-list > li:visible').first.inner_text()
    assert page.locator('#article-status').get_attribute('role') == 'status'
    page.goto(BASE + 'en/articles/')
    page.locator('#article-query').fill('ＥＬＥＣＴＲＩＣＡＬ')
    page.wait_for_timeout(250)
    assert visible(page) == 1
    print('PASS: complete category coverage, combined search, normalization, no results, reset and live status')

    page.goto(BASE + 'articles/first-visit-checklist.html')
    table = page.locator('.table-wrap').first
    table.scroll_into_view_if_needed()
    table.focus()
    page.keyboard.press('ArrowRight')
    page.wait_for_timeout(200)
    assert table.evaluate('(e) => e.scrollLeft > 0')
    page.goto(BASE + 'articles/missing/audit.html')
    home = page.locator('.breadcrumb a').first
    assert home.get_attribute('href') == BASE
    home.click()
    assert page.url == BASE
    print('PASS: keyboard table scrolling and nested 404 recovery')

    page.emulate_media(color_scheme='dark', reduced_motion='reduce')
    page.goto(BASE)
    assert page.locator('body').evaluate('(e) => getComputedStyle(e).backgroundColor') == 'rgb(251, 252, 255)'
    assert page.locator('html').evaluate('(e) => getComputedStyle(e).scrollBehavior') == 'auto'
    for color in ['#315cae', '#315b85', '#6757af']:
        assert contrast(color, '#d4e2ff') >= 3, color
    for color in ['#315cae', '#6757af']:
        assert contrast(color, '#ffffff') >= 4.5, color
    assert page.locator('.grad-text').evaluate('(e) => getComputedStyle(e).backgroundImage').find('49, 92, 174') >= 0
    assert page.locator('.button').first.evaluate('(e) => getComputedStyle(e).backgroundImage').find('49, 92, 174') >= 0
    page.emulate_media(forced_colors='active')
    assert page.locator('.grad-text').evaluate('(e) => getComputedStyle(e).color') != 'rgba(0, 0, 0, 0)'
    print('PASS: fixed light theme, reduced motion, forced colors and headline/button contrast')

    plain = browser.new_context(java_script_enabled=False, viewport={'width': 390, 'height': 844})
    plain.route('**/*', serve)
    nojs = plain.new_page()
    for path, count in [('articles/', 51), ('en/articles/', 10)]:
        nojs.goto(BASE + path)
        assert visible(nojs) == count
        assert not nojs.locator('#article-controls').is_visible()
        nojs.locator('summary').click()
        assert nojs.locator('.nav-disclosure nav').is_visible()
    print('PASS: all articles and mobile navigation remain available without JavaScript')
    browser.close()

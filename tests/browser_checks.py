"""Browser regressions for static pages. Run after installing tests/requirements.txt."""
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, unquote
from playwright.sync_api import sync_playwright, expect

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
            '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml',
            '.woff2': 'font/woff2'}.get(path.suffix, 'text/plain')
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
                 'articles/disney-mobile-order-guide.html', 'articles/ticket-change-cancellation-guide.html', 'en/', 'en/articles/getting-there-by-train.html', 'en/articles/park-etiquette.html', 'journal/', 'journal/resort-line-stamp-rally-2026.html', 'en/articles/suica-payment-guide.html']:
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
    print('PASS: twelve page layouts at five widths; keyboard menu activation')

    page.goto(BASE + 'articles/')
    assert visible(page) == 38
    chips = page.locator('.filter-chip')
    assert sum(int(re.search(r'（(\d+)）', x).group(1)) for x in chips.all_text_contents()[1:]) == 38
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
    assert visible(page) == 38 and query.evaluate('(e) => document.activeElement === e')
    query.fill('ﾓﾊﾞｲﾙｵｰﾀﾞｰ')
    page.wait_for_timeout(250)
    assert visible(page) >= 1
    assert 'モバイルオーダー' in page.locator('#article-list > li:visible').first.inner_text()
    assert page.locator('#article-status').get_attribute('role') == 'status'
    page.goto(BASE + 'en/articles/')
    page.locator('#article-query').fill('ＥＬＥＣＴＲＩＣＡＬ')
    page.wait_for_timeout(250)
    assert visible(page) == 1
    page.locator('#article-query').fill('etiquette')
    page.wait_for_timeout(250)
    assert page.locator('#article-list > li:visible a[href="park-etiquette.html"]').count() == 1
    page.locator('#article-list a[href="park-etiquette.html"]').click()
    assert page.locator('h1').inner_text() == 'Tokyo Disney Resort Etiquette: Park Rules & Japanese Customs'
    page.locator('a[href="#viewing"]').click()
    assert page.url.endswith('#viewing')
    page.locator('article a[href="park-photography.html"]').click()
    assert page.url.endswith('/park-photography.html')
    page.goto(BASE + 'en/articles/')
    page.locator('#article-query').fill('Suica')
    page.wait_for_timeout(250)
    assert visible(page) == 1
    page.locator('#article-list > li:visible a[href="suica-payment-guide.html"]').click()
    assert page.url.endswith('/en/articles/suica-payment-guide.html')
    page.locator('a[href="what-to-pack.html"]').click()
    page.locator('a[href="suica-payment-guide.html"]').click()
    assert page.locator('#top-up').is_visible()
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
    assert page.locator('html').evaluate('(e) => getComputedStyle(e).backgroundColor') == 'rgb(248, 247, 243)'
    for label in ['初めて行く方へ', '舞浜へのアクセス']:
        link = page.locator('.quick-links a').filter(has_text=label)
        assert link.is_visible()
        assert link.bounding_box()['y'] + link.bounding_box()['height'] <= 844
    for path in ['profile.html', 'articles/', 'articles/first-visit-checklist.html', 'journal/', 'en/', 'en/articles/first-visit.html']:
        page.goto(BASE + path)
        assert page.locator('body').evaluate('(e) => getComputedStyle(e).backgroundColor') == 'rgb(248, 247, 243)'
        assert page.locator('h1').evaluate('(e) => getComputedStyle(e).color') == 'rgb(39, 59, 58)'
        assert 'serif' in page.locator('h1').evaluate('(e) => getComputedStyle(e).fontFamily')
    for ink, paper in [('#273b3a', '#f8f7f3'), ('#5d6763', '#f8f7f3'), ('#ffffff', '#355b50')]:
        assert contrast(ink, paper) >= 4.5
    page.emulate_media(forced_colors='active')
    assert page.locator('h1').evaluate('(e) => getComputedStyle(e).color') != 'rgba(0, 0, 0, 0)'
    print('PASS: shared magazine design, readable contrast, reduced motion and forced colors')

    plain = browser.new_context(java_script_enabled=False, viewport={'width': 390, 'height': 844})
    plain.route('**/*', serve)
    nojs = plain.new_page()
    for path, count in [('articles/', 38), ('en/articles/', 12)]:
        nojs.goto(BASE + path)
        assert visible(nojs) == count
        assert not nojs.locator('#article-controls').is_visible()
        nojs.locator('summary').click()
        assert nojs.locator('.nav-disclosure nav').is_visible()
    print('PASS: all articles and mobile navigation remain available without JavaScript')
    for client in (page, nojs):
        client.goto(BASE + 'journal/')
        client.locator('.journal-card').click()
        assert client.url.endswith('/journal/resort-line-stamp-rally-2026.html')
        client.locator('article img').scroll_into_view_if_needed()
        expect(client.locator('article img')).to_have_js_property('complete', True)
        expect(client.locator('article img')).to_have_js_property('naturalWidth', 900)
        assert client.locator('time.experience-date').get_attribute('datetime') == '2026-10-18'
        client.goto(BASE + 'articles/resort-line-stamp-rally-2026.html#my-stamp')
        client.wait_for_url('**/journal/resort-line-stamp-rally-2026.html*')
        assert client.locator('article figure').count() == 1
    # Also inspect the fallback HTML itself; meta refresh works even without JS.
    fallback = (ROOT / 'articles/resort-line-stamp-rally-2026.html').read_text()
    assert 'href="../journal/resort-line-stamp-rally-2026.html"' in fallback
    assert 'noindex,follow' in fallback
    for width in (1200, 1440):
        page.set_viewport_size({'width': width, 'height': 900})
        page.goto(BASE)
        assert page.locator('.site-nav-inline').is_visible()
        assert page.locator('.site-nav-inline a').filter(has_text='Journal').is_visible()
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    print('PASS: Journal cards, photo, date, old URL with/without JS and desktop navigation')
    for client in (page, nojs):
        client.emulate_media(forced_colors='none', reduced_motion='reduce')
        client.goto(BASE)
        client.locator('.entrances a[href="#journal"]').click()
        assert client.url.endswith('#journal')
        client.locator('.journal-photo img').scroll_into_view_if_needed()
        expect(client.locator('.journal-photo img')).to_have_js_property('naturalWidth', 900)
        client.locator('#journal a[href="journal/resort-line-stamp-rally-2026.html"]').first.click()
        assert client.url.endswith('/journal/resort-line-stamp-rally-2026.html')
        client.goto(BASE + 'en/')
        for slug in ('getting-there-by-train', 'suica-payment-guide', 'park-etiquette', 'park-photography', 'first-visit'):
            assert client.locator('.latest-section a[href="articles/' + slug + '.html"]').is_visible()
        client.locator('#journal a[href="../journal/"]').click()
        assert client.url.endswith('/journal/')
    print('PASS: reorganized Japanese/English homepage journeys with and without JavaScript')
    # Approved retirement notices and consolidation routes must work without JS, too.
    import json
    transitions = json.loads((ROOT / 'tests/fixtures/article-reorganization.json').read_text())['transitions']
    for client in (page, nojs):
        for path, transition in transitions.items():
            client.goto(BASE + path + '#sources')
            if transition['action'] == 'retire':
                assert client.url.split('#')[0] == BASE + path
                assert client.locator('h1').inner_text() == 'この記事の公開は終了しました'
                assert client.locator('meta[name="robots"]').get_attribute('content') == 'noindex,follow'
                assert client.locator('article').count() == 0
            else:
                client.wait_for_url(BASE + transition['target'] + '#' + transition['fragment'])
                assert client.locator('#' + transition['fragment']).is_visible()
        client.goto(BASE + 'articles/')
        for path in transitions:
            assert client.locator('#article-list a[href$="' + path.split('/')[-1] + '"]').count() == 0
    for width in (320, 390):
        page.set_viewport_size({'width': width, 'height': 844})
        page.goto(BASE)
        for link in page.locator('.entrances > a').all():
            box = link.bounding_box()
            assert box['y'] + box['height'] <= 844
        cover = page.locator('.cover-image img')
        expect(cover).to_have_js_property('complete', True)
        assert cover.evaluate('(e) => e.naturalWidth > 0 && Math.abs(e.naturalWidth / e.naturalHeight - 4/3) < .01')
        assert cover.evaluate('(e) => Math.abs(e.getBoundingClientRect().width / e.getBoundingClientRect().height - 4/3) < .01')
        assert cover.evaluate('(e) => getComputedStyle(e).objectFit') == 'contain'
        assert '写真：てる' in page.locator('.cover-image figcaption').inner_text()
        assert page.locator('#discover .photo-slot').count() == 0
        assert page.locator('.quick-links').bounding_box()['y'] < page.locator('.cover-image').bounding_box()['y']
    print('PASS: 11 ended notices and 3 section redirects with/without JS; 3 mobile entrances in first screen')
    browser.close()


# On the authorized main release, also verify the actual deployed Pages site.
if os.environ.get('GITHUB_EVENT_NAME') == 'push' and os.environ.get('GITHUB_REF') == 'refs/heads/main':
    import runpy
    runpy.run_path(str(ROOT / 'tests/public_checks.py'), run_name='__main__')

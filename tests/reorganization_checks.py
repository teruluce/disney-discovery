"""Protect existing article URLs, redirects and English content during reorganization."""
import hashlib
import json
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from site_support import ROOT, documents, is_redirect, is_retired

docs = documents()
articles = {p: d for p, d in docs.items()
            if p.startswith(('articles/', 'en/articles/', 'journal/'))
            and not p.endswith('index.html') and not is_redirect(d) and not is_retired(d)}
fixture = json.loads((ROOT / 'tests/fixtures/article-reorganization.json').read_text())
transitions = fixture['transitions']
retired = {p for p, r in transitions.items() if r['action'] == 'retire'}
merged = {p for p, r in transitions.items() if r['action'] == 'merge'}
assert len(retired) == 11 and len(merged) == 3
assert set(articles) == set(fixture['original_articles']) - retired - merged
assert len(articles) == 50 and sum(p.startswith('en/') for p in articles) == 12
assert {p for p, d in docs.items() if is_retired(d)} == retired
for path, digest in fixture['protected_hashes'].items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
for path, digest in fixture['protected_main_hashes'].items():
    body = re.search(r'<main\b[\s\S]*?</main>', (ROOT / path).read_text())[0]
    assert hashlib.sha256(body.encode()).hexdigest() == digest, path
for path in retired:
    d = docs[path]
    assert d.meta('robots') == 'noindex,follow' and not is_redirect(d)
    assert d.link('canonical').endswith(path)
    assert not d.all('article') and not any('Article' in n.text for n in d.all('script'))
for path in merged:
    row, d = transitions[path], docs[path]
    assert is_redirect(d) and d.meta('robots') == 'noindex,follow'
    assert d.link('canonical').endswith(row['target'])
    target = docs[row['target']]
    assert any(n.attrs.get('id') == row['fragment'] for n in target.all())
    links = {a.attrs.get('href') for a in target.all('a')}
    for url in row['external_links']:
        normalized = {'https://www.tokyodisneyresort.jp/tdl/show/': 'https://www.tokyodisneyresort.jp/tdl/show.html',
                      'https://www.tokyodisneyresort.jp/tds/show': 'https://www.tokyodisneyresort.jp/tds/show.html'}.get(url, url)
        assert normalized in links, (path, url)
for path, digest in {'articles/chip-and-dale-difference.html': '232bf758d22886cb4ce1532a847e1b196a89e4e78d12e10acea5c6dfe204bd96', 'articles/disney-first-timer-app-day-plan.html': '2ab72f810b84d415133e2f5b49c4c6d858dafc52baeca733a8cf917441a17bae', 'articles/resort-line-stamp-rally-2026.html': '9092900f087153e42027e33c1a8fa0dca26e58b6c2e9c0afc6a95256f1589911'}.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
assert {p for p, d in docs.items() if is_redirect(d)} - merged == set({'articles/chip-and-dale-difference.html': '232bf758d22886cb4ce1532a847e1b196a89e4e78d12e10acea5c6dfe204bd96', 'articles/disney-first-timer-app-day-plan.html': '2ab72f810b84d415133e2f5b49c4c6d858dafc52baeca733a8cf917441a17bae', 'articles/resort-line-stamp-rally-2026.html': '9092900f087153e42027e33c1a8fa0dca26e58b6c2e9c0afc6a95256f1589911'})
for path, digest in {'en/articles/electrical-parade.html': '7a95e4b23febe493d586c9dc665b101eecc811f0bfbf833ef12faf6820a6a3d1', 'en/articles/first-visit.html': 'c9f5582e3b043361feb1d4d53f6fe2beb16673ad9bca5e261d9679c56364c2c2', 'en/articles/getting-there-by-train.html': '975706afd9c4e2dcb64c8b579520c0ad2ca8e502da16441f6474276bef3be565', 'en/articles/land-vs-sea.html': '2df51be1db6b74b22219020159d8cf4c017f5c9d74ef4eb399c4ecf77fd58c42', 'en/articles/official-app-guide.html': '839c5ec8d64e396e366573bb73dd1630611b39212280aa88b44ebc6b3c44e9a4', 'en/articles/park-etiquette.html': '617c7798d1768f639d7d92421bb342bd2da2a1e35e5cafd8f0d38c8caa7a5c25', 'en/articles/park-photography.html': '5d529719ec2e5033b5e9dcbc958a335e3a92f2d26228e57b000759ba43389083', 'en/articles/rainy-day.html': 'c3957ad14f013e9ad548a8f3e83001bbdc167debd97c4c90b56eb3ba24f8571b', 'en/articles/suica-payment-guide.html': '33f4983147ad2a3b9575e05108052335526126610ecc70958cfa95fcbc43e84a', 'en/articles/ticket-basics.html': 'cfbed054cdbe1e32107412c5b7572cbacfdd30c2affdad83645aca69b7cf1823', 'en/articles/unique-tokyo-disneysea.html': '768a23f0129ab423447dc5d342af75313ef5a31401aa9e8c1b983e2b78ae4cde', 'en/articles/what-to-pack.html': 'cc75d05bc9b18c76b2c04bece9e919bd8bb24cc53d6a42d5a4e335bf6ed0e5ba'}.items():
    body = re.search(r'<main\b[\s\S]*?</main>', (ROOT / path).read_text())[0]
    assert hashlib.sha256(body.encode()).hexdigest() == digest, path
print('PASS: 50 active articles, 11 noindex notices, 3 merged routes; English/Journal bodies and 3 original redirects unchanged')

# Public cover derivatives must never reintroduce capture metadata from the private source.
for name in ('cover-courtyard-teru-640.jpg', 'cover-courtyard-teru-1280.jpg'):
    data = (ROOT / 'assets/img' / name).read_bytes()
    assert data[:2] == b'\xff\xd8'
    offset = 2
    while offset < len(data):
        assert data[offset] == 0xff
        while data[offset] == 0xff:
            offset += 1
        marker = data[offset]
        offset += 1
        if marker in (0xda, 0xd9):  # Compressed scan / end of JPEG headers.
            break
        assert marker not in (0xe1, 0xe2, 0xed, 0xfe), (name, 'EXIF/XMP, ICC/MPF, Photoshop/IPTC or comment metadata')
        size = int.from_bytes(data[offset:offset + 2], 'big')
        assert size >= 2
        offset += size
print('PASS: both public cover JPEGs contain no EXIF/GPS, XMP, ICC/MPF, IPTC or comments')

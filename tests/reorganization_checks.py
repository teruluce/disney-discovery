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
for path, digest in {'en/articles/electrical-parade.html': '47e36fcb27d57cdf5821cc99d99ef65bdf39e748e91a96f5a0144c4341c9ca26', 'en/articles/first-visit.html': '72dad1a2dfb7054170fdf850a3cb389595029227441af8e4924018fa836cc71c', 'en/articles/getting-there-by-train.html': '3ec082fe9b1a6a915dd2c9fafc7eab21c33846197dffea3b0125942ba628ce17', 'en/articles/land-vs-sea.html': '564683be30d4f1095b0892d2ae3a66a5558cc20bd26eb65d9140a5a406fdf4f0', 'en/articles/official-app-guide.html': 'aae528e59bbb1987fbf2a64ad15dd1f32c9c5b749a99c0deaf171ab72db3386d', 'en/articles/park-etiquette.html': '7be267fd294efd8e65b7f45394a3885135372fcc85d4bc56b9cb29276f637e16', 'en/articles/park-photography.html': 'fe467368643f1f5b010cd5602ba9a780f934b11c7b4a37ae505f31d88c990b05', 'en/articles/rainy-day.html': 'd4c6e958e7ac528b62fe60f1d8d4685beb2845d5ac954285a937ebf43be1eef6', 'en/articles/suica-payment-guide.html': 'd95f7cf5719000d079bbccbfd193c8031957a16b0a76dffdda70ee5b3ce2d1d1', 'en/articles/ticket-basics.html': '5180c2f0d9f8ff72e662aefd5127aacc4d37d81f3e95ed02a58fcd927a1331ee', 'en/articles/unique-tokyo-disneysea.html': '84295fe63b4d5fe5968739ea2fb970b2eb8bdc9f672dc767346d658db755f4b5', 'en/articles/what-to-pack.html': '7f9192c93805a16c9c7c10389320be5b811580efd0ceb83edc6b47e319aeaa02'}.items():
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

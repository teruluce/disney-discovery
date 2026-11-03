"""Guard the record's photo and facts after owner-authorized prose editing.

2026-11-03: the owner requested a friendlier voice, past tense for the ended
anniversary rally, and the upcoming Christmas version. Whole-prose digests from
the migration no longer apply; the original H1, figure and JPEG stay protected.
"""
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'journal/resort-line-stamp-rally-2026.html').read_text()
for pattern, digest in [
    (r'<figure>[\s\S]*?</figure>', 'a6f9be1143d3fb04bd09610bce5e1245aa571217a8ce9ab71e58f0e8d06d2b49'),
    (r'<h1>.*?</h1>', '224ea8b4446451a357b27e7962e6ab60b8183d5d264d3a7588aacc75d7443d6f'),
]:
    content = re.search(pattern, source)[0]
    assert hashlib.sha256(content.encode()).hexdigest() == digest, pattern
photo = (ROOT / 'assets/img/resort-line-stamp-rally-teru.jpg').read_bytes()
assert hashlib.sha1(b'blob ' + str(len(photo)).encode() + b'\0' + photo).hexdigest() == 'dff51e88f96482cad8044535a339c468f2789474'
# Retain the owner's actual memory and the corrected event facts.
body = source.split('<main id="main">', 1)[1].split('</main>', 1)[0]
for fact in ['模試帰り', '2回目', '1回目は失敗', 'うまく押せました',
             '7種類', 'datetime="2026-10-18"', '2026年10月31日で終了しました']:
    assert fact in body, fact
for stale in ['8種類', '開催中', '終了日が近い', 'が開催されています']:
    assert stale not in source, stale
christmas = body.split('<h2 id="christmas">', 1)[1].split('<div class="sources">', 1)[0]
assert '2026年11月10日（火）から12月25日（金）まで開催予定' in christmas
# Keep the pre-existing source/related links alongside the new announcement.
for href in ['https://www.tokyodisneyresort.jp/fantasy/resortline/',
             'https://prtimes.jp/main/html/rd/p/000000091.000038492.html',
             '../articles/tdr-access-guide.html', '../articles/tdr-history-timeline.html']:
    assert 'href="' + href + '"' in body, href
print('PASS: original H1, photo, caption and existing links; memoir facts, ended rally and upcoming Christmas dates')

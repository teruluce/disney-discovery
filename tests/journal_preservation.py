"""Freeze the migrated record against the original HTML and photo (before migration).

Intentional future edits to this personal record require the owner's review before
updating these digests. Owner-authorized amendments on 2026-11-03: seven stamp types (operator release),
mock-exam return / second attempt memory, and the supporting source link.
Normalize only these exact amendments below to keep guarding the original record.
Layout, navigation and generated metadata may evolve.
"""
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'journal/resort-line-stamp-rally-2026.html').read_text()
for pattern, digest in [
    (r'<article class="prose article-body">[\s\S]*?</article>', 'a61753744fc721544e4241757e7dccaec775fccf311068ccbaddfff6f3320acf'),
    (r'<p class="lead">.*?</p>', '27d0515a504ae01afdfff1dc8ee3397acf3a04faca4f23412c4b5f448b704b69'),
    (r'<h1>.*?</h1>', '224ea8b4446451a357b27e7962e6ab60b8183d5d264d3a7588aacc75d7443d6f'),
]:
    content = re.search(pattern, source)[0]
    # Confirm and remove the precise authorized additions before checking the original.
    if pattern.startswith(r'<article'):
        memory = '<p>この日は模試帰りに、リゾートラインのスタンプラリーに参加しました。実は今回が2回目です。1回目は失敗してしまったのですが、この日はうまく押せました。</p>'
        reference = '<li><a href="https://prtimes.jp/main/html/rd/p/000000091.000038492.html" target="_blank" rel="noopener noreferrer">株式会社舞浜リゾートライン｜東京ディズニーシー25周年を記念したスタンプラリーの発表</a>（全7種類・4駅に計7か所のスタンプ台。2026年11月3日確認）</li>'
        assert content.count(memory) == 1 and content.count(reference) == 1
        assert '8種類' not in content
        content = content.replace(memory + '\n', '').replace(reference, '')
    if pattern.startswith(r'<article') or pattern.startswith(r'<p'):
        assert '7種類' in content and '8種類' not in content
    content = content.replace('7種類', '8種類')
    assert hashlib.sha256(content.encode()).hexdigest() == digest, pattern
photo = (ROOT / 'assets/img/resort-line-stamp-rally-teru.jpg').read_bytes()
# Git blob digest from the source repository; no image decoding/re-encoding.
assert hashlib.sha1(b'blob ' + str(len(photo)).encode() + b'\0' + photo).hexdigest() == 'dff51e88f96482cad8044535a339c468f2789474'
print('PASS: owner-authorized amendments present; remaining original article, photo, caption and links preserved')

"""Freeze the migrated record against the original HTML and photo (before migration).

Intentional future edits to this personal record require the owner's review before
updating these digests. Layout, navigation and generated metadata may evolve.
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
    assert hashlib.sha256(content.encode()).hexdigest() == digest, pattern
photo = (ROOT / 'assets/img/resort-line-stamp-rally-teru.jpg').read_bytes()
# Git blob digest from the source repository; no image decoding/re-encoding.
assert hashlib.sha1(b'blob ' + str(len(photo)).encode() + b'\0' + photo).hexdigest() == 'dff51e88f96482cad8044535a339c468f2789474'
print('PASS: original article HTML, lead, H1, photograph, caption and link order preserved')

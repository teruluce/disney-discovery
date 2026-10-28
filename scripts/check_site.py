"""Validate links, article coverage, translations, metadata and CSP before publication."""
import base64
import hashlib
import json
import xml.etree.ElementTree as ET
from site_support import BASE, ROOT, documents, is_redirect, local_target, canonical_path
from sync_metadata import sync


def jpeg_size(path):
    """Read JPEG dimensions without adding an image dependency to the static checks."""
    data = path.read_bytes()
    offset = 2
    while offset < len(data):
        if data[offset] != 255:
            return None
        while data[offset] == 255:
            offset += 1
        marker = data[offset]
        offset += 1
        size = int.from_bytes(data[offset:offset+2], 'big')
        if marker in (0xC0, 0xC1, 0xC2):
            return int.from_bytes(data[offset+5:offset+7], 'big'), int.from_bytes(data[offset+3:offset+5], 'big')
        if size < 2:
            return None
        offset += size
    return None


def check():
    errors = []
    docs = documents()
    def require(ok, message):
        if not ok:
            errors.append(message)
    normal = {p: d for p, d in docs.items() if not is_redirect(d)}
    for path, doc in docs.items():
        ids = [n.attrs['id'] for n in doc.all() if 'id' in n.attrs]
        require(len(ids) == len(set(ids)), path + ': duplicate IDs')
        for node in doc.all():
            for key in ('href', 'src'):
                href = node.attrs.get(key)
                if not href:
                    continue
                target, fragment = local_target(path, href)
                if target is None:
                    continue
                require((ROOT / target).is_file(), f'{path}: missing {href}')
                if fragment and target in docs:
                    require(any(n.attrs.get('id') == fragment for n in docs[target].all()), f'{path}: missing anchor {href}')
            if node.tag == 'a' and node.attrs.get('target') == '_blank':
                require('noopener' in node.attrs.get('rel', '').split(), path + ': unsafe external tab')
            if node.tag == 'img':
                require(bool(node.attrs.get('alt')), path + ': image needs alt text')
                require(all(node.attrs.get(k, '').isdigit() for k in ('width', 'height')), path + ': image dimensions missing')
                image, _ = local_target(path, node.attrs.get('src', ''))
                if image and (ROOT / image).suffix.lower() in ('.jpg', '.jpeg') and (ROOT / image).is_file():
                    declared = tuple(int(node.attrs.get(k, '0')) for k in ('width', 'height'))
                    require(jpeg_size(ROOT / image) == declared, path + ': image dimensions differ from the JPEG')
        if is_redirect(doc):
            target = canonical_path(doc.link('canonical'))
            require(target in normal, path + ': invalid redirect destination')
            continue
        require(len(doc.all('h1')) == 1, path + ': exactly one h1 required')
        require(doc.meta('description') and doc.all('title'), path + ': missing search metadata')
        require(canonical_path(doc.link('canonical')) == path, path + ': canonical mismatch')
        require(doc.all('a', 'skip-link'), path + ': no skip link')
        require(doc.meta('og:title') and doc.meta('og:image'), path + ': missing social metadata')
        policies = [n for n in doc.all('meta') if n.attrs.get('http-equiv') == 'Content-Security-Policy']
        require(len(policies) == 1, path + ': exactly one CSP required')
        policy = policies[0].attrs.get('content', '') if policies else ''
        require("object-src 'none'" in policy and "base-uri 'self'" in policy and "form-action 'none'" in policy, path + ': missing CSP protections')
        require("script-src 'self'" in policy and "'unsafe-inline'" not in policy.split('script-src')[-1].split(';')[0], path + ': unsafe script policy')
        for script in doc.all('script'):
            if not script.attrs.get('src'):
                digest = base64.b64encode(hashlib.sha256(script.text.encode()).digest()).decode()
                require("'sha256-" + digest + "'" in policy, path + ': CSP hash mismatch')
            if script.attrs.get('type') == 'application/ld+json':
                try:
                    data = json.loads(script.text)
                    for item in data.get('@graph', [data]):
                        if item.get('@type') == 'Article':
                            require(item['headline'] == doc.all('h1')[0].text.strip(), path + ': structured headline mismatch')
                            require(item['url'] == doc.link('canonical'), path + ': structured URL mismatch')
                except (ValueError, KeyError) as exc:
                    errors.append(f'{path}: invalid JSON-LD {exc}')
        for link in doc.all('link'):
            if link.attrs.get('rel') == 'alternate' and link.attrs.get('hreflang') in ('ja', 'en'):
                target = canonical_path(link.attrs.get('href', ''))
                require(target in normal, path + ': missing translation')
                if target in normal:
                    require(any(n.attrs.get('rel') == 'alternate' and n.attrs.get('href') == doc.link('canonical')
                                and n.attrs.get('hreflang') == doc.all('html')[0].attrs['lang'] for n in normal[target].all('link')),
                            path + ': non-reciprocal translation link')
    for listing in ('articles/index.html', 'en/articles/index.html'):
        directory = listing.rsplit('/', 1)[0] + '/'
        listed = [local_target(listing, a.attrs['href'])[0] for a in docs[listing].all('a') if 'href' in a.attrs]
        for path in normal:
            if path.startswith(directory) and path != listing:
                require(listed.count(path) == 1, f'{listing}: article must appear exactly once: {path}')
        ids = {n.attrs.get('id') for n in docs[listing].all()}
        require({'article-list', 'article-controls', 'article-status'} <= ids, listing + ': incomplete search controls')
    sitemap = ET.parse(ROOT / 'sitemap.xml')
    urls = [n.text for n in sitemap.findall('.//{*}loc')]
    expected = {d.link('canonical') for p, d in normal.items() if p != '404.html'}
    require(set(urls) == expected and len(urls) == len(set(urls)), 'Sitemap must contain each normal page once, without redirects/404')
    require(not sync(check=True), 'Generated metadata needs updating: run python scripts/sync_metadata.py')
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print(f'PASS: {len(docs)} pages, {len(urls)} sitemap URLs; internal links, anchors, listings, hreflang, JSON-LD and CSP')


if __name__ == '__main__':
    check()

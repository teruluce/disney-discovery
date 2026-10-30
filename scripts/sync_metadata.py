"""Update derived metadata without changing article text. Use --check in CI."""
import argparse
import base64
import hashlib
import html
import json
import re
from site_support import BASE, ROOT, documents, canonical_path, is_redirect

START = '<!-- BEGIN GENERATED METADATA -->'
END = '<!-- END GENERATED METADATA -->'
BLOCK = re.compile(r'\n?' + re.escape(START) + r'[\s\S]*?' + re.escape(END) + r'\n?')


def sync(check=False):
    docs = documents()
    pairs = {p: {} for p in docs}
    for path, doc in docs.items():
        for link in doc.all('link'):
            if link.attrs.get('rel') == 'alternate' and link.attrs.get('hreflang') in ('ja', 'en'):
                target = canonical_path(link.attrs.get('href', ''))
                if target in docs and target != path:
                    pairs[path][link.attrs['hreflang']] = target
                    lang = doc.all('html')[0].attrs['lang']
                    pairs[target][lang] = path
    pairs['articles/index.html']['en'] = 'en/articles/index.html'
    pairs['en/articles/index.html']['ja'] = 'articles/index.html'
    changed = []
    for path, doc in docs.items():
        if is_redirect(doc):
            continue
        source = (ROOT / path).read_text()
        clean = BLOCK.sub('', source)
        doc_without_generated = type(doc)(clean)
        lang = doc.all('html')[0].attrs['lang']
        title = doc.all('title')[0].text
        description = doc.meta('description')
        url = doc.link('canonical')
        article = (path.startswith('articles/') or path.startswith('en/articles/')) and not path.endswith('index.html')
        lines = []
        for key, target in sorted(pairs[path].items()):
            target_url = docs[target].link('canonical')
            if not any(n.attrs.get('hreflang') == key and n.attrs.get('href') == target_url for n in doc_without_generated.all('link')):
                lines.append('<link rel="alternate" hreflang="' + key + '" href="' + target_url + '">')
        if pairs[path] and not any(n.attrs.get('hreflang') == lang for n in doc_without_generated.all('link')):
            lines.append('<link rel="alternate" hreflang="' + lang + '" href="' + url + '">')
        og = {'og:type': 'article' if article else 'website', 'og:site_name': 'Disney Discovery',
              'og:locale': 'en_US' if lang == 'en' else 'ja_JP', 'og:title': title,
              'og:description': description, 'og:url': url, 'og:image': BASE + 'assets/img/og-default.png',
              'twitter:card': 'summary_large_image'}
        for key, value in og.items():
            if not doc_without_generated.meta(key):
                attr = 'name' if key.startswith('twitter:') else 'property'
                lines.append('<meta ' + attr + '="' + key + '" content="' + html.escape(value, quote=True) + '">')
        graph = []
        if article:
            item = {'@type': 'Article', '@id': url + '#article', 'url': url,
                    'headline': doc.all('h1')[0].text.strip(), 'description': description,
                    'inLanguage': lang, 'mainEntityOfPage': url,
                    'publisher': {'@type': 'Organization', 'name': 'Disney Discovery', 'url': BASE}}
            images = doc.all('img')
            if images:
                from urllib.parse import urljoin
                item['image'] = urljoin(url, images[0].attrs['src'])
            graph.append(item)
        if path == 'en/articles/index.html':
            graph.append({'@type': 'CollectionPage', '@id': url + '#collection',
                          'url': url, 'name': doc.all('h1')[0].text.strip(),
                          'description': description, 'inLanguage': lang})
        # Use the visible breadcrumb; do not invent publication dates or translations.
        crumbs = doc.all('nav', 'breadcrumb')
        if crumbs and path != '404.html' and path != 'articles/index.html':
            from urllib.parse import urljoin
            nav = crumbs[0]
            items = [{'@type': 'ListItem', 'position': i + 1, 'name': a.text.strip(),
                      'item': urljoin(url, a.attrs['href'])} for i, a in enumerate(nav.all('a'))]
            items.append({'@type': 'ListItem', 'position': len(items) + 1,
                          'name': nav.text.split('›')[-1].strip(), 'item': url})
            graph.append({'@type': 'BreadcrumbList', 'itemListElement': items})
        if graph:
            lines.append('<script type="application/ld+json">\n' + json.dumps(
                {'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=2).replace('<', '\\u003c') + '\n</script>')
        # A meta policy works on Pages; frame-ancestors and other HTTP-only headers need host support.
        before_policy = clean.replace('</head>', '\n'.join(lines) + '\n</head>', 1)
        hashes = []
        for attributes, content in re.findall(r'<script\b([^>]*)>([\s\S]*?)</script>', before_policy):
            if 'src=' not in attributes:
                hashes.append("'sha256-" + base64.b64encode(hashlib.sha256(content.encode()).digest()).decode() + "'")
        policy = "default-src 'self'; script-src 'self'" + (' ' + ' '.join(hashes) if hashes else '') + "; style-src 'self' 'unsafe-inline'; img-src 'self' data:; object-src 'none'; base-uri 'self'; form-action 'none'"
        # CSP goes before resources, while Open Graph and JSON-LD stay at the end of head.
        csp_re = r'\n?<meta http-equiv="Content-Security-Policy" content="[^"]*">\n?'
        clean = re.sub(csp_re, '', clean)
        csp = '<meta http-equiv="Content-Security-Policy" content="' + html.escape(policy, quote=True) + '">'
        clean = re.sub(r'(<meta charset="utf-8">)', r'\1\n' + csp + '\n', clean, count=1)
        result = clean.replace('</head>', '\n' + START + '\n' + '\n'.join(lines) + '\n' + END + '\n</head>', 1)
        if result != source:
            changed.append(path)
            if not check:
                (ROOT / path).write_text(result)
    return changed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changed = sync(args.check)
    print(('Out-of-date' if args.check else 'Updated') + ' metadata: ' + str(len(changed)) + ' pages')
    if args.check and changed:
        print('\n'.join(changed))
        raise SystemExit(1)

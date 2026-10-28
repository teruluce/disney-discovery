"""Small, dependency-free helpers for the static site's maintenance checks."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://teruluce.github.io/disney-discovery/'
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


class Node:
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    @property
    def text(self):
        return ''.join(c.text if isinstance(c, Node) else c for c in self.children)

    def all(self, tag=None, cls=None):
        found = []
        for child in self.children:
            if isinstance(child, Node):
                if (tag is None or child.tag == tag) and (cls is None or cls in child.attrs.get('class', '').split()):
                    found.append(child)
                found.extend(child.all(tag, cls))
        return found


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)

    def all(self, tag=None, cls=None):
        return self.root.all(tag, cls)

    def meta(self, key):
        return next((n.attrs.get('content', '') for n in self.all('meta') if n.attrs.get('name', n.attrs.get('property')) == key), '')

    def link(self, rel):
        return next((n.attrs.get('href', '') for n in self.all('link') if n.attrs.get('rel') == rel), '')


def documents():
    return {p.relative_to(ROOT).as_posix(): Document(p.read_text())
            for p in sorted(ROOT.rglob('*.html')) if '.git' not in p.parts and not p.name.startswith('google')}


def canonical_path(url):
    if not url.startswith(BASE):
        return None
    path = unquote(urlsplit(url).path[len(urlsplit(BASE).path):])
    return path + 'index.html' if not path or path.endswith('/') else path


def local_target(path, href):
    url = urljoin(BASE + path, href)
    return canonical_path(url), unquote(urlsplit(url).fragment)


def is_redirect(doc):
    return any(n.attrs.get('http-equiv', '').lower() == 'refresh' for n in doc.all('meta'))

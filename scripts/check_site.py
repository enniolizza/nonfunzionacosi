#!/usr/bin/env python3
"""Offline content, security and link regression checks; Python standard library only."""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.main_text = []
        self.in_main = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        if tag == 'main':
            self.in_main = True

    def handle_endtag(self, tag):
        if tag == 'main':
            self.in_main = False

    def handle_data(self, data):
        if self.in_main:
            self.main_text.append(data)

    @property
    def digest(self):
        text = ' '.join(''.join(self.main_text).split())
        return sha256(text.encode()).hexdigest()

    @property
    def sources(self):
        return [a['href'] for t, a in self.tags
                if t == 'a' and a.get('href', '').startswith('https://')]


def check_site(root=ROOT):
    failures = []
    paths = sorted(root.rglob('*.html'))
    pages = {p.resolve(): Page(p.read_text(encoding='utf-8')) for p in paths}

    def require(condition, path, message):
        if not condition:
            failures.append(f'{path.relative_to(root)}: {message}')

    def local_target(path, value):
        url = urlsplit(value)
        if url.scheme or url.netloc:
            return None, url.fragment
        target = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
        if target.is_dir():
            target /= 'index.html'
        return target, unquote(url.fragment)

    def check_link(path, value):
        target, fragment = local_target(path, value)
        if target is None:
            return
        require(target.is_relative_to(root.resolve()), path, f'link escapes site: {value}')
        require(target.is_file(), path, f'missing resource: {value}')
        if fragment and target in pages:
            ids = {a.get('id') for _, a in pages[target].tags}
            require(fragment in ids, path, f'missing anchor: {value}')

    for path in paths:
        text = path.read_text(encoding='utf-8')
        page = pages[path.resolve()]
        policies = [a.get('content', '') for t, a in page.tags if t == 'meta'
                    and a.get('http-equiv', '').lower() == 'content-security-policy']
        require(len(policies) == 1, path, 'exactly one CSP required')
        if policies:
            parts = [part.split() for part in policies[0].split(';') if part.strip()]
            directives = {part[0]: part[1:] for part in parts}
            require(len(directives) == len(parts), path, 'duplicate CSP directive')
            for directive in ['default-src', 'object-src', 'base-uri', 'form-action',
                              'connect-src', 'frame-src', 'script-src-attr', 'style-src-attr']:
                require(directives.get(directive) == ["'none'"], path, f'{directive} must block by default')
            require(directives.get('script-src') == ["'self'"], path, 'scripts must be local')
            require(directives.get('style-src') == ["'self'"], path, 'styles must be local')
            require(directives.get('font-src') == ["'self'"], path, 'font-src must be self only')
            require(not any(x in policies[0] for x in ['unsafe-inline', 'unsafe-eval', '*', 'data:']),
                    path, 'unsafe CSP source')
            require('frame-ancestors' not in directives, path, 'frame-ancestors is ignored in meta CSP')
        require(bool(re.search(r'<html\s+lang="it"', text)), path, 'Italian language declaration missing')
        require(not any(code.strip() for code in re.findall(r'<script\b[^>]*>(.*?)</script>', text, re.I | re.S)), path, 'inline JavaScript forbidden')
        ids = [a['id'] for _, a in page.tags if 'id' in a]
        require(len(ids) == len(set(ids)), path, 'duplicate IDs')
        if path.name != 'index.html':
            require('main-content' in ids, path, 'skip-link target missing')
        for tag, attrs in page.tags:
            require(tag not in ['style', 'iframe', 'object', 'embed', 'base', 'form'], path,
                    f'unsupported active tag: {tag}')
            require(not any(k.startswith('on') or k == 'style' for k in attrs), path,
                    f'inline handler/style on {tag}')
            if tag == 'a':
                href = attrs.get('href', '')
                require(href != '#', path, 'placeholder link')
                require(urlsplit(href).scheme in ['', 'https', 'mailto', 'tel'], path, f'unsafe link scheme: {href}')
                if attrs.get('target') == '_blank':
                    require({'noopener', 'noreferrer'} <= set(attrs.get('rel', '').split()), path,
                            'external tab lacks rel protection')
                check_link(path, href)
            for key in ['src', 'poster']:
                if key in attrs:
                    require(not urlsplit(attrs[key]).scheme and not attrs[key].startswith('//'), path,
                            f'external resource: {attrs[key]}')
                    check_link(path, attrs[key])
            if tag == 'link' and 'stylesheet' in attrs.get('rel', '').split():
                href = attrs.get('href', '')
                require(not urlsplit(href).scheme and not href.startswith('//'), path, 'external stylesheet')
                check_link(path, href)
            if tag == 'link' and (attrs.get('as') == 'font' or
                                  set(attrs.get('rel', '').split()) & {'preload', 'prefetch', 'preconnect', 'dns-prefetch'}):
                href = attrs.get('href', '')
                require(not urlsplit(href).scheme and not href.startswith('//'), path,
                        'external font or resource hint forbidden')
                check_link(path, href)
            if tag == 'img':
                require('alt' in attrs, path, 'image missing alt')
        # Policies must precede any active resources.
        resource_positions = [m.start() for m in re.finditer(r'<(?:link|script|style)\b', text)]
        if resource_positions:
            require(text.find('Content-Security-Policy') < min(resource_positions), path, 'late CSP')

    font_faces = set()
    font_urls = set()
    for path in sorted((root / 'assets/css').glob('*.css')):
        css = path.read_text()
        require('@import' not in css.casefold(), path, 'CSS imports forbidden')
        for _, url in re.findall(r'url\(\s*([\'\"]?)([^)\'\"]+?)\1\s*\)', css, re.I):
            require(not urlsplit(url).scheme and not url.startswith('//'), path, 'external CSS resource')
            check_link(path, url)
        for body in re.findall(r'@font-face\s*\{([^}]+)\}', css, re.I):
            props = dict(re.findall(r'([\w-]+)\s*:\s*([^;]+)', body))
            require(props.get('font-display') == 'swap', path, 'fonts must use font-display: swap')
            source = re.fullmatch(r"url\(['\"]?(\.\./fonts/[\w-]+\.woff2)['\"]?\) format\(['\"]woff2['\"]\)", props.get('src', ''))
            require(source is not None, path, 'font source must be a local WOFF2 in assets/fonts')
            if source:
                font_urls.add((path.parent / source[1]).resolve())
            font_faces.add((props.get('font-family', '').strip("'\""),
                            props.get('font-style'), props.get('font-weight')))

    expected_faces = {('Cinzel', 'normal', weight) for weight in ['500', '700']}
    expected_faces |= {('Inter', 'normal', weight) for weight in ['400', '500', '600', '700']}
    expected_faces |= {('Playfair Display', 'normal', weight) for weight in ['400', '700']}
    expected_faces.add(('Playfair Display', 'italic', '400'))
    font_root = root / 'assets/fonts'
    manifest_path = font_root / 'sources.json'
    manifest = json.loads(manifest_path.read_text())
    require(font_faces == expected_faces, manifest_path, 'required font families, styles or weights changed')
    expected_files = {(font_root / entry['path']).resolve() for entry in manifest['fonts']}
    require(font_urls == expected_files, manifest_path, 'CSS fonts differ from provenance manifest')
    require({p.resolve() for p in font_root.glob('*.woff2')} == expected_files,
            manifest_path, 'unlisted or missing WOFF2 file')
    for entry in manifest['fonts'] + manifest['licenses']:
        path = font_root / entry['path']
        require(path.is_file(), path, 'missing font or license')
        if not path.is_file():
            continue
        data = path.read_bytes()
        require(sha256(data).hexdigest() == entry['sha256'], path, 'font/license fingerprint changed')
        if path.suffix == '.woff2':
            require(data[:4] == b'wOF2' and int.from_bytes(data[8:12], 'big') == len(data),
                    path, 'invalid WOFF2 header or length')
            require(len(data) == entry['bytes'], path, 'font size differs from provenance manifest')
        else:
            require(b'SIL OPEN FONT LICENSE Version 1.1' in data, path, 'OFL license missing')
    require({entry['family'] for entry in manifest['licenses']} == {'Cinzel', 'Inter', 'Playfair Display'},
            manifest_path, 'a font family is missing its license')

    baseline = json.loads((root / 'tests/content-baseline.json').read_text())
    for rel, expected in baseline['pages'].items():
        path = root / rel
        if path.resolve() not in pages:
            require(False, path, 'protected page deleted')
            continue
        actual = pages[path.resolve()]
        require(actual.digest == expected['main_sha256'], path, 'editorial main text changed')
        require(actual.sources == expected['sources'], path, 'source/social link changed')
    return failures, len(paths)


if __name__ == '__main__':
    errors, count = check_site()
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)
    print(f'OK: {count} pages; content fingerprints, CSP, local fonts/licenses, assets and internal links verified.')

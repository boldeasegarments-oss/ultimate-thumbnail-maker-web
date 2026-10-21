import os
import re
import json
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CANONICAL_DOMAIN = "https://ultimatethumbnailmaker.pages.dev"
PLAY_STORE_URL = "https://play.google.com/store/apps/details?id=com.sk.thumbnailmaker"

html_files = []
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.relpath(os.path.join(root, f), BASE_DIR))

print(f"Discovered {len(html_files)} HTML files for audit: {html_files}")

errors = []
warnings = []
passed = []

titles = {}
descriptions = {}
canonicals = {}

for rel_path in html_files:
    full_path = os.path.join(BASE_DIR, rel_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Doctype & lang
    if '<!DOCTYPE html>' not in content:
        errors.append(f"[{rel_path}] Missing <!DOCTYPE html>")
    if '<html lang="en">' not in content:
        errors.append(f"[{rel_path}] Missing <html lang=\"en\">")

    # 2. Title tag
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    if not title_match:
        errors.append(f"[{rel_path}] Missing <title> tag")
    else:
        title = title_match.group(1).strip()
        if title in titles:
            errors.append(f"[{rel_path}] Duplicate title tag with [{titles[title]}]: '{title}'")
        else:
            titles[title] = rel_path
            passed.append(f"[{rel_path}] Title: '{title}' ({len(title)} chars)")

    # 3. Meta description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
    if not desc_match:
        errors.append(f"[{rel_path}] Missing meta description")
    else:
        desc = desc_match.group(1).strip()
        if desc in descriptions:
            errors.append(f"[{rel_path}] Duplicate meta description with [{descriptions[desc]}]: '{desc}'")
        else:
            descriptions[desc] = rel_path
            passed.append(f"[{rel_path}] Meta Description: {len(desc)} chars")

    # 4. Canonical link (except 404.html)
    if rel_path != '404.html':
        canon_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', content, re.IGNORECASE)
        if not canon_match:
            errors.append(f"[{rel_path}] Missing canonical link")
        else:
            canon = canon_match.group(1).strip()
            if not canon.startswith(CANONICAL_DOMAIN):
                errors.append(f"[{rel_path}] Canonical URL does not match canonical domain: {canon}")
            if canon in canonicals:
                errors.append(f"[{rel_path}] Duplicate canonical URL with [{canonicals[canon]}]: {canon}")
            else:
                canonicals[canon] = rel_path

    # 5. Single H1 tag
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    if len(h1_matches) != 1:
        errors.append(f"[{rel_path}] Expected exactly 1 <h1> tag, found {len(h1_matches)}")
    else:
        passed.append(f"[{rel_path}] <h1> verified: '{h1_matches[0].strip()}'")

    # 6. Noindex check
    if 'noindex' in content.lower():
        if rel_path == '404.html':
            passed.append(f"[{rel_path}] Intentionally has noindex (correct for 404 page)")
        else:
            errors.append(f"[{rel_path}] Unexpected noindex directive found!")

    # 7. Check images have alt, width, height
    img_tags = re.findall(r'<img\s+([^>]+)>', content, re.IGNORECASE)
    for tag in img_tags:
        if 'alt=' not in tag:
            errors.append(f"[{rel_path}] <img> tag missing alt attribute: {tag}")
        if 'width=' not in tag or 'height=' not in tag:
            warnings.append(f"[{rel_path}] <img> tag missing width/height attributes: {tag}")

    # 8. Check internal links resolve to files
    hrefs = re.findall(r'href=["\'](.*?)["\']', content, re.IGNORECASE)
    for href in hrefs:
        if href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
            continue
        if href.startswith('http://') or href.startswith('https://'):
            if 'play.google.com' in href:
                if href != PLAY_STORE_URL:
                    errors.append(f"[{rel_path}] Incorrect Google Play URL: {href}")
            continue
        
        # Internal link check
        clean_href = href.split('?')[0].split('#')[0]
        if clean_href.startswith('/'):
            target_rel = clean_href.lstrip('/')
        else:
            target_rel = os.path.normpath(os.path.join(os.path.dirname(rel_path), clean_href))
        
        # Check target
        if target_rel == '':
            target_file = os.path.join(BASE_DIR, 'index.html')
        elif os.path.isdir(os.path.join(BASE_DIR, target_rel)):
            target_file = os.path.join(BASE_DIR, target_rel, 'index.html')
        else:
            target_file = os.path.join(BASE_DIR, target_rel)
            
        if not os.path.exists(target_file):
            errors.append(f"[{rel_path}] Broken internal link: '{href}' resolves to non-existent '{target_file}'")

    # 9. JSON-LD structured data verification
    json_ld_blocks = re.findall(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
    for block in json_ld_blocks:
        try:
            parsed = json.loads(block)
            passed.append(f"[{rel_path}] Valid JSON-LD schema of type: {parsed.get('@type', 'Unknown')}")
        except json.JSONDecodeError as e:
            errors.append(f"[{rel_path}] Invalid JSON-LD structured data: {e}")

# Check placeholder occurrences across all project files
placeholder_targets = ['.html', '.xml', '.txt', '.js', '.css', '.md']
found_placeholders = []
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if any(f.endswith(ext) for ext in placeholder_targets):
            fpath = os.path.join(root, f)
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
                file_text = fp.read()
                # Check for YOUR_DOMAIN in non-README / non-blueprint files
                if 'YOUR_DOMAIN' in file_text and not f.endswith('blueprint.md') and not f.endswith('README.md') and not f.endswith('run_audit.py'):
                    found_placeholders.append(os.path.relpath(fpath, BASE_DIR))

if found_placeholders:
    errors.append(f"Unreplaced 'YOUR_DOMAIN' placeholders found in production files: {found_placeholders}")
else:
    passed.append("No unreplaced 'YOUR_DOMAIN' placeholders found in production files.")

# Check Sitemap
sitemap_path = os.path.join(BASE_DIR, 'sitemap.xml')
if not os.path.exists(sitemap_path):
    errors.append("sitemap.xml is missing")
else:
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        sitemap_urls = [elem.text.strip() for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        passed.append(f"sitemap.xml verified with {len(sitemap_urls)} URLs: {sitemap_urls}")
        # Verify every URL matches an existing canonical
        for surl in sitemap_urls:
            if surl not in canonicals:
                errors.append(f"sitemap.xml references URL not in canonical pages: {surl}")
    except Exception as e:
        errors.append(f"sitemap.xml parse error: {e}")

# Check robots.txt
robots_path = os.path.join(BASE_DIR, 'robots.txt')
if not os.path.exists(robots_path):
    errors.append("robots.txt is missing")
else:
    with open(robots_path, 'r', encoding='utf-8') as f:
        robots_content = f.read()
    if f"Sitemap: {CANONICAL_DOMAIN}/sitemap.xml" not in robots_content:
        errors.append(f"robots.txt missing or incorrect Sitemap directive: {CANONICAL_DOMAIN}/sitemap.xml")
    if "User-agent: OAI-SearchBot" not in robots_content:
        warnings.append("robots.txt does not explicitly configure OAI-SearchBot")
    passed.append("robots.txt verified.")

# Check _headers
headers_path = os.path.join(BASE_DIR, '_headers')
if not os.path.exists(headers_path):
    errors.append("_headers is missing")
else:
    passed.append("_headers verified.")

print("\n" + "="*50)
print(f"AUDIT SUMMARY: {len(passed)} checks passed, {len(warnings)} warnings, {len(errors)} errors")
print("="*50)

if warnings:
    print("\nWARNINGS:")
    for w in warnings:
        print(f"  [!] {w}")

if errors:
    print("\nERRORS:")
    for e in errors:
        print(f"  [X] {e}")
else:
    print("\nALL VERIFICATION CHECKS PASSED PERFECTLY!")

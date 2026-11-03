"""Makes a demo copy of site/ in _build/demo-dist for Cloudflare (a static-assets Worker): no Google Tag Manager (so demo clicks never reach
Khat's Google Ads conversions) and noindex on every page (so the demo stays out of search).
Deploy: python3 demo.py && npx wrangler deploy --config demo-wrangler.jsonc"""
import os, re, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
SITE, OUT = os.path.join(HERE, '..', 'site'), os.path.join(HERE, 'demo-dist')
shutil.rmtree(OUT, ignore_errors=True)
shutil.copytree(SITE, OUT, ignore=shutil.ignore_patterns('.DS_Store'))
for root, _, files in os.walk(OUT):
    for f in files:
        if not f.endswith('.html'): continue
        p = os.path.join(root, f); s = open(p).read()
        s = re.sub(r'<link rel="preconnect" href="https://www.googletagmanager.com">\n?', '', s)
        s = re.sub(r'<!-- Google Tag Manager.*?</script>\n?', '', s, flags=re.S)
        s = re.sub(r'<noscript><iframe src="https://www.googletagmanager.com/ns.html[^<]*</iframe></noscript>\n?', '', s)
        s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 1)
        assert 'googletagmanager' not in s and 'GTM-' not in s, p
        open(p, 'w').write(s)
open(os.path.join(OUT, '_headers'), 'w').write('/*\n  X-Robots-Tag: noindex, nofollow\n\n/assets/*\n  Cache-Control: public, max-age=86400\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nDisallow: /\n')
print('demo-dist ready:', sum(len(f) for _, _, f in os.walk(OUT)), 'files')

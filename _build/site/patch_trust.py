"""Rating boxes and matched buttons, applied to the three page sources (category template, homepage, yacht)."""
import re

TRUST_CSS = """/* review ratings: two equal boxes, each with the platform's mark, name, score and count */
.trust { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; max-width: 480px; }
.rate-box { position: relative; display: grid; grid-template-columns: 36px minmax(0, 1fr); column-gap: 12px; align-items: center; padding: 10px 14px 10px 16px; background: var(--paper); border: 1px solid var(--line); border-radius: 14px; box-shadow: var(--shadow); text-decoration: none; color: var(--ink); }
.rate-box::before { content: ""; position: absolute; left: -1px; top: 12px; bottom: 12px; width: 4px; border-radius: 0 4px 4px 0; background: var(--c); }
.rate-box:hover { border-color: var(--ink); }
.rate-box img { grid-row: 1 / span 3; width: 36px; height: 36px; }
.rate-box .nm { font-weight: 800; font-size: 15px; line-height: 1.2; }
.rate-box .sc { display: flex; align-items: center; gap: 6px; font-weight: 800; font-size: 15px; line-height: 1.3; }
.rate-box small { color: var(--ink-2); font-size: 13px; text-decoration: underline; text-underline-offset: 3px; }
.trust .flag { grid-column: 1 / -1; display: inline-flex; align-items: center; gap: 6px; color: var(--ok); font-weight: 700; font-size: 15px; }
.trust .flag svg { width: 18px; height: 18px; }
@media (max-width: 420px) {
  .rate-box { grid-template-columns: 28px minmax(0, 1fr); column-gap: 10px; padding: 9px 10px 9px 13px; }
  .rate-box img { width: 28px; height: 28px; }
  .rate-box .nm, .rate-box .sc { font-size: 14px; }
  .rate-box .bubbles i { width: 10px; height: 10px; }
  .rate-box .stars svg { width: 12px; height: 12px; }
}
"""

TRUST_JS = """  $('trust').innerHTML =
    '<a class="rate-box" style="--c: var(--ta)" href="' + R.tripadvisor.url + '" target="_blank" rel="noopener"><img src="/assets/img/logos/tripadvisor-mark.svg" alt="" width="36" height="36"><span class="nm">Tripadvisor</span><span class="sc">' + R.tripadvisor.score.toFixed(1) + bubbles(5) + '</span><small>' + fmt.format(R.tripadvisor.count) + ' reviews</small></a>' +
    '<a class="rate-box" style="--c: var(--g-star)" href="' + R.google.url + '" target="_blank" rel="noopener"><img src="/assets/img/logos/google-g.png" alt="" width="36" height="36"><span class="nm">Google</span><span class="sc">' + R.google.score.toFixed(1) + stars(5) + '</span><small>' + fmt.format(R.google.count) + ' reviews</small></a>'"""

FLAG = """ +
    '<span class="flag"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12 4 4 10-10"/></svg>Free cancellation</span>'"""

# two buttons side by side share one width; on phones they stack at full width
PAIR_CSS = """
/* paired buttons: the same width side by side, full width and stacked on phones */
.ctas, .final .acts { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; max-width: 480px; }
.ctas .btn, .final .acts .btn { padding-inline: 14px; }
@media (max-width: 560px) { .ctas, .final .acts { grid-template-columns: minmax(0, 1fr); max-width: none; width: 100%; } }
"""


def strip_trust_css(t):
    return re.sub(r'\n\.trust[^\n]*', '', t)


def patch_template(p):
    t = open(p).read()
    if 'rate-box' in t: return 'template: already done'
    t = strip_trust_css(t)
    t = t.replace('/* gallery */', TRUST_CSS + '\n/* gallery */', 1)
    i = t.index("  $('trust').innerHTML ="); j = t.index("';", t.index('Free cancellation</span>', i)) + 2
    t = t[:i] + TRUST_JS + FLAG + ';' + t[j:]
    t = t.replace('.trust {', '.trust { margin-bottom: 4px;', 0)
    open(p, 'w').write(t); return 'template: patched'


def patch_home(p):
    t = open(p).read()
    if 'rate-box' in t: return 'home: already done'
    t = strip_trust_css(t)
    t = t.replace('.collage {', TRUST_CSS + '\n.collage {', 1)
    i = t.index("  $('trust').innerHTML ="); j = t.index("reviews</u></a>';", i) + len("reviews</u></a>';")
    t = t[:i] + TRUST_JS + ';' + t[j:]
    t = t.replace('.hero .ctas { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 24px; }', '.hero .ctas { margin-bottom: 22px; }')
    t = t.replace('.final .acts { display: flex; flex-wrap: wrap; gap: 12px; }', '')
    t = t.replace('/* promises */', PAIR_CSS + '\n/* promises */', 1)
    open(p, 'w').write(t); return 'home: patched'


def patch_yacht(p):
    t = open(p).read()
    if 'rate-box' in t: return 'yacht: already done'
    css = TRUST_CSS + """.bubbles { display: inline-flex; gap: 3px; }
.bubbles i { width: 13px; height: 13px; border-radius: 50%; background: var(--ta); }
.stars { display: inline-flex; gap: 1px; }
.stars svg { width: 15px; height: 15px; fill: var(--g-star); }
.hero-copy .trust { margin-top: 18px; }
"""
    t = t.replace('  --wa-dk:', '  --ta: #00aa6c;\n  --g-star: #fbbc04;\n  --wa-dk:', 1)
    t = t.replace('/* the chart */', css + '\n/* the chart */', 1)
    star = '<svg viewBox="0 0 20 20"><path d="M10 1.5l2.6 5.6 6.1.7-4.5 4.2 1.2 6-5.4-3.1-5.4 3.1 1.2-6L1.3 7.8l6.1-.7z"/></svg>'
    boxes = ('\n        <div class="trust">'
             '<a class="rate-box" style="--c: var(--ta)" href="https://www.tripadvisor.com/Attraction_Review-g295424-d10898020-Reviews-Khat_Tours_and_Safaris-Dubai_Emirate_of_Dubai.html" target="_blank" rel="noopener"><img src="/assets/img/logos/tripadvisor-mark.svg" alt="" width="36" height="36"><span class="nm">Tripadvisor</span><span class="sc">5.0<span class="bubbles" aria-hidden="true">' + '<i></i>' * 5 + '</span></span><small>1,396 reviews</small></a>'
             '<a class="rate-box" style="--c: var(--g-star)" href="https://maps.google.com/?cid=10514996801509726899" target="_blank" rel="noopener"><img src="/assets/img/logos/google-g.png" alt="" width="36" height="36"><span class="nm">Google</span><span class="sc">5.0<span class="stars" aria-hidden="true">' + star * 5 + '</span></span><small>113 reviews</small></a>'
             '</div>')
    a = 'and the map shows where you\'ll go.</p>'
    assert a in t; t = t.replace(a, a + boxes, 1)
    t = t.replace('.final .acts { display: flex; flex-wrap: wrap; gap: 12px; }', '')
    t = t.replace('/* mobile dock:', PAIR_CSS + '\n/* mobile dock:', 1)
    open(p, 'w').write(t); return 'yacht: patched'


if __name__ == '__main__':
    import os
    H = os.path.dirname(os.path.abspath(__file__))
    print(patch_template(os.path.join(H, 'template.html')))
    print(patch_home(os.path.join(H, 'home_source.html')))
    print(patch_yacht(os.path.join(H, '..', 'yacht', 'template.html')))

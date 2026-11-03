"""Smooth FAQ open/close on every page, and plain rating boxes and review panels without coloured edge strips."""
import re, os

FAQ_JS = """<script>
/* FAQ: open and close with a short height-and-fade animation instead of a jump */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var EASE = 'cubic-bezier(.2, .7, .2, 1)', MS = 320;
  document.querySelectorAll('.faq details').forEach(function (d) {
    var s = d.querySelector('summary'), body = s.nextElementSibling, run = null;
    if (d.open) d.classList.add('is-open');
    s.addEventListener('click', function (e) {
      e.preventDefault();
      var opening = !d.classList.contains('is-open');
      d.classList.toggle('is-open', opening);
      if (reduce || !d.animate) { d.open = opening; return; }
      var from = d.offsetHeight;
      if (run) run.cancel();
      if (opening) d.open = true;
      var to = opening ? d.offsetHeight : s.offsetHeight + (d.offsetHeight - d.clientHeight);
      d.style.overflow = 'hidden';
      run = d.animate({ height: [from + 'px', to + 'px'] }, { duration: MS, easing: EASE });
      if (body) body.animate({ opacity: opening ? [0, 1] : [1, 0], transform: opening ? ['translateY(-6px)', 'none'] : ['none', 'translateY(-6px)'] }, { duration: MS, easing: EASE, fill: 'forwards' });
      run.onfinish = function () {
        if (!opening) d.open = false;
        d.style.overflow = ''; run = null;
        if (body) body.getAnimations().forEach(function (a) { a.cancel(); });
      };
    });
  });
})();
</script>
"""


def patch(p):
    t = open(p).read()
    # rating boxes: no coloured side strip
    t = re.sub(r'\n\.rate-box::before[^\n]*', '', t)
    t = t.replace('padding: 10px 14px 10px 16px;', 'padding: 10px 14px;').replace('padding: 9px 10px 9px 13px;', 'padding: 9px 10px;')
    # review panels: no coloured top strip either
    t = re.sub(r'\n\.plat\.(?:ta|g) \{ border-top: 4px solid [^}]*\}', '', t)
    # FAQ: the arrow follows the is-open class, which flips the moment the question is tapped
    t = t.replace('.faq details[open] summary::after { transform: rotate(225deg) translateY(-3px); }',
                  '.faq details.is-open summary::after { transform: rotate(225deg) translateY(-3px); }\n'
                  '.faq summary::after { transition: transform .32s cubic-bezier(.2, .7, .2, 1); }\n'
                  '.faq summary:hover { color: var(--red); }\n'
                  '@media (prefers-reduced-motion: reduce) { .faq summary::after { transition: none; } }')
    if 'FAQ: open and close' not in t:
        assert t.count('</body>') == 1
        t = t.replace('</body>', FAQ_JS + '</body>')
    open(p, 'w').write(t)
    return p.split('/_build/')[1], 'rate-box::before' in t, '.plat.ta {' in t, t.count('is-open')


H = os.path.dirname(os.path.abspath(__file__))
for f in [os.path.join(H, 'template.html'), os.path.join(H, 'home_source.html'), os.path.join(H, '..', 'yacht', 'template.html')]:
    print(patch(os.path.normpath(f)))

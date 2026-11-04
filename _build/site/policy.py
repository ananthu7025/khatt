"""Builds site/cancellation-policy/index.html with the shared header, footer and styles.
The terms are Khat's own, from the cancellation policy on their current site."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(HERE, '..', '..', 'site'))
header = re.sub(r'\{\{CUR_[a-z-]+\}\}', '', open(os.path.join(HERE, 'partials', 'header.html'), encoding='utf-8').read()).strip()
footer = open(os.path.join(HERE, 'partials', 'footer.html'), encoding='utf-8').read().strip()
home = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()
style = home[home.index('<style>'):home.index('</style>') + len('</style>')]
sprite = home[home.index('<svg width="0" height="0"'):home.index('</svg>', home.index('<svg width="0" height="0"')) + 6]
head_links = '\n'.join(l for l in home.split('\n') if l.startswith(('<link rel="icon"', '<link rel="apple-touch-icon"', '<link rel="preload" href="/assets/fonts')))
gtm = home[home.index('<!-- Google Tag Manager'):home.index('</script>', home.index('<!-- Google Tag Manager')) + 9]

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Cancellation and Refund Policy | Khat Tourism</title>
<meta name="description" content="Khat Tourism's cancellation and refund policy for private desert safaris, yacht charters and tours in Dubai and Abu Dhabi.">
<link rel="canonical" href="https://khattourism.com/cancellation-policy/">
<meta name="theme-color" content="#0d2436">
{head_links}
{gtm}
{style}
<style>
.policy {{ max-width: 760px; padding-block: 40px 72px; }}
.policy h1 {{ font: 800 clamp(30px, 4vw, 44px)/1.08 var(--display); letter-spacing: -.025em; margin: 0 0 12px; }}
.policy .lede {{ color: var(--ink-2); font-size: 18px; margin: 0 0 32px; }}
.policy h2 {{ font: 700 22px/1.2 var(--display); margin: 32px 0 10px; }}
.policy table {{ width: 100%; border-collapse: collapse; margin: 8px 0; }}
.policy th, .policy td {{ text-align: left; padding: 12px 14px; border-bottom: 1px solid var(--line); vertical-align: top; }}
.policy th {{ background: var(--foam); font-weight: 700; }}
.policy p, .policy li {{ color: var(--ink-2); }}
.policy .ask {{ margin-top: 36px; padding: 20px; border-radius: var(--r); background: var(--sand); display: flex; flex-wrap: wrap; gap: 14px; align-items: center; justify-content: space-between; }}
.policy .ask p {{ margin: 0; color: var(--ink); font-weight: 600; }}
</style>
</head>
<body>
{header}

<main class="wrap policy">
  <h1>Cancellation and refund policy</h1>
  <p class="lede">Plans change. Here is how cancelling works, and what happens if the weather stops your trip.</p>

  <h2>Private tours, desert camps and yacht charters</h2>
  <p>Cancel at least 48 hours before pickup or departure for a full refund.</p>

  <h2>Desert safaris and city tours</h2>
  <table>
    <thead><tr><th scope="col">When you cancel</th><th scope="col">Refund</th></tr></thead>
    <tbody>
      <tr><td>More than 24 hours before pickup</td><td>Full refund</td></tr>
      <tr><td>12 to 24 hours before pickup</td><td>50% refund</td></tr>
      <tr><td>Less than 12 hours before pickup, or a no-show</td><td>No refund</td></tr>
    </tbody>
  </table>

  <h2>Bad weather</h2>
  <p>If a severe sandstorm, heavy rain or a government weather warning stops your trip, you choose: move it to another date for free, or get a full refund.</p>

  <h2>How refunds are paid</h2>
  <p>Approved refunds go back the way you paid (card, bank transfer or cash) within 3 to 5 working days.</p>

  <div class="ask">
    <p>Need to change or cancel a booking?</p>
    <a class="btn btn-wa" href="https://chat.whatsapp.com/DOW0NrXtuJpAb0G1cILkYL?s=cl&p=i&mlu=4&ilr=4&iam=2" data-wa="policy" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><use href="#i-wa"/></svg>Message us on WhatsApp</a>
  </div>
</main>

{footer}

{sprite}
<script>
document.addEventListener('click', function (e) {{
  var a = e.target.closest('a[data-wa], a[data-track]');
  if (!a) return;
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push(a.hasAttribute('data-wa') ? {{ event: 'whatsapp_lead', lead_source: 'cancellation-policy', cta: a.dataset.wa }} : {{ event: 'call_click', lead_source: 'cancellation-policy' }});
}});
</script>
</body>
</html>
'''
os.makedirs(os.path.join(SITE, 'cancellation-policy'), exist_ok=True)
open(os.path.join(SITE, 'cancellation-policy', 'index.html'), 'w', encoding='utf-8').write(page)
print('cancellation-policy', len(page), 'bytes; khattourism hrefs:', sorted(set(re.findall(r'href="(https://khattourism\.com[^"]*)"', page))))

import json,sys,html
S,P=sys.argv[1],sys.argv[2]
t=open(S+'/template.html').read()
faq=[
 ("How many hours should I book?","One hour covers Dubai Marina, JBR and Ain Dubai. Two hours adds the Palm and Atlantis, and three reaches Burj Al Arab. Book four if you also want a long swim stop."),
 ("Is the price per person?","No. The hourly price is for the whole boat with captain and crew, up to the boat's guest limit."),
 ("Where do we board?","At Dubai Marina or Dubai Harbour, depending on the boat. We send the exact pier and a map pin on WhatsApp after you book."),
 ("Does every guest need ID?","Yes. UAE Coast Guard rules say everyone on board must carry an original passport or Emirates ID."),
 ("Can we bring food, drinks and music?","Yes. Bring your own snacks, food and drinks, and connect your phone to the boat's Bluetooth speakers. We can also arrange catering if you ask when you book."),
 ("Is it safe for children?","Yes. The boat carries life jackets for adults and children, life rings and a first-aid kit, and the captain is licensed."),
 ("Can you pick us up from our hotel?","Yes. Private hotel transfers are available for an extra fee. Ask for one in your WhatsApp message."),
 ("What if the weather is bad?","Boats can't leave when the Coast Guard closes the sea. If that happens, you can move your charter to another day or get a full refund. See our cancellation policy."),
 ("Can we cancel?","Yes. Cancel at least 48 hours before your charter for a full refund."),
]
link='<a href="/cancellation-policy/">cancellation policy</a>'
items=[]
for q,a in faq:
    ah=html.escape(a).replace('cancellation policy',link)
    items.append(f'<details><summary>{html.escape(q)}</summary><p>{ah}</p></details>')
ld={"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
wa=open(S+'/wa_icon.svg').read().strip()
chart=open(S+'/chart.svg.html').read()
import re as _re, os as _os
SP=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'..','site','partials')
head=_re.sub(r'\{\{CUR_([a-z-]+)\}\}', lambda m: ' aria-current="page"' if m.group(1)=='yacht-rental-dubai' else '', open(_os.path.join(SP,'header.html')).read())
t=t.replace('{{HEADER}}',head.strip()).replace('{{FOOTER}}',open(_os.path.join(SP,'footer.html')).read().strip())
t=t.replace('{{CHART}}',chart).replace('{{WA_ICON}}',wa).replace('{{FAQ_HTML}}','\n        '.join(items)).replace('{{FAQ_LD}}',json.dumps(ld,indent=2).replace('\n','\n    '))
# the icon template must exist before the script that reads it
tpl='<template id="wa-icon-src">'+wa+'</template>\n'
t=t.replace(tpl,'').replace('<script>\n(function () {',tpl+'<script>\n(function () {',1)
assert '{{' not in t, [l for l in t.splitlines() if '{{' in l][:3]
open(P+'/index.html','w').write(t); print(len(t),'bytes')

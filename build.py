"""Builds the Heat Fitness site.
dist/     ready to deploy (Netlify, Vercel or any static host)
preview/  the same site, shaped for a Claude artifact preview
Edit the page content below, then run: python3 build.py
"""
import os, shutil, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import group_pages as GP

TBC = lambda s="to confirm": f'<span class="tbc">{s}</span>'
PHONE = "07718 339510"; STUDIO = "01786 473694"
PHONE_A = f'<a href="tel:07718339510">{PHONE}</a>'
# Six-week cycles. Change these when Helen confirms dates.
CYCLE_NOW = "the week of 16 November"
CYCLE_NEXT = "January 2027"
ADDR = "Unit 22, 15 Borrowmeadow Road, Stirling"
POSTCODE = "FK7 7FB"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Caveat:wght@600;700&display=swap">')
UNDERLINE = ('<svg class="underline" viewBox="0 0 100 8" preserveAspectRatio="none" aria-hidden="true"><path d="M2 5.5 C 18 2.5, 30 7, 48 4.2 S 80 2.2, 98 4.8" '
             'fill="none" stroke="#F68A1D" stroke-width="3" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>')
HEAT_COL = {"unheated": "var(--cool)", "warm": "#F68A1D", "30": "#F6A24A", "38": "#C64B12", "40": "#970D0B", "tbc": "transparent"}

def temp(label, key):
    border = "border:1.5px dashed currentColor;" if key == "tbc" else ""
    return f'<span class="temp"><i style="background:{HEAT_COL[key]};{border}"></i>{label}</span>'

NAV = [("classes.html", "Classes"), ("one-to-one.html", "One-to-one"), ("timetable.html", "Timetable"), ("prices.html", "Prices"),
       ("start-here.html", "New here?"), ("meet-helen.html", "Meet Helen"), ("news.html", "News"), ("resources.html", "Free resources"), ("contact.html", "Contact")]

def header(cur):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{t}</a>' for h, t in NAV)
    six_cur = ' aria-current="page"' if (cur == "six-week-start.html" or GP.link_for_slug(cur)) else ""
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="wrap">
  <a class="brand" href="index.html" aria-label="Heat Fitness, home">
    <img class="logo-light" src="assets/img/logo_black.png" alt="Heat Fitness Stirling" width="54" height="48">
    <img class="logo-dark" src="assets/img/logo_white.png" alt="Heat Fitness Stirling" width="54" height="48">
  </a>
  <nav class="nav" aria-label="Main">{links}<a class="btn" href="six-week-start.html"{six_cur}>Six-week groups</a></nav>
  <details class="menu"><summary>Menu</summary><nav class="menu-panel" aria-label="Main">{links}<a class="btn" href="six-week-start.html"{six_cur}>Six-week groups</a></nav></details>
</div></header>'''

FOOTER = f'''<footer class="site-foot"><div class="wrap">
  <div class="foot-grid">
    <div><h2>Find us</h2><p>{ADDR}<br>{POSTCODE}</p><p style="margin-top:8px">Opening hours {TBC()}</p></div>
    <div><h2>Talk to Helen</h2><ul><li>Text or call {PHONE_A}</li><li>Studio <a href="tel:01786473694">{STUDIO}</a></li><li><a href="mailto:helen@heatfitness.co.uk">helen@heatfitness.co.uk</a></li></ul></div>
    <div><h2>Pages</h2><ul><li><a href="classes.html">Classes</a></li><li><a href="timetable.html">Timetable</a></li><li><a href="prices.html">Prices</a></li><li><a href="start-here.html">New here?</a></li><li><a href="resources.html">Free resources</a></li></ul></div>
    <div><h2>Classes</h2><ul><li><a href="classes.html#hot">Hot yoga</a></li><li><a href="classes.html#warm">Warm and unheated yoga</a></li><li><a href="classes.html#strength">TRX and the gym</a></li><li><a href="one-to-one.html">Personal training</a></li><li><a href="classes.html#groups">Six-week groups</a></li></ul></div>
    <div><h2>Follow us</h2><ul><li><a href="https://www.facebook.com/HeatFitnessScotland">Facebook</a></li><li><a href="https://www.instagram.com/heatfitnessscotland">Instagram</a></li></ul></div>
  </div>
  <div class="foot-base"><span>&copy; <span id="year">2026</span> Heat Fitness, Stirling</span><a href="privacy.html">Privacy notice</a></div>
</div></footer>'''

JSONLD = '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"HealthClub","name":"Heat Fitness","url":"https://heatfitnessstirling.co.uk/",
"telephone":"+441786473694","email":"helen@heatfitness.co.uk","address":{"@type":"PostalAddress","streetAddress":"Unit 22, 15 Borrowmeadow Road","addressLocality":"Stirling","postalCode":"FK7 7FB","addressCountry":"GB"},
"sameAs":["https://www.facebook.com/HeatFitnessScotland","https://www.instagram.com/heatfitnessscotland"]}</script>'''

def page(fname, title, desc, body, extra_head=""):
    head = (f'<title>{title}</title><meta name="description" content="{desc}">'
            f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">'
            f'<meta property="og:image" content="https://heatfitnessstirling.co.uk/assets/img/studio-helen.jpg">'
            f'{FONTS}<link rel="stylesheet" href="assets/css/site.css">{extra_head}')
    inner = f'{header(fname)}<main id="main">{body}</main>{FOOTER}<script src="assets/js/site.js"></script>'
    full = (f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            f'<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png"><link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png"><link rel="manifest" href="site.webmanifest"><meta name="theme-color" content="#F68A1D">{head}</head><body>{inner}</body></html>')
    preview_index = '<title>Heat Fitness Website</title>' + f'{head}{inner}'.replace(f'<title>{title}</title>', '', 1)   # the artifact wraps index.html in its own skeleton
    return full, preview_index

FEATURED = [
  ("Strong and Calm", "Perimenopause", "Not sleeping? Not yourself?",
   "Gentle strength in the gym and slow, unheated yoga upstairs, built around energy that changes from week to week. When you arrive, tell Helen how you feel today: green for full of beans, amber for so-so, red for running on empty. She'll shape the session to match.",
   "unheated"),
  ("Strong Bones", "Menopause and after", "Strong enough for the next thirty years.",
   "Cool, unhurried strength for muscle and bones in the gym, plus yoga for balance upstairs. Daytime sessions during school hours, with a teacher who gets it.",
   "unheated"),
  ("The Unstiffening", "Stiff backs and desk bodies, every gender", "Your back called. It would like a word.",
   "Lunchtime strength basics downstairs and a deep stretch in the warm room upstairs. No chanting, no headstands, and time to shower before you head back to work.",
   "warm"),
  ("The Quiet Hour", "Anxiety, low mood or stress", "Calm, and the same every week.",
   "The same simple routine at the same times every week, so nothing comes as a surprise. Low lights in the studio, low music, nobody watching, and you can leave whenever you need to.",
   "unheated"),
  ("Steady and Strong", "Over-60s", "Daytime, no heat, and a cuppa after.",
   "Strength and balance in the gym with the wall to hold on to, and supported yoga upstairs. Tea and a chat afterwards is part of the class.",
   "unheated"),
]

def featured_cards():
    out = ""
    for name, forw, head, body, heat in FEATURED:
        t = temp("Unheated", "unheated") if heat == "unheated" else temp("Upstairs warm, about 28°C", "warm")
        out += f'''<article class="card"><span class="for">{forw}</span><h3><a href="{GP.link_for(name)}">{name}</a></h3>
<p class="hand" style="font-size:1.45rem">{head}</p><p>{body}</p>
<div class="meta"><span><b>Twice a week</b>, downstairs and upstairs</span>{t}<span>{GP.when(name)}, times {TBC()}</span></div>
<span data-places="{name}" hidden></span><a class="card-link" href="{GP.link_for(name)}">Find out more about {name}</a></article>'''
    out += f'''<article class="card running"><span class="for">Women over 40 · running now</span><h3>Women's Strength</h3>
<p class="hand" style="font-size:1.45rem">Strong through the change.</p><p>Our small women's-only strength group is already up and running, and some of the women have been coming for over two years. More weights than cardio, for women through perimenopause and menopause. Booked a month at a time, and there's usually space.</p>
<div class="meta"><span><b>Wednesdays and Fridays</b>, 6:30am</span>{temp("Unheated", "unheated")}<span><b>£15</b> a session</span></div>
<a class="card-link" href="contact.html">Message Helen to join</a></article>'''
    return out

SCALE = f'''<div class="scale">
  <div class="sec-head" style="margin-bottom:0"><span class="kicker">Hot when you want it</span><h2 class="display" style="font-size:clamp(1.5rem,3.4vw,2.2rem)">Not every class is hot</h2>
  <p class="measure">We're Stirling's only hot yoga studio, but plenty of our classes aren't heated at all. Most people start somewhere cool, and every class tells you its temperature before you book.</p></div>
  <div class="scale-bar" role="img" aria-label="Class temperatures from unheated up to 40 degrees">
    <span class="scale-dot" style="left:40%"></span><span class="scale-dot" style="left:74%"></span></div>
  <div class="scale-stops">
    <div class="scale-stop" style="left:0"><b>Unheated</b>Yin, the gym, our new groups</div>
    <div class="scale-stop" style="left:40%"><b>30 to 35°C</b>Power Yoga, Fire Pilates</div>
    <div class="scale-stop" style="left:74%"><b>35 to 40°C</b>Fierce Grace, Hot Yoga 60</div>
    <div class="scale-stop" style="left:100%"><b>40°C</b>Hot 26 &amp; 2</div>
  </div>
</div>'''

def six_band(href="six-week-start.html#groups", label="See the groups and how it works"):
    return f'''<section class="section"><div class="wrap"><div class="band"><div class="band-inner">
  <div class="stack"><span class="kicker">Next cycle starts {CYCLE_NOW}</span><h2 class="display">The six-week groups</h2>
  <p>Six weeks, two sessions a week, in a small group of people starting at the same point as you. One session downstairs in the gym and one upstairs in the studio. The groups run in six-week cycles all year: the next runs from {CYCLE_NOW} up to Christmas, and the one after that starts in {CYCLE_NEXT} {TBC("date")}.</p>
  <div class="cta-row"><a class="btn" href="{href}">{label}</a></div></div>
  <div class="price-tag"><span class="big">£50</span><span>for six weeks, about £4 a session</span>
  <ul><li>Sign-up only, so the group stays the same</li><li>Carry on into the next cycle, or move into any regular class</li><li>15% off your first membership or class pack afterwards</li></ul></div>
</div></div></div></section>'''
SIX_BAND = six_band()

# ---------------- pages ----------------
P = {}

P["index.html"] = ("Gym, yoga and hot yoga in Stirling for beginners | Heat Fitness",
 "A friendly gym and yoga studio in Stirling, and the only hot yoga studio in town. Hot, warm and unheated yoga, TRX, a small gym and personal training with Helen, plus six-week groups for beginners.",
 f'''<section class="hero"><div class="wrap hero-grid">
  <div><span class="kicker">Heat Fitness, Borrowmeadow Road, Stirling</span>
    <h1 class="display" style="margin-top:.6rem">Walking in<span class="hand">is the hardest part.</span></h1>{UNDERLINE}
    <p class="lead">Hi, welcome to Heat. I'm Helen. I've worked here since the studio opened, and it's my absolute pleasure to be running it now. I want this to be a space with something for everybody, from super slow, on-the-floor yoga to hot classes and strength sessions in the gym. You only ever do what you can manage, and nobody's going to force anything on you.</p>
    <p class="lead" style="margin-top:.9rem">Already one of us? Your Hot 26 &amp; 2, Fierce Grace and Yin are going nowhere. Everything I'm doing here is for you guys, so tell me what you want and I'll do my best to make it happen. See you on the mat!</p>
    <p class="hand" style="font-size:1.8rem;margin-top:.2rem">Helen x</p>
    <div class="cta-row"><a class="btn" href="start-here.html">New here? Start here</a></div>
    <p class="cta-note" style="margin-top:1rem">or just text me on {PHONE_A}</p></div>
  <figure class="polaroid"><img src="assets/img/studio-helen.jpg" alt="Helen at the table in the studio, with a wall of colourful yoga mats behind her" width="1600" height="1200"><figcaption>Pop in for a cuppa</figcaption></figure>
</div></section>
<section class="section"><div class="wrap"><div class="doors">
  <a class="door hot" href="six-week-start.html"><span class="kicker">Next cycle starts {CYCLE_NOW}</span><h2 class="display">Six-week groups</h2><p>Two sessions a week in a small group, running in six-week cycles. £50 for the six weeks.</p><span class="go">See how it works</span></a>
  <a class="door" href="classes.html"><span class="kicker">Hot, warm or cool</span><h2 class="display">Classes</h2><p>Yoga, strength and TRX, with the temperature of every class.</p><span class="go">Find your class</span></a>
  <a class="door" href="one-to-one.html"><span class="kicker">Just you and Helen</span><h2 class="display">One-to-one</h2><p>Personal training in the gym or private yoga on the mat.</p><span class="go">One-to-one sessions</span></a>
  <a class="door" href="prices.html"><span class="kicker">No contracts</span><h2 class="display">Prices</h2><p>Try 10 days of unlimited classes for £20.</p><span class="go">See prices</span></a>
</div></div></section>
<section class="section"><div class="wrap"><div class="sec-head"><span class="kicker">Inside Heat Fitness</span><h2 class="display">Upstairs and downstairs</h2></div><div class="gallery"><figure class="g-wide"><img src="assets/img/photos/gym-corridor.jpg" alt="The gym and TRX space downstairs" loading="lazy"><figcaption>The gym and TRX space downstairs</figcaption></figure><figure class="g-tall"><img src="assets/img/photos/studio-candles.jpg" alt="The studio, set for an evening class" loading="lazy"><figcaption>The studio, set for an evening class</figcaption></figure><figure class=""><img src="assets/img/photos/yoga-restorative.jpg" alt="Yoga with bolsters and blocks" loading="lazy"><figcaption>Yoga with bolsters and blocks</figcaption></figure><figure class=""><img src="assets/img/photos/trx-boxing.jpg" alt="TRX and boxing" loading="lazy"><figcaption>TRX and boxing</figcaption></figure><figure class="g-wide"><img src="assets/img/photos/studio-group.jpg" alt="After class in the studio" loading="lazy"><figcaption>After class in the studio</figcaption></figure><figure class=""><img src="assets/img/photos/members-mural.jpg" alt="Members by the mural" loading="lazy"><figcaption>Members by the mural</figcaption></figure></div></div></section>
<section class="section"><div class="wrap">
  <div class="sec-head" style="flex-direction:row;flex-wrap:wrap;justify-content:space-between;align-items:end"><div><span class="kicker">Latest from the studio</span><h2 class="display">News</h2></div><a href="news.html">More news</a></div>
  <div class="news" data-news="3"></div>
</div></section>
''')

P["six-week-start.html"] = ("Six-week groups for beginners in Stirling | Heat Fitness",
 "Small six-week groups at Heat Fitness in Stirling for perimenopause, menopause, over-60s, stiff backs and anxiety. Two sessions a week for £50, running in cycles all year.",
 f'''<section class="hero"><div class="wrap">
  <span class="kicker">Next cycle starts {CYCLE_NOW}</span>
  <h1 class="display" style="margin-top:.6rem;font-size:clamp(2.4rem,6vw,4.4rem)">Six-week groups<span class="hand" style="display:block;text-transform:none">two sessions a week, in a small group.</span></h1>{UNDERLINE}
  <p class="lead">Four weeks is too short to feel the difference, so we've made it six. You'll come twice a week with the same small group, one session downstairs in the gym and one upstairs in the studio. When one cycle ends the next begins, so you can join at the start of any cycle.</p>
  <div class="cta-row"><a class="btn" href="#groups">Pick your group</a><a class="btn ghost" href="#signup">Save your place</a></div>
</div></section>
{six_band("#signup", "Save your place")}
<section class="section"><div class="wrap"><div class="strip"><figure class=""><img src="assets/img/photos/studio-group.jpg" alt="A group in the studio" loading="lazy"><figcaption>A group in the studio</figcaption></figure><figure class=""><img src="assets/img/photos/trx-team.jpg" alt="The TRX team" loading="lazy"><figcaption>The TRX team</figcaption></figure><figure class=""><img src="assets/img/photos/members-group.jpg" alt="Friends made in class" loading="lazy"><figcaption>Friends made in class</figcaption></figure></div></div></section>
<section class="section"><div class="wrap split" style="align-items:start">
  <div class="stack"><h2 class="display" style="font-size:1.8rem">What you get</h2>
  <ul class="ticks">
    <li>Two sessions a week for six weeks, for £50 in total</li>
    <li>The same small group each week, all starting together</li>
    <li>A strength session in the gym and a yoga class in the studio</li>
    <li>Unheated sessions, plus a warm stretch for The Unstiffening</li>
    <li>15% off your first membership or class pack when the six weeks end</li>
  </ul>
  <p class="muted">The six weeks are sign-up only, not drop-in, so everyone in the group starts and finishes together. Spaces are limited.</p>
  <div class="cta-row"><a class="btn" href="#signup">Save your place</a><span class="muted">or text Helen on {PHONE_A}</span></div></div>
  <div class="stack" id="groups"><h2 class="display" style="font-size:1.8rem">Pick your group</h2>
  <div class="cards" style="grid-template-columns:1fr">{featured_cards()}</div></div>
</div></section>
<section class="section"><div class="wrap"><div class="faq">
  <details><summary>Do I need to be fit already?</summary><p>No. The six weeks are for people starting from wherever they are, and every exercise has an easier and a harder version.</p></details>
  <details><summary>What if I miss a session?</summary><p>Life happens. Let Helen know and she'll help you catch up. {TBC("catch-up policy")}</p></details>
  <details><summary>Can I just try one class first?</summary><p>Yes. If the six weeks aren't for you, bring our leaflet and your first class is free.</p></details>
  <details><summary>What happens after six weeks?</summary><p>The groups run in cycles, so you can carry straight on into the next six weeks with your group. Or you can move into any of our regular classes, with 15% off your first membership or class pack. Two weeks before the end, Helen will chat to you about what suits you best.</p></details>
  <details><summary>When does the next cycle start?</summary><p>The next cycle starts {CYCLE_NOW} and runs up to Christmas. The one after that starts in {CYCLE_NEXT} {TBC("date")}. If you can't make this one, save your place for the next.</p></details>
</div></div></section>
<section class="section" id="signup"><div class="wrap split" style="align-items:start">
  <div class="stack"><span class="kicker">Save your place</span><h2 class="display" style="font-size:1.8rem">Sign up for a group</h2>
  <p>Tell us which group you'd like to join and how to reach you. Helen will get back to you to confirm your place, the times and how to pay. Nothing is charged until she does.</p>
  <p>Prefer not to fill in a form? Text Helen on {PHONE_A} and she'll reply by text.</p></div>
  <form class="card" name="six-week-signup" method="POST" data-netlify="true" netlify-honeypot="company" action="thanks.html">
    <input type="hidden" name="form-name" value="six-week-signup">
    <p hidden><label>Leave this empty <input name="company"></label></p>
    <label for="sw-group">Which group?<select id="sw-group" name="group" required>
      <option value="">Choose a group</option>{"".join(f'<option value="{g[0]}">{g[0]} ({g[1][0].lower() + g[1][1:]})</option>' for g in FEATURED)}
      <option value="Not sure yet">I'm not sure yet, help me choose</option></select></label>
    <label for="sw-cycle">Which cycle?<select id="sw-cycle" name="cycle"><option>Starting {CYCLE_NOW}</option><option>The next one, in {CYCLE_NEXT}</option></select></label>
    <label for="sw-name">Your name<input id="sw-name" name="name" autocomplete="name" required></label>
    <label for="sw-contact">Phone number or email<input id="sw-contact" name="contact" autocomplete="tel" required></label>
    <label for="sw-msg">Anything Helen should know? (optional)<textarea id="sw-msg" name="message" rows="3"></textarea></label>
    <p class="muted" style="font-weight:400;font-size:.9rem">We only use your details to arrange your place. See our <a href="privacy.html">privacy notice</a>.</p>
    <button class="btn" type="submit">Save my place</button><p class="form-msg" role="status"></p>
  </form>
</div></section>''')

CLASSES = [
 ("Unheated and warm", [
   ("Yin 60", "Unheated", "unheated", "Close your day with an hour of deep stretching. A slow-paced style of yoga, mostly on the floor with plenty of props, that encourages relaxation and leaves you feeling calmer.", "Wednesdays 6:45pm, with Helen"),
   ("Yin and Somatics", "Unheated", "unheated", "A deeply restorative 75 minutes, using gentle somatic movements and yin postures to calm, stretch and unwind both the body and the nervous system.", "Sundays 10am, with Yvonne"),
   ("Power Yoga", "Warm, 32°C", "30", "An hour of power based on traditional Ashtanga yoga. A fast-moving class with sun salutations, a warrior series and balances, building strength, flexibility and balance.", "Thursdays 5:45pm, with Laura"),
   ("Fire Pilates and Flow", "Warm, 30 to 35°C", "30", "Lightly weighted mat Pilates with some yoga flow, though it's more Pilates than yoga. Plenty of core work in a warm room.", "Wednesdays 5:30pm"),
 ]),
 ("Hot", [
   ("Fierce Grace", "Hot, 35 to 40°C", "38", "A beginner-level yoga sequence in the hot room, with quiet music in the background. You explore the postures with help from the teacher if you need it, there are props and blocks, and you never do anything you don't want to do.", "Mondays 6pm (75 min), Thursdays 6:30am, Fridays 5:30pm, and most Saturdays 9am (90 min)"),
   ("Hot 26 &amp; 2", "Hot, 40°C", "40", "The original hot yoga sequence of 26 postures and two breathing exercises. Choose the 60-minute express or the 90-minute original, and work at your own level.", "Express: Tuesdays 6:30am and 6pm. Original: Sundays 4:30pm, and one Saturday a month at 9am"),
   ("Hot Yoga 60", "Hot, 35 to 40°C", "38", "Sixty minutes of beginner-level yoga postures in the hot room. A friendly way to try the heat.", "Wednesdays 9:45am, with Helen"),
 ]),
 ("Strength", [
   ("The gym", "Unheated", "unheated", "The gym is downstairs, and it's small and friendly. Every newcomer gets a proper walk-through, so nobody is left wondering how the kit works.", "All levels"),
   ("TRX Suspension Training", "Unheated", "unheated", "A full-body workout using TRX straps and your own body weight, with your core working throughout. Perfect for beginners, with options for anyone who's been on the straps a while.", "Mondays and Fridays 12pm, 45 minutes, with Helen"),
   ("Strength and Conditioning", "Unheated", "unheated", "A 45-minute strength circuit for your whole body. You keep the same moves for four weeks so you can track your progress and get stronger, with more reps or heavier weights, then the programme changes each month.", "Tuesdays 5:30pm, with Helen"),
   ("Women's Strength, over 40s", "Unheated", "unheated", "A small women's-only strength group for women over 40, through perimenopause and menopause. More weights than cardio, because once you hit that beautiful number, building strength is the key. It's small group personal training, booked a month at a time, so <a href=\"contact.html\">message Helen</a> to join.", "Wednesdays and Fridays 6:30am, £15 a session"),
   ("Personal training", "Your choice", "unheated", "One-to-one with Helen in the gym or on the mat. <a href=\"one-to-one.html\">See one-to-one sessions</a>.", "From £40 per person"),
 ]),
]
def class_sections():
    out = ""
    for group, items in CLASSES:
        cards = "".join(f'''<article class="card"><h3>{n}</h3>{temp(tl, tk)}<p>{d}</p><div class="meta"><span>{lvl}</span>{"" if n in ("Personal training", "Women's Strength, over 40s") else '<a data-book href="timetable.html#book">See times and book</a>'}</div></article>''' for n, tl, tk, d, lvl in items)
        ph = {"Unheated and warm": ("yoga-class-wide", "A yoga class in the studio"), "Hot": ("yoga-lunge", "A class in the hot room"), "Strength": ("trx-class", "TRX downstairs")}[group]
        aid = {"Unheated and warm": "warm", "Hot": "hot", "Strength": "strength"}[group]
        out += f'<section class="section" id="{aid}"><div class="wrap"><div class="sec-head"><h2 class="display">{group}</h2></div><img class="banner" src="assets/img/photos/{ph[0]}.jpg" alt="{ph[1]}" loading="lazy"><div class="cards">{cards}</div></div></section>'
    return out

P["classes.html"] = ("Yoga and strength classes in Stirling, hot and unheated | Heat Fitness",
 "Hot, warm and unheated yoga, TRX and beginner strength sessions on Borrowmeadow Road. See the temperature of every class.",
 f'''<section class="hero"><div class="wrap">
  <span class="kicker">Classes</span><h1 class="display" style="margin-top:.6rem;font-size:clamp(2.4rem,6vw,4.4rem)">Hot, warm<span class="hand" style="display:block;text-transform:none">or not heated at all.</span></h1>{UNDERLINE}
  <p class="lead">From 40°C Hot 26 &amp; 2 to unheated Yin, every class shows its temperature, so you can choose what suits you.</p>
  <div class="cta-row"><a class="btn" data-book href="timetable.html#book">See the live timetable and book</a></div>
  <nav class="jump" aria-label="On this page"><a href="#hot">Hot</a><a href="#warm">Warm and unheated</a><a href="#strength">TRX and the gym</a><a href="#groups">Six-week groups</a></nav>
</div></section>
<section class="section"><div class="wrap">{SCALE}</div></section>
{class_sections()}
<section class="section" id="groups"><div class="wrap">
  <div class="sec-head"><span class="kicker">New: six-week groups</span><h2 class="display">Our six-week groups</h2><p class="measure">Alongside the regular timetable, we now run small six-week groups for people who'd like a bit more support to get started. Each one has two sessions a week, one downstairs and one upstairs. Each group runs in six-week cycles, and the next starts {CYCLE_NOW}.</p></div>
  <div class="cards groups">{featured_cards()}</div>
  <div class="cta-row" style="margin-top:1.4rem;justify-content:center"><a class="btn" href="six-week-start.html#signup">Save your place</a><a class="btn ghost" href="six-week-start.html">How the six weeks work</a></div></div></section>''')

P["timetable.html"] = ("Class timetable and booking | Heat Fitness, Stirling",
 "The live class timetable for Heat Fitness in Stirling. See what's on, check spaces and book your class.",
 f'''<section class="hero"><div class="wrap">
  <span class="kicker">Timetable</span><h1 class="display" style="margin-top:.6rem;font-size:clamp(2.4rem,6vw,4.4rem)">Find a class<span class="hand" style="display:block;text-transform:none">and book your spot.</span></h1>{UNDERLINE}
  <p class="lead">Every class this week, with live spaces. Pick a day, then tap Book. New here? <a href="start-here.html">Here's what to expect</a>.</p>
</div></section>
<section class="section" id="book"><div class="wrap"><div class="booking">
  <div class="mindbody-widget" data-widget-type="Schedules" data-widget-id="d6713468a54"></div>
  <p class="booking-fallback muted">If the timetable doesn't appear, <a href="https://go.mindbodyonline.com/book/widgets/schedules/view/d6713468a54/schedule" target="_blank" rel="noopener">open it in a new tab</a>.</p>
</div></div></section>
<section class="section"><div class="wrap"><div class="sec-head"><span class="kicker">Six-week groups</span><h2 class="display">Our six-week groups</h2><p class="measure">Times for the six-week groups are being finalised. These are sign-up only, so <a href="six-week-start.html#signup">save your place here</a> rather than booking above.</p></div><div class="days" id="timetable"></div></div></section>
<section class="section"><div class="wrap"><div class="card"><h3>Still being finalised</h3><ul class="ticks" id="pending"></ul></div></div></section>
<script src="https://brandedweb.mindbodyonline.com/embed/widget.js" async></script>''')

P["prices.html"] = ("Prices and passes | Heat Fitness, Stirling",
 "The six-week start for £50, plus drop-ins, class passes and monthly passes at Heat Fitness in Stirling. No contracts. 20% off for students, over-65s, NHS staff and people on Universal Credit.",
 f'''<section class="hero"><div class="wrap">
  <span class="kicker">Prices</span><h1 class="display" style="margin-top:.6rem;font-size:clamp(2.4rem,6vw,4.4rem)">Prices<span class="hand" style="display:block;text-transform:none">and no contracts.</span></h1>{UNDERLINE}
  <p class="lead">Start small and only commit once you know you like it.</p>
  <div class="cards three" style="margin-top:1.4rem">
    <div class="card"><span class="for">New to exercise?</span><h3>The six-week groups</h3><p>Two sessions a week in a small group for £50. The best way in if you'd like support.</p><div class="meta"><a href="six-week-start.html#groups">See the groups</a></div></div>
    <div class="card"><span class="for">Want to try everything?</span><h3>10 days for £20</h3><p>Unlimited regular classes for ten days, so you can find the ones you love.</p><div class="meta"><a data-book href="timetable.html#book">Book a class</a></div></div>
    <div class="card"><span class="for">Got our leaflet?</span><h3>Your first class free</h3><p>Bring the leaflet to any regular class and your first one is on us.</p><div class="meta"><a data-book href="timetable.html#book">Pick a class</a></div></div>
  </div>
</div></section>
<section class="section"><div class="wrap price-grid">
  <div><h3>Drop in</h3><div class="table-wrap"><table><thead><tr><th>Class</th><th style="text-align:right">Price</th></tr></thead><tbody>
    <tr><td>Hot yoga, 60 minutes</td><td class="num">£13</td></tr><tr><td>Hot yoga, 75 minutes</td><td class="num">£14</td></tr>
    <tr><td>Hot yoga, 90 minutes</td><td class="num">£15</td></tr><tr><td>Yin</td><td class="num">£12</td></tr>
    <tr><td>Hot core, or weights and cardio<br><span class="muted">When they're on the timetable</span></td><td class="num">£13</td></tr><tr><td>TRX</td><td class="num">£8</td></tr></tbody></table></div></div>
  <div><h3>Monthly passes</h3><div class="table-wrap"><table><thead><tr><th>Pass</th><th style="text-align:right">Per month</th></tr></thead><tbody>
    <tr><td>Yoga<br><span class="muted">Yoga, hot core, weights and cardio</span></td><td class="num">£65</td></tr>
    <tr><td>Yoga and TRX<br><span class="muted">Everything, including TRX</span></td><td class="num">£75</td></tr>
    <tr><td>Family yoga<br><span class="muted">For couples or two people in the same family</span></td><td class="num">£110</td></tr>
    <tr><td>Family yoga and TRX</td><td class="num">£125</td></tr></tbody></table></div></div>
  <div><h3>Class passes</h3><div class="table-wrap"><table><thead><tr><th>Pass</th><th style="text-align:right">Price</th></tr></thead><tbody>
    <tr><td>Yoga, 5 classes<br><span class="muted">Use within 4 months</span></td><td class="num">£60</td></tr>
    <tr><td>Yoga, 10 classes<br><span class="muted">Use within 6 months</span></td><td class="num">£115</td></tr>
    <tr><td>TRX, 5 classes</td><td class="num">£36</td></tr><tr><td>TRX, 10 classes</td><td class="num">£70</td></tr></tbody></table></div></div>
  <div class="stack"><h3>Good to know</h3>
    <ul class="ticks"><li>20% off everything except intro offers for students, over-65s on a full pension, NHS staff and people on Universal Credit</li>
    <li><a href="one-to-one.html">One-to-one sessions</a> in the gym or on the mat, from £40 per person</li>
    <li>New here? Try 10 days of unlimited classes for £20</li></ul>
    <div class="cta-row"><a class="btn" data-book href="timetable.html#book">Book a class</a><a class="btn ghost" href="contact.html">Ask about passes</a></div></div>
</div></section>
{SIX_BAND}''')

P["start-here.html"] = ("Beginners welcome: your first visit to Heat Fitness, Stirling",
 "What happens at your first session, what to bring, and which classes aren't heated.",
 f'''<section class="hero"><div class="wrap hero-grid">
  <div><span class="kicker">New here?</span><h1 class="display" style="margin-top:.6rem;font-size:clamp(2.4rem,6vw,4.4rem)">Your first visit<span class="hand" style="display:block;text-transform:none">step by step.</span></h1>{UNDERLINE}
  <p class="lead">Here's exactly what happens, so there are no surprises.</p></div>
  <figure class="polaroid tall"><img src="assets/img/helen-portrait.jpg" alt="Helen smiling in the studio" width="900" height="1000"><figcaption>See you soon!</figcaption></figure>
</div></section>
<section class="section"><div class="wrap split" style="align-items:start">
  <ol class="steps">
    <li><div><h3>Get in touch</h3><p>Text or call Helen on {PHONE_A} and tell her a little about what you're looking for. She'll suggest a class that suits you.</p></div></li>
    <li><div><h3>Fill in a short health form</h3><p>It asks about injuries or conditions so Helen can adjust things for you. It stays private.</p></div></li>
    <li><div><h3>Arrive ten minutes early</h3><p>Helen will show you round, explain what happens and find you a spot. At the back or by the door is fine.</p></div></li>
    <li><div><h3>Go at your own pace</h3><p>Every exercise has an easier version. Rest whenever you like, and you can leave at any point.</p></div></li>
  </ol>
  <div class="card"><img class="card-img" src="assets/img/photos/welcome-door.jpg" alt="A warm welcome at the studio door" loading="lazy"><h3>What to bring</h3><ul class="ticks"><li>Comfortable clothes you can move in</li><li>A bottle of water</li><li>A towel for hot classes</li><li>Mats and props are here for you</li></ul>
  <p class="muted">Not sure which class to try? Start with something unheated, like one of <a href="six-week-start.html#groups">our six-week groups</a> or Yin.</p></div>
</div></section>
<section class="section"><div class="wrap"><div class="sec-head"><h2 class="display">Questions people ask</h2></div><div class="faq">
  <details><summary>Is every class hot?</summary><p>No. Plenty of our classes aren't heated at all, and others are warm rather than hot. Every class lists its temperature on the <a href="classes.html">classes page</a>.</p></details>
  <details><summary>Do I need to be fit or flexible?</summary><p>No. Most people who walk in for the first time feel the same way, and every exercise has an easier option.</p></details>
  <details><summary>Can I leave if I need to?</summary><p>Yes, any time, and nobody will ask why.</p></details>
  <details><summary>Are there stairs?</summary><p>The gym is on the ground floor. The yoga studio is upstairs: 16 steps to a landing, then 10 more, and there's no lift. If stairs are hard for you, tell Helen and she'll suggest something downstairs. There's an accessible toilet with grab rails downstairs, and another toilet upstairs.</p></details>
  <details><summary>Is there parking?</summary><p>{TBC("parking details")}</p></details>
  <details><summary>How much is it?</summary><p>Your first class is free with our leaflet. After that, see <a href="prices.html">our prices</a>. There are no contracts.</p></details>
</div></div></section>''')

P["meet-helen.html"] = ("Meet Helen, owner of Heat Fitness, Stirling",
 "Helen is a qualified personal trainer and yoga teacher who runs Heat Fitness in Stirling.",
 f'''<section class="hero"><div class="wrap hero-grid">
  <div><span class="kicker">Meet Helen</span><h1 class="display" style="margin-top:.6rem;font-size:clamp(2.4rem,6vw,4.4rem)">Hello, I'm Helen<span class="hand" style="display:block;text-transform:none">and this is my studio.</span></h1>{UNDERLINE}
  <p class="lead">I'm a personal trainer and yoga teacher, and I run Heat Fitness with a lovely team of teachers, upstairs and downstairs.</p></div>
  <figure class="polaroid left tall"><img src="assets/img/helen-mats.jpg" alt="Helen smiling in front of the wall of yoga mats" width="900" height="975"><figcaption>Helen</figcaption></figure>
</div></section>
<section class="section"><div class="wrap split" style="align-items:start">
  <div class="stack measure">
    <p>I've worked here since the studio opened, teaching for Jack and Jules, and now I've taken over from them. It's my absolute pleasure to be in charge. I want to create a space with something for everybody, whether that's super slow yoga on the floor, a sweaty hot class or a strength session downstairs.</p>
    <p>What keeps me going is watching people change. I've seen someone who couldn't touch their toes end up with their leg in the air. I've seen someone who couldn't lie still for a minute tell me the rest at the end is now their favourite bit. That's the kind of stuff that's why I do it.</p>
    <p>It's never a good idea to ram anything down anyone's throat, so I won't. I'd much rather work with what you want. Everything I'm doing here is for you guys, so tell me what you'd like and I'll do my best to make it happen.</p>
    <p>We're Stirling's only hot yoga studio, but not every class is hot. Downstairs there's a small gym where I teach strength. Upstairs there's the studio for yoga, hot and cool.</p>
    <p class="note" style="margin-top:.6rem">Pop in for a cup of tea first. No pressure, and no sales pitch.</p>
  </div>
  <div class="card"><h3>Qualifications</h3><ul class="ticks"><li>Level 3 Personal Trainer</li><li>Level 2 Certificate in Fitness Instructing</li><li>200-hour yoga teacher training, and around 700 classes taught</li><li>Menopause coach</li><li>TRX suspension training, Metafit and aqua fitness instructor</li><li>First aid trained</li><li>Training as a breathwork coach</li></ul></div>
</div></section>''')

P["contact.html"] = ("Contact and directions | Heat Fitness, Stirling",
 "Find Heat Fitness on Borrowmeadow Road, Stirling. Text or call Helen, check opening hours, and see parking and access.",
 f'''<section class="hero"><div class="wrap">
  <span class="kicker">Contact</span><h1 class="display" style="margin-top:.6rem;font-size:clamp(2.4rem,6vw,4.4rem)">Come and say hello</h1>{UNDERLINE}
  <p class="lead">The quickest way to reach Helen is a text. She'll get back to you as soon as she's out of class.</p>
</div></section>
<section class="section"><div class="wrap split" style="align-items:start">
  <dl class="info-list">
    <div><dt>Text or call Helen</dt><dd>{PHONE_A}</dd></div>
    <div><dt>Studio phone</dt><dd><a href="tel:01786473694">{STUDIO}</a></dd></div>
    <div><dt>Email</dt><dd><a href="mailto:helen@heatfitness.co.uk">helen@heatfitness.co.uk</a></dd></div>
    <div><dt>Address</dt><dd>{ADDR}<br>{POSTCODE}</dd></div>
    <div><dt>Opening hours</dt><dd>{TBC()}</dd></div>
    <div><dt>Getting here</dt><dd>Parking {TBC()}. The gym is on the ground floor, with an accessible toilet. The studio is upstairs, up 26 steps with a landing halfway, and there's no lift.</dd></div>
    <div><dt>Map</dt><dd><a href="https://www.google.com/maps/search/?api=1&query=Heat+Fitness+Borrowmeadow+Road+Stirling">Open in Google Maps</a></dd></div>
  </dl>
  <div class="card"><h3>Send a message</h3>
  <form name="contact" method="POST" data-netlify="true" netlify-honeypot="company" action="thanks.html">
    <input type="hidden" name="form-name" value="contact">
    <p hidden><label>Leave this empty <input name="company" id="company"></label></p>
    <label for="name">Your name<input id="name" name="name" autocomplete="name" required></label>
    <label for="email">Email or phone number<input id="email" name="contact" autocomplete="email" required></label>
    <label for="msg">What would you like to know?<textarea id="msg" name="message" rows="5" required></textarea></label>
    <p class="muted" style="font-weight:400;font-size:.9rem">We only use your details to reply to you. See our <a href="privacy.html">privacy notice</a>.</p>
    <button class="btn" type="submit">Send message</button><p class="form-msg" id="form-msg" role="status"></p>
  </form></div>
</div></section>''')

P["thanks.html"] = ("Message sent | Heat Fitness, Stirling", "Thanks for getting in touch with Heat Fitness.",
 f'''<section class="hero"><div class="wrap"><h1 class="display" style="font-size:clamp(2.4rem,6vw,4rem)">Thank you<span class="hand" style="display:block;text-transform:none">Helen will be in touch soon.</span></h1>{UNDERLINE}
 <p class="lead">If it's urgent, text her on {PHONE_A}.</p><div class="cta-row"><a class="btn" href="index.html">Back to the home page</a><a class="btn ghost" href="classes.html">See our classes</a></div></div></section>''')

P["privacy.html"] = ("Privacy notice | Heat Fitness, Stirling", "How Heat Fitness collects and uses your personal information.",
 f'''<section class="hero"><div class="wrap measure stack">
  <span class="kicker">Privacy notice</span><h1 class="display" style="font-size:clamp(2.2rem,5vw,3.4rem)">Your information</h1>{UNDERLINE}
  <p>Heat Fitness is run by Heat Fitness Stirling Ltd, which is registered with the Information Commissioner's Office {TBC("full ICO registration number")}. This notice explains what we collect and why.</p>
  <h2 style="font-size:1.3rem;margin-top:1rem">What we collect</h2>
  <p>Your name and contact details when you get in touch, book or join. Health information you give us on the health form, so we can keep you safe in class. Payment details are handled by our booking system, {TBC("booking system name")}, and we never see your full card number.</p>
  <h2 style="font-size:1.3rem;margin-top:1rem">How we use it</h2>
  <p>To reply to you, manage your bookings and membership, and keep you safe. We'll only send you news and offers if you've said yes, and you can stop them at any time.</p>
  <h2 style="font-size:1.3rem;margin-top:1rem">Who we share it with</h2>
  <p>Only the services we use to run the studio: our booking system, our website host and our email provider. We never sell your information.</p>
  <h2 style="font-size:1.3rem;margin-top:1rem">How long we keep it</h2>
  <p>{TBC("for example, while you're a member and for two years after")}</p>
  <h2 style="font-size:1.3rem;margin-top:1rem">Your rights</h2>
  <p>You can ask to see, correct or delete the information we hold about you. Email <a href="mailto:helen@heatfitness.co.uk">helen@heatfitness.co.uk</a>. If you're unhappy with how we've handled it, you can complain to the Information Commissioner's Office at ico.org.uk.</p>
  <p class="muted">Last updated {TBC("date")}</p>
</div></section>''')


P["one-to-one.html"] = ("Personal trainer and private yoga teacher in Stirling | One-to-one with Helen",
 "One-to-one personal training and private yoga in Stirling with Helen, a qualified female personal trainer and yoga teacher. Ideal for beginners, after physio, menopause and over-60s.",
 f"""<section class="hero"><div class="wrap hero-grid">
  <div><span class="kicker">One-to-one with Helen</span><h1 class="display" style="margin-top:.6rem;font-size:clamp(2.4rem,6vw,4.4rem)">Just you<span class="hand" style="display:block;text-transform:none">and a plan made for you.</span></h1>{UNDERLINE}
  <p class="lead">Helen is a qualified personal trainer and yoga teacher, so your one-to-one can be in the gym, on the mat, or a mix of both. It's ideal if you'd rather not start in a group, or you want a plan built around your body. Already train? Helen can review your programme, fix your technique and set a plan for your next goal.</p>
  <div class="cta-row"><a class="btn" href="contact.html">Ask Helen about a session</a><span class="cta-note">or text {PHONE_A}</span></div></div>
  <figure class="polaroid tall"><img src="assets/img/helen-mats.jpg" alt="Helen smiling in front of the wall of yoga mats" width="900" height="975"><figcaption>Let's have a chat</figcaption></figure>
</div></section>
<section class="section"><div class="wrap"><div class="cards two">
  <article class="card"><img class="card-img" src="assets/img/photos/one-to-one-gym.jpg" alt="One-to-one TRX training" loading="lazy"><span class="for">Downstairs</span><h3>In the gym</h3>
    <p>Personal training for strength, fitness and confidence. Helen shows you how everything works and writes a plan you can follow on your own, then checks in as you progress.</p>
    <ul class="ticks"><li>Getting started in a gym for the first time</li><li>Strength for bones, joints and everyday life</li><li>Picking up where physio left off</li><li>Training for an event or a goal</li></ul>
    <div class="meta"><span><b>From £40</b> per person</span>{temp("Unheated", "unheated")}</div></article>
  <article class="card"><img class="card-img" src="assets/img/photos/one-to-one-yoga.jpg" alt="Private yoga in the studio" loading="lazy"><span class="for">Upstairs</span><h3>On the mat</h3>
    <p>Private yoga at your pace. Learn the basics before joining a class, work around an injury, or have an hour of calm that's entirely yours. Hot, warm or unheated, whichever suits you.</p>
    <ul class="ticks"><li>Complete beginners who'd like the basics first</li><li>Stiff backs, hips and shoulders</li><li>Balance, breathing and sleep</li><li>A practice you can do at home</li></ul>
    <div class="meta"><span><b>From £40</b> per person</span>{temp("Your choice of temperature", "warm")}</div></article>
</div></div></section>
<section class="section"><div class="wrap split" style="align-items:start">
  <div class="stack"><h2 class="display" style="font-size:1.8rem">How it works</h2>
  <ol class="steps">
    <li><div><h3>A free chat first</h3><p>Tell Helen what you'd like to work on, and any injuries or conditions she should know about.</p></div></li>
    <li><div><h3>Your first session</h3><p>Helen sees how you move, what feels good and what doesn't, and agrees a goal with you.</p></div></li>
    <li><div><h3>A plan that fits</h3><p>One session, a block of sessions, or a mix of one-to-ones and classes. Whatever works for you.</p></div></li>
  </ol></div>
  <div class="card"><h3>Bring someone along</h3><p>Sessions also work for couples, two friends, family members or a small group, which brings the price down for each person. {TBC("shared session prices")}</p>
  <h3 style="margin-top:.6rem">Session packs</h3><p>{TBC("for example a block of 4 or 6 sessions, and its price")}</p></div>
</div></section>""")

P["news.html"] = ("News from the studio | Heat Fitness, Stirling",
 "The latest posts from Heat Fitness in Stirling: classes, workshops, timetable changes and life at the studio.",
 f"""<section class="hero"><div class="wrap">
  <span class="kicker">News</span><h1 class="display" style="margin-top:.6rem;font-size:clamp(2.4rem,6vw,4.4rem)">Latest from<span class="hand" style="display:block;text-transform:none">the studio.</span></h1>{UNDERLINE}
  <p class="lead">Our latest posts from Instagram and Facebook: new classes, workshops, timetable changes and what we've been up to.</p>
  <div class="cta-row"><a class="btn" href="https://www.instagram.com/heatfitnessscotland">Instagram</a><a class="btn ghost" href="https://www.facebook.com/HeatFitnessScotland">Facebook</a><a class="btn ghost" href="classes.html">See our classes</a></div>
</div></section>
<section class="section"><div class="wrap"><div class="news" data-news="12"></div></div></section>""")

P["resources.html"] = ("Free breathing exercises and short meditations | Heat Fitness, Stirling",
 "Free breathing exercises, short guided meditations and simple stretches from Helen at Heat Fitness in Stirling, to use at home between classes.",
 f"""<section class="hero"><div class="wrap">
  <span class="kicker">Free resources</span><h1 class="display" style="margin-top:.6rem;font-size:clamp(2.4rem,6vw,4.4rem)">A wee bit of calm<span class="hand" style="display:block;text-transform:none">for in between classes.</span></h1>{UNDERLINE}
  <p class="lead">These are little things I'd love you to use at home: breathing exercises, short meditations and simple stretches. They're free, there's nothing to sign up for, and you can come back to them whenever you need them. Pop your headphones on and give yourself five minutes.</p>
  <p class="muted" style="margin-top:.8rem">Everything here is gentle, but listen to your body. If something doesn't feel right, stop.</p>
  <p class="hand" style="font-size:1.8rem;margin-top:.4rem">Helen x</p>
</div></section>
<section class="section"><div class="wrap" id="resources"></div></section>
<section class="section"><div class="wrap"><div class="band"><div class="band-inner">
  <div class="stack"><h2 class="display">Want more?</h2><p>If these help, you'll love a class. Yin, Yin and Somatics and our six-week groups all use the same kind of breathing and slow movement.</p>
  <div class="cta-row"><a class="btn" href="classes.html">See our classes</a></div></div>
</div></div></div></section>""")

GP.build(P, temp, TBC, UNDERLINE, PHONE_A, CYCLE_NOW, CYCLE_NEXT)

# ---------------- write ----------------
ROOT = os.path.dirname(os.path.abspath(__file__))
for out in ("dist", "preview"):
    d = os.path.join(ROOT, out)
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(d, "assets"))
for fname, v in P.items():
    title, desc, body = v[:3]
    extra = JSONLD if fname == "index.html" else (v[3] if len(v) > 3 else "")
    full, prev = page(fname, title, desc, body, extra)
    open(os.path.join(ROOT, "dist", fname), "w").write(full)
    open(os.path.join(ROOT, "preview", fname), "w").write(prev if fname == "index.html" else full)
shutil.copy(os.path.join(ROOT, "favicon.ico"), os.path.join(ROOT, "dist", "favicon.ico"))
open(os.path.join(ROOT, "dist", "site.webmanifest"), "w").write('{"name":"Heat Fitness Stirling","short_name":"Heat Fitness","icons":[{"src":"assets/img/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"assets/img/icon-512.png","sizes":"512x512","type":"image/png"}],"theme_color":"#F68A1D","background_color":"#FBF4EC","display":"browser"}')
open(os.path.join(ROOT, "dist", "robots.txt"), "w").write("User-agent: *\nAllow: /\nSitemap: https://heatfitnessstirling.co.uk/sitemap.xml\n")
open(os.path.join(ROOT, "dist", "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
    "".join(f"<url><loc>https://heatfitnessstirling.co.uk/{'' if f == 'index.html' else f}</loc></url>" for f in P if f != "thanks.html") + "</urlset>")
# Old URLs from the previous site, so links and Google results keep working (Netlify format)
OLD = [("/classes/*", "/classes.html"), ("/services/*", "/classes.html"), ("/pricing/*", "/prices.html"),
       ("/new-members-intro-deal/*", "/prices.html"), ("/about/*", "/meet-helen.html"), ("/contact/*", "/contact.html"),
       ("/contact", "/contact.html"), ("/book-now/*", "/timetable.html"), ("/book-now", "/timetable.html"),
       ("/personal-training/*", "/one-to-one.html"), ("/blog/*", "/news.html"), ("/*", "/")]
NEW = "https://heatfitnessstirling.co.uk"
lines = []
# Visitors arriving on the old domain go to the matching page on the new one (active once heatfitness.co.uk points at Netlify)
for host in ("https://heatfitness.co.uk", "https://www.heatfitness.co.uk", "http://heatfitness.co.uk", "http://www.heatfitness.co.uk"):
    for frm, to in OLD:
        lines.append(f"{host}{frm}  {NEW}{to}  301!")
# Old page addresses typed on the new domain
for frm, to in OLD[:-1]:
    lines.append(f"{frm}  {to}  301")
open(os.path.join(ROOT, "dist", "_redirects"), "w").write("\n".join(lines) + "\n")

print("built", len(P), "pages")
for f in P:
    assert "—" not in open(os.path.join(ROOT, "dist", f)).read(), f

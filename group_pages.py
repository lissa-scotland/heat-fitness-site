"""One page per group, each written around the words that group types into Google.
Imported by build.py. Times stay 'to confirm' until Helen fixes the timetable."""
import json, re
from groups_data import G

SESS = {g["name"]: g for g in G}

# Groups with confirmed days and times: name -> (first session, last session) of the current cycle.
# Groups not listed here show "times to confirm".
START = {
    "Strong and Calm": ("Tuesday 10 November", "Thursday 17 December"),
    "The Unstiffening": ("Tuesday 10 November", "Thursday 17 December"),
    "Steady and Strong": ("Monday 9 November", "Wednesday 16 December"),
    "The Quiet Hour": ("Monday 9 November", "Wednesday 16 December"),
    "Strong Bones": ("Wednesday 11 November", "Saturday 19 December"),
}

GROUPS = [
 dict(name="Strong and Calm", when="Tuesdays and Thursdays, 9:45am", slug="perimenopause-exercise-stirling.html", photo=("gym-strength.jpg", "Strength training in the gym"),
  title="Perimenopause exercise classes in Stirling: strength and gentle yoga | Heat Fitness",
  desc="Small perimenopause classes in Stirling. Gentle strength training and slow, unheated yoga for sleep, energy and stress, with Helen at Heat Fitness.",
  kicker="Six-week group for perimenopause", h1a="Not sleeping?", h1b="Not feeling like yourself?",
  lead="Strong and Calm is a small group for women in perimenopause who are tired of being tired. Two sessions a week: gentle strength training in the gym, then slow, unheated yoga to help with sleep and stress.",
  who=["Your sleep, mood or energy has changed and you're not sure why it's happening now",
       "You've heard that strength training helps in perimenopause but you don't know where to start",
       "You'd like to be with other women going through the same thing",
       "Some weeks you have loads of energy and some weeks you have none"],
  faqs=[("Do I need to be fit to join?", "Not at all. When you arrive, you tell Helen how you feel today: green for full of beans, amber for so-so, red for running on empty. She shapes the session to match."),
        ("Is it hot yoga?", "No. Both sessions are unheated. Hot flushes are quite enough heat, thank you."),
        ("Do I need a diagnosis?", "No. If you think you might be in perimenopause, you're welcome. This is exercise and support, not medical advice, so speak to your GP about any symptoms that worry you.")]),
 dict(name="Strong Bones", when="Wednesdays at 5:30pm and Saturdays at 10:45am", slug="menopause-strength-classes-stirling.html", photo=("yoga-balance.jpg", "Balance work in the yoga studio"),
  title="Menopause and post-menopause strength classes in Stirling | Strong Bones at Heat Fitness",
  desc="Strength and balance classes in Stirling for women after menopause, with gentle warm yoga on Saturdays. Help to protect your bones and muscles in a small, unhurried group.",
  kicker="Six-week group for menopause and after", h1a="Strong enough", h1b="for the next thirty years.",
  lead="Strong Bones is for women after menopause who want to look after their bones, muscles and balance. Cool, unhurried strength training in the gym on Wednesday evenings and gentle yoga for balance in the warm room on Saturday mornings, in a group of no more than six.",
  who=["You've been told to look after your bone density, or you're worried about osteoporosis",
       "You'd like to feel steady on your feet and confident on stairs",
       "You've never lifted a weight and you'd like someone to show you how",
       "You'd like to train after work or on a Saturday morning, in a small group of women"],
  faqs=[("Is it safe if I have osteopenia or osteoporosis?", "Helen starts with very light weights and builds up slowly, watching how you move all the way. Strength training is one of the best things you can do for your bones. If you've been diagnosed, check with your GP or physio before you start, and tell Helen about any limits they've given you so she can plan around them."),
        ("Is it heated?", "Wednesday's strength session in the gym is unheated. Saturday's yoga is in a nicely warm room, straight after a hot yoga class has finished, so it's warm, not hot."),
        ("How many people are in the group?", "No more than six, so Helen can watch everyone closely.")]),
 dict(name="The Unstiffening", when="Tuesdays and Thursdays, 12:15pm", slug="back-pain-stiffness-classes-stirling.html", photo=("yoga-lunge.jpg", "A deep stretch in the yoga studio"),
  title="Classes for stiff backs and desk workers in Stirling: lunchtime strength and stretch | Heat Fitness",
  desc="Lunchtime classes in Stirling for stiff backs, tight hips and sore necks from sitting all day. Strength basics and a warm stretch, for every gender.",
  kicker="Six-week group for stiff backs, every gender", h1a="Your back called.", h1b="It would like a word.",
  lead="The Unstiffening is for anyone with a stiff back, tight hips or a sore neck from sitting at a desk or driving all day. Lunchtime strength basics downstairs and a deep stretch in the warm room upstairs, with time to shower before you go back to work.",
  who=["You sit at a desk or drive for most of the day",
       "Your back, hips or shoulders feel stiff, especially in the morning",
       "You'd like a short lunchtime session rather than an evening class",
       "You want something practical, with no chanting and no headstands"],
  faqs=[("Will it help my back pain?", "Lots of people find that moving more and getting stronger eases everyday stiffness. If you have pain that's new, severe or getting worse, see your GP or a physio first."),
        ("Is it hot?", "The gym session is unheated. The stretch upstairs is warm, about 28°C, which helps your muscles relax. It isn't hot yoga."),
        ("Who comes along?", "Mostly people who sit at a desk or drive all day, men and women alike.")]),
 dict(name="The Quiet Hour", when="Mondays at 7:30pm and Wednesdays at 8pm", slug="yoga-for-anxiety-stress-stirling.html", photo=("studio-candles.jpg", "The yoga studio with low lights and candles"),
  title="Gentle yoga and exercise for anxiety, low mood and stress in Stirling | The Quiet Hour",
  desc="A calm, predictable class in Stirling for anyone living with anxiety, low mood or stress. The same gentle routine each week, low lights and a small group.",
  kicker="Six-week group for anxiety, low mood or stress", h1a="Calm,", h1b="and the same every week.",
  lead="The Quiet Hour is for anyone living with anxiety, low mood or stress. It's the same simple routine at the same times every week, so nothing comes as a surprise. Low lights in the studio, low music, nobody watching, and you can leave whenever you need to.",
  who=["Walking into a gym or a busy class feels like too much",
       "You'd like to know exactly what will happen before you arrive",
       "You find gentle movement and breathing help you settle",
       "You'd like to be around people without having to talk"],
  faqs=[("What if I need to leave halfway through?", "That's absolutely fine. Sit near the door if it helps, and leave whenever you need to. Nobody will ask why."),
        ("Do I have to talk to anyone?", "No. You're welcome to arrive, take part and go home without chatting."),
        ("Do I have to phone?", "No. You can save your place with the online form, or send Helen a text and she'll reply by text."),
        ("Is this therapy?", "No. It's gentle exercise in a calm setting, and it doesn't replace any support you already have. If you're struggling, please also talk to your GP.")]),
 dict(name="Steady and Strong", when="Mondays and Wednesdays, 10am", slug="over-60s-exercise-classes-stirling.html", photo=("gym-corridor.jpg", "The gym downstairs, with plenty of wall to hold on to"),
  title="Exercise classes for over-60s in Stirling: strength, balance and gentle yoga | Heat Fitness",
  desc="Daytime strength and balance classes for over-60s in Stirling, with the wall to hold on to and a cup of tea afterwards. Unheated and beginner friendly.",
  kicker="Six-week group for over-60s", h1a="Daytime, no heat,", h1b="and a cuppa after.",
  lead="Steady and Strong is for anyone over 60 who wants to stay strong, steady on their feet and independent. Strength and balance in the gym with the wall to hold on to, and supported yoga upstairs. Tea and a chat afterwards is part of the class.",
  who=["You'd like to feel steadier on your feet and more confident on stairs",
       "Getting up from a low chair or the floor is harder than it used to be",
       "You've never been to a gym and you'd like a friendly start",
       "You'd enjoy meeting people and having a cup of tea after the class",
       "You've had a fall, or you worry about having one. We practise balance next to the wall and show you how to get up from the floor safely"],
  faqs=[("I haven't exercised for years. Is that okay?", "Yes. Most people who join haven't, and Helen starts everyone gently."),
        ("Is it heated?", "No. Both sessions are unheated."),
        ("How much is it?", "£50 for six weeks, which is twelve sessions at about £4 each, with tea included. Over-65s get 20% off passes after that. See the prices page for details.")]),
]

def when(name):
    for g in GROUPS:
        if g["name"] == name:
            return g["when"]
    return ""

def link_for_slug(slug):
    return any(g["slug"] == slug for g in GROUPS)

def link_for(name):
    for g in GROUPS:
        if g["name"] == name:
            return g["slug"]
    return None

def _session_card(s, where, temp):
    steps = "".join(f"<li><b>{lbl}</b>. {det}</li>" for _, lbl, det in s["steps"])
    return (f'<article class="card"><span class="for">{where}</span><h3>{s["kind"]}</h3>'
            f'<ul class="ticks">{steps}</ul>'
            f'<div class="meta"><span><b>{s["length"].capitalize()}</b></span>{temp}</div></article>')

def build(P, temp, TBC, UNDERLINE, PHONE, CYCLE_NOW, CYCLE_NEXT):
    from urllib.parse import quote
    for g in GROUPS:
        s = SESS[g["name"]]
        tkey = lambda t: "unheated" if t.lower().startswith("unheated") else "warm"
        down = _session_card(s["down"], "Downstairs, in the gym", temp(s["down"]["temp"], tkey(s["down"]["temp"])))
        up = _session_card(s["up"], "Upstairs, in the studio", temp(s["up"]["temp"], tkey(s["up"]["temp"])))
        who = "".join(f"<li>{w}</li>" for w in g["who"])
        st = START.get(g["name"])
        when_a = (f"{g['when']}, starting {st[0]}. The six weeks finish on {st[1]}." if st
                  else f"{g['when']}. Exact times are being confirmed now. Check the timetable page, or text Helen and she'll let you know.")
        starts = st[0] if st else CYCLE_NOW
        faqs = g["faqs"] + [("When are the sessions?", when_a),
                            ("Is it a one-off?", f"No. The groups run in six-week cycles all year. The next cycle starts {CYCLE_NOW}, and the one after that in {CYCLE_NEXT}. You can join at the start of any cycle, and carry on from one to the next."),
                            ("How do I join?", "Fill in the short form to save your place, and Helen will confirm the times and how to pay. Or text Helen and she'll answer any questions first.")]
        faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
        others = "".join(f'<a class="btn ghost" href="{o["slug"]}">{o["name"]}</a>' for o in GROUPS if o is not g)
        ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faqs]})
        signup = f'six-week-start.html?group={quote(g["name"])}#signup'
        body = f'''<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><a href="index.html">Home</a><span aria-hidden="true">›</span><a href="six-week-start.html#groups">Six-week groups</a><span aria-hidden="true">›</span><span aria-current="page">{g["name"]}</span></div></nav>
<section class="hero"><div class="wrap hero-grid">
  <div><span class="kicker">{g["kicker"]}</span><h1 class="display" style="margin-top:.6rem;font-size:clamp(2.4rem,6vw,4.4rem)">{g["h1a"]}<span class="hand" style="display:block;text-transform:none">{g["h1b"]}</span></h1>{UNDERLINE}
  <p class="lead">{g["lead"]}</p>
  <div class="cta-row"><a class="btn" href="{signup}">Save your place</a><a class="btn ghost" href="six-week-start.html#groups">Compare all groups</a></div>
  <p class="cta-note" style="margin-top:.8rem">{"Starts" if st else "Next cycle starts"} {starts}. Or text Helen on {PHONE}</p></div>
  <figure class="polaroid tall"><img src="assets/img/photos/{g["photo"][0]}" alt="{g["photo"][1]}" loading="lazy"><figcaption>{g["name"]}</figcaption></figure>
</div></section>
<section class="section"><div class="wrap split" style="align-items:start">
  <div class="stack"><h2 class="display" style="font-size:1.8rem">Is this for you?</h2><ul class="ticks">{who}</ul></div>
  <div class="card"><h3>A six-week group</h3><p>{g["name"]} is one of our six-week groups. It meets twice a week, once downstairs in the gym and once upstairs in the studio, with {s["size"].lower()} people so Helen gets to know everyone. It runs in six-week cycles all year: the next starts {starts}, and the one after that in {CYCLE_NEXT} {TBC("date")}. When your six weeks are up, you can carry on into the next cycle or move into any class on our <a href="classes.html">regular timetable</a>.</p>
  <div class="meta"><span><b>{g["when"]}</b>{"" if st else ", times " + TBC()}</span><span><b>£50</b> for six weeks</span></div>
  <span data-places="{g["name"]}" hidden></span>
  <div class="cta-row"><a class="btn" href="{signup}">Save your place</a></div></div>
</div></section>
<section class="section"><div class="wrap"><div class="sec-head"><h2 class="display">What happens in a session</h2></div>
  <div class="cards two">{down}{up}</div></div></section>
<section class="section"><div class="wrap measure"><div class="sec-head"><h2 class="display">Questions</h2></div><div class="faq">{faq_html}</div></div></section>
<section class="section"><div class="wrap"><div class="sec-head"><h2 class="display" style="font-size:1.6rem">Our other six-week groups</h2></div><div class="cta-row">{others}<a class="btn" href="six-week-start.html#groups">See all groups side by side</a></div>
  <p style="margin-top:1.2rem">Looking for something else? See <a href="classes.html">all our classes</a>, from hot yoga to TRX, or <a href="one-to-one.html">one-to-one sessions with Helen</a>.</p></div></section>'''
        P[g["slug"]] = (g["title"], g["desc"], body, f'<script type="application/ld+json">{ld}</script>')

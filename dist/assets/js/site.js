/* Heat Fitness site settings. Change these in one place. */
var HEAT = {
  // Where every "Book" button goes. The live Mindbody timetable sits on the Timetable page.
  // When the studio moves from Mindbody (contract ends 14 April 2027), swap the widget code on that page.
  bookingUrl: "timetable.html#book",
  // Latest News: paste the JSON feed link from Behold (behold.so) here once Helen connects her Instagram.
  // Until then, the news section shows the posts listed under "news" below.
  instagramFeed: "https://feeds.behold.so/nQSTANpwZDbxtYzddWgI",
  news: [
    { date: "", image: "assets/img/ig-poster.jpg", link: "https://www.instagram.com/heatfitnessscotland/",
      text: "New here? Try 10 days of unlimited classes for £20. Yoga, strength, suspension and circuits, plus one-to-one personal training and private yoga." },
    { date: "", image: "", link: "https://www.instagram.com/p/Ddbjn9sCLdd/",
      text: "TRX suspension training: the movement method where you are the weight plate. The team were back today to build some serious strength." },
    { date: "", image: "", link: "https://www.instagram.com/p/DdRiJSICKyB/",
      text: "As the evenings grow darker and the air a little cooler, there's no better time to bring a little warmth into your week." }
  ],
  // Free resources page. To add a recording:
  //   audio: put the mp3 in assets/audio/ and type its path, e.g. "assets/audio/bedtime-breathing.mp3"
  //   video: upload it to YouTube as "Unlisted" and paste the link, e.g. "https://youtu.be/abc123"
  // Anything without a recording shows as "Coming soon".
  resources: [
    { section: "Breathing", title: "Bedtime breathing", length: "3 minutes", blurb: "Slow, easy breathing to help you wind down and drift off.", audio: "", video: "" },
    { section: "Breathing", title: "Box breathing for a busy mind", length: "2 minutes", blurb: "Breathe in, hold, breathe out, hold. A simple pattern for when your head won't settle.", audio: "", video: "" },
    { section: "Breathing", title: "Breathe before you begin", length: "2 minutes", blurb: "A short settle to use before a class, a meeting, or anything that makes you nervous.", audio: "", video: "" },
    { section: "Short meditations", title: "Five-minute body scan", length: "5 minutes", blurb: "Lie or sit comfortably and notice each part of your body in turn.", audio: "", video: "" },
    { section: "Short meditations", title: "Ten minutes to switch off", length: "10 minutes", blurb: "A guided rest for the end of a long day.", audio: "", video: "" },
    { section: "Simple stretches", title: "Desk stretches", length: "4 minutes", blurb: "Loosen your neck, shoulders and back without leaving your desk.", audio: "", video: "" },
    { section: "Simple stretches", title: "Balance at the kitchen counter", length: "5 minutes", blurb: "Gentle balance practice, holding on to something sturdy.", audio: "", video: "" }
  ],
  // Places left in each six-week group, for the next cycle.
  // Put a number to show "3 places left", 0 to show "Full", or null to show nothing.
  places: {
    "Strong and Calm": null,
    "Strong Bones": null,
    "The Unstiffening": null,
    "The Quiet Hour": null,
    "Steady and Strong": null
  },
  // The timetable for the featured classes. Leave time as "" until it's confirmed and the page shows "to confirm".
  // floor: "down" (the gym) or "up" (the studio). heat: "unheated", "warm" or "hot".
  timetable: [
    { day: "Monday",     time: "10am",     name: "Steady and Strong",  floor: "down", heat: "unheated" },
    { day: "Wednesday",  time: "10am",     name: "Steady and Strong",  floor: "up",   heat: "unheated" },
    { day: "Tuesday",    time: "12:15pm",  name: "The Unstiffening",   floor: "down", heat: "unheated" },
    { day: "Thursday",   time: "12:15pm",  name: "The Unstiffening",   floor: "up",   heat: "warm" },
    { day: "",          time: "",       name: "The Quiet Hour",    floor: "down", heat: "unheated" },
    { day: "Wednesday", time: "",       name: "The Quiet Hour",    floor: "up",   heat: "unheated" },
    { day: "",          time: "",       name: "Strong Bones",      floor: "down", heat: "unheated" },
    { day: "",          time: "",       name: "Strong Bones",      floor: "up",   heat: "unheated" },
    { day: "Tuesday",    time: "9:45am",   name: "Strong and Calm",    floor: "down", heat: "unheated" },
    { day: "Thursday",   time: "9:45am",   name: "Strong and Calm",    floor: "up",   heat: "unheated" }
  ]
};

(function () {
  // Booking links
  document.querySelectorAll("[data-book]").forEach(function (a) {
    a.href = HEAT.bookingUrl;
    if (/^https?:/.test(HEAT.bookingUrl)) { a.target = "_blank"; a.rel = "noopener"; }
  });

  // Free resources
  var res = document.getElementById("resources");
  if (res) {
    var yt = function (u) { var m = String(u).match(/(?:youtu\.be\/|v=|embed\/|shorts\/)([\w-]{6,})/); return m ? m[1] : ""; };
    var secs = [];
    HEAT.resources.forEach(function (r) { if (secs.indexOf(r.section) < 0) secs.push(r.section); });
    res.innerHTML = secs.map(function (sec) {
      var items = HEAT.resources.filter(function (r) { return r.section === sec; });
      return '<div class="sec-head"><h2 class="display" style="font-size:1.8rem">' + esc(sec) + '</h2></div><div class="cards">' + items.map(function (r) {
        var media = "";
        if (r.video && yt(r.video)) media = '<div class="res-video"><iframe src="https://www.youtube-nocookie.com/embed/' + yt(r.video) + '" title="' + esc(r.title) + '" loading="lazy" allowfullscreen></iframe></div>';
        else if (r.video) media = '<video controls preload="none" src="' + esc(r.video) + '"></video>';
        else if (r.audio) media = '<audio controls preload="none" src="' + esc(r.audio) + '"></audio>';
        else media = '<span class="soon">Coming soon</span>';
        return '<article class="card res"><span class="for">' + esc(r.length) + (r.video ? " · video" : r.audio ? " · audio" : "") + '</span><h3>' + esc(r.title) + '</h3><p>' + esc(r.blurb) + '</p>' + media + '</article>';
      }).join("") + '</div>';
    }).join('<div style="height:2.4rem"></div>');
  }

  // Places left in the six-week groups
  document.querySelectorAll("[data-places]").forEach(function (el) {
    var n = HEAT.places[el.getAttribute("data-places")];
    if (n === null || n === undefined) { el.hidden = true; return; }
    el.hidden = false;
    el.className = "places" + (n === 0 ? " full" : n <= 2 ? " low" : "");
    el.textContent = n === 0 ? "Full for this cycle. Save a place for the next one" : n === 1 ? "Only 1 place left" : (n <= 2 ? "Only " : "") + n + " places left";
  });

  // Footer year
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  // Timetable
  var tt = document.getElementById("timetable");
  if (tt) {
    var days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    var html = "";
    days.forEach(function (d) {
      var slots = HEAT.timetable.filter(function (s) { return s.day === d && s.time; });
      html += '<div class="day"><h3>' + d + "</h3>";
      if (!slots.length) html += '<p class="empty">Nothing confirmed yet.</p>';
      slots.forEach(function (s) {
        html += '<div class="slot' + (s.heat === "unheated" ? " cool" : "") + '"><span class="t">' + s.time + "</span><span>" + s.name +
          "</span><span class=\"muted\">" + (s.floor === "down" ? "Downstairs, the gym" : "Upstairs, the studio") + "</span></div>";
      });
      html += "</div>";
    });
    tt.innerHTML = html;
    var pending = HEAT.timetable.filter(function (s) { return !(s.day && s.time); });
    var list = document.getElementById("pending");
    if (list) {
      if (!pending.length) { list.closest("section").hidden = true; }
      else list.innerHTML = pending.map(function (s) {
        return "<li><b>" + s.name + "</b>, " + (s.floor === "down" ? "downstairs" : "upstairs") +
          (s.day ? ", " + s.day : "") + ' <span class="tbc">time to confirm</span></li>';
      }).join("");
    }
  }

  // Latest News
  var boxes = document.querySelectorAll("[data-news]");
  function esc(t) { return String(t || "").replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function trim(t, n) { t = String(t || "").replace(/\s+/g, " ").trim(); return t.length > n ? t.slice(0, n).replace(/\s+\S*$/, "") + "..." : t; }
  function fmt(d) { var x = new Date(d); return isNaN(x) ? "" : x.toLocaleDateString("en-GB", { day: "numeric", month: "long" }); }
  function render(items) {
    boxes.forEach(function (box) {
      var n = parseInt(box.getAttribute("data-news"), 10) || 3;
      box.innerHTML = items.slice(0, n).map(function (p) {
        var img = p.image ? '<img src="' + esc(p.image) + '" alt="" loading="lazy">' : '<div class="news-mark" aria-hidden="true"></div>';
        return '<a class="news-card" href="' + esc(p.link) + '" target="_blank" rel="noopener">' + img +
          '<div class="news-body"><span class="news-date">' + (fmt(p.date) || "On Instagram") + "</span><p>" + esc(trim(p.text, 150)) + "</p></div></a>";
      }).join("");
    });
  }
  if (boxes.length) {
    render(HEAT.news);
    if (HEAT.instagramFeed) {
      fetch(HEAT.instagramFeed).then(function (r) { return r.json(); }).then(function (d) {
        var posts = Array.isArray(d) ? d : (d.posts || []);
        var items = posts.map(function (p) {
          var img = (p.sizes && p.sizes.medium && p.sizes.medium.mediaUrl) || p.thumbnailUrl || p.mediaUrl;
          return { date: p.timestamp, image: img, link: p.permalink, text: p.prunedCaption || p.caption };
        });
        if (items.length) render(items);
      }).catch(function () { /* keep the fallback posts */ });
    }
  }

  // Forms: on the live site Netlify sends them to Helen. Anywhere else (like a preview) they can't go anywhere.
  var live = /heatfitness(stirling)?\.co\.uk$|netlify\.app$/.test(location.hostname);
  document.querySelectorAll("form[data-netlify]").forEach(function (form) {
    if (!live) form.addEventListener("submit", function (e) {
      e.preventDefault();
      var m = form.querySelector(".form-msg");
      if (m) m.textContent = "This is a preview, so nothing was sent. On the live site it goes straight to Helen.";
    });
  });

  // Six-week sign-up: pick the group the visitor came from
  var pick = new URLSearchParams(location.search).get("group");
  var sel = document.getElementById("sw-group");
  if (pick && sel) {
    Array.prototype.forEach.call(sel.options, function (o) { if (o.value === pick) sel.value = pick; });
  }

  // Mobile menu: close it after a tap on a link, a tap outside it, or a scroll
  var menu = document.querySelector("details.menu");
  if (menu) {
    menu.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { menu.open = false; }); });
    document.addEventListener("click", function (e) { if (menu.open && !menu.contains(e.target)) menu.open = false; });
    var y0 = 0;
    window.addEventListener("scroll", function () { if (menu.open && Math.abs(window.scrollY - y0) > 80) menu.open = false; }, { passive: true });
    menu.addEventListener("toggle", function () { y0 = window.scrollY; });
  }
})();

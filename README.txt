HEAT FITNESS WEBSITE

dist/       The finished site. Drag this folder onto Netlify (app.netlify.com > Add new site > Deploy manually),
            or deploy it on Vercel as a static site. No build step needed.
build.py    The page content lives here. Edit it, run "python3 build.py", and dist/ is rebuilt.
assets/     Styles, script, photos and logos.

BEFORE LAUNCH
1. Search the pages for "tbc" (the yellow "to confirm" labels) and fill in every one.
2. In assets/js/site.js, set bookingUrl to the booking system's own link (Mindbody now, Gymcatch or TeamUp later).
   Don't leave it as heatfitness.co.uk/book-now/, because that page won't exist on the new site.
3. Fill in the class times in the timetable list in assets/js/site.js. A slot with no time shows as "to confirm".
4. Contact form: works automatically on Netlify (Netlify Forms). Turn on email notifications in the Netlify dashboard.
5. Point the domain at the host: in 123-reg, add the DNS records Netlify or Vercel gives you.
6. _redirects (Netlify) sends the old page addresses to the new pages, so Google results keep working.

PLACES LEFT IN THE SIX-WEEK GROUPS
Open dist/assets/js/site.js and find "places:" near the top.
Next to each group, type the number of places left (for example 3), 0 if it's full, or null to show nothing.
Save, then drag the dist folder onto Netlify's Deploys tab again.

FREE RESOURCES PAGE (breathing, meditations, stretches)
Open dist/assets/js/site.js and find "resources:" near the top.
Audio: put the mp3 file in dist/assets/audio/ and type its path next to audio, for example "assets/audio/bedtime-breathing.mp3".
Video: upload it to YouTube as Unlisted and paste the link next to video.
Anything without a recording shows as "Coming soon". Then drag the dist folder onto Netlify again.

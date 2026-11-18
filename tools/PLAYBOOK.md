# Behind The Hype — production playbook

Read this before making or reworking any post. The owner's notes on a specific post override this file for that post only.

## Brand
- Instagram @behind.the.hype.in · YouTube Shorts @behindthehype_in_speed
- Promise: the story behind everything India is hyped about. Pillars (from 19 Nov): **sport in depth** (Formula 1: business, engineering, history, present season, technical rules, teams/competitors, drivers; cricket: money, records, history, players, rivalries; other sports: football, Olympics, tennis, chess, kabaddi), **who keeps what** (everyday money: who earns what from things people buy), brands & startups, deals (M&A, India and global), results decoded, and two test pillars, **history** (India's engineering marvels and business history) and **space** (astronomy and the space economy, India angle first). The weekly calendar is in "Growth reset" below.
- Language: ALL on-screen text, headlines, captions and YouTube titles/descriptions in clear English. Never write the word "Hinglish" anywhere.
- Voice (owner, 19 Nov: "include Hindi in between to improve engagement, check the accent"): the voiceover mixes English with Hindi lines, about one line in three in Hindi. Use Hindi for the human moments: the reaction, the twist and the "socho..." line. Keep numbers, names and technical terms in English.
  - Write the Hindi lines in Devanagari in the voice script. This was tested on 19 Nov: Devanagari gives the most natural Hindi pronunciation; romanised Hindi also passed.
  - Style line: "Read aloud as a warm Indian male storyteller who switches naturally between English and Hindi, with a natural Indian accent in both. Relaxed pace."
  - On screen, each Hindi beat gets `"cap"`: the English rendering shown as its captions, so all on-screen text stays English.
  - **Accent check, every take.** Transcribe the take twice with the reel-transcriber script, once with `--lang hi` and once with `--lang en`. Every Hindi line must come back as the right Hindi words in the hi pass, and every English line as the right English words in the en pass. If a line comes back garbled or anglicised, simplify that line's Hindi and redo the take with a new file_name.
- The owner works at Blinkit. Every topic is allowed, including quick commerce, food delivery and their deals, as long as it uses only publicly available information (filings, official statements, major press). Never insider information or claims, and never anything that hints at what the owner knows from work.
- Every number must be confirmed in a reputable source (filings, major business press, official bodies); keep URLs in the row's `sources`. Drop anything you can't verify.

## Growth reset (owner, 19 Nov): followers and subscribers first
**Where we stand (18 Nov).** 15 reels. Every Instagram reel reaches roughly 100–140 accounts. That is the first test group Instagram gives any reel from a 1-follower account, and none of ours has gone past it. Watching improved a lot: skip rate fell from 75–89% to 43–52%, and average watch went from 2–6 s to 7–11 s. But across all 15 reels, people sent a reel to a friend once and saved one once. Sends are the signal Instagram uses most to show a reel to people who don't follow you, so with near-zero sends no reel gets wider reach. YouTube Shorts peaked with p006/p007 (255/347) and fell to 16–92 for the latest ones. Followers: 1. Subscribers: 2.
**What the scan proved (19 Nov, IDEAS.md Scan 4).** Our topics are right, but our packaging isn't:
- @untoldlessons_0 posted "₹102 of petrol: how much does the pump owner keep?" (the same topic as our p013) and got **10.3M views**.
- Its whole "You pay ₹X… who keeps what?" series runs at 0.9–2.6M views a reel.
- F1 engineering ("The F1 trick so genius it got banned", 5.3M on a 60K channel) and Indian history/engineering (Ellora Kailasa, Mehrangarh, 0.5–15M on 10–40K channels) are huge outlier pools.
- Space is weaker: under 100K a Short unless it's something like a "biggest planet" video.

**Rules from now on (they add to the growth rules below; they never replace accuracy rules):**
1. **Every reel belongs to a named, numbered series.**
   - The series name and number go in the frame-1 kicker and the thumbnail, e.g. "F1 EXPLAINED #3", "CRICKET MONEY #2", "WHO KEEPS WHAT #4", "INDIA BUILT THIS #1", "SPACE MONEY #1".
   - A series is the reason to follow. The last spoken line is a specific promise, not "follow for more": "Every Tuesday, one F1 secret. Follow for number four."
   - Never skip a series day once it's announced.
2. **Send test before scripting.** Write down who the viewer would send this to and why, e.g. "my F1-mad friend, because he thinks DRS is just a button". If there's no clear answer, change the angle. Put one line in the script aimed at that person: "Send this to the friend who still thinks Ferrari is the richest team."
3. **Debate beats facts for comments.** Sports reels end with a two-sided question fans will argue about ("Dhoni or Kohli: whose brand is worth more?"). Never ask for a vote on something with a factual answer.
4. **Weekly calendar (IST):**
   - Learn days stay Monday and Thursday; the research scan stays Monday.
   - A results decode or a big deal that's due takes Wednesday's slot. If it's truly time-critical it takes any day, and that day's series moves to the next free day.
   - Story-reel rules still apply to Saturday's Short.

   | Day | Series | What it covers |
   |---|---|---|
   | Mon | Cricket Money | IPL/BCCI money, player earnings, records, rivalries, cricket history with a twist |
   | Tue | F1 Explained | Rotate: engineering/tech (banned tricks first) → business/money → history/legends → drivers & rivalries → teams and rules |
   | Wed | Who Keeps What | "You pay ₹X for Y. Who keeps what?" (petrol, flights, cinema, cars, LPG, IRCTC). This week's results decode or deal goes here instead when due |
   | Thu | India Built This | History test: India's engineering marvels and old business history (forts, temples, stepwells, railways, dabbawalas) |
   | Fri | Long video | Rotate: F1 story → cricket story → history story → brand story |
   | Sat | Short from the long video | One only, ending with "The full story is on our YouTube channel, Behind The Hype." |
   | Sun | Space Money / other sports | Alternate: space (ISRO vs NASA costs, how satellites make money, astronomy with a number) and other sports (football clubs, Olympics, chess, kabaddi) |

5. **Test pillars get 4 reels each before a verdict** (history Thursdays, space every other Sunday). Judge by sends per reach, follows and skip rate versus that fortnight's sport and money reels. Log the results in tools/EXPERIMENTS.md. Drop or keep only after 4 data points.
6. **One deep reel a week (60–90 s).** Usually Wednesday's Who Keeps What, in the style of @untoldlessons_0's IPL owner reel: a full money walk-through, one step per beat, every number on screen.
   - Keep it under 4.6 MB: render 720x1280 if needed. Illustrated scenes compress well.
   - All other reels stay 25–40 s.
7. **Sport visuals are illustrations only.**
   - Allowed: drawn cars, helmets, tyres, tracks, maps, bats, balls, stadiums and big numbers.
   - Never: footage, photos, team logos, F1/IPL marks or faces. These are a copyright risk and break Instagram's originality rule, and footage/photos/logos would get us flagged as an aggregator.
   - Driver, team and player names in text are fine.
8. **Sources for sport:**
   - F1: FIA regulations and decisions, formula1.com, team statements, published team accounts (UK Companies House filings for teams' revenue), major outlets (BBC Sport, The Race, Autosport, Motorsport.com, Reuters).
   - Cricket: BCCI/ICC releases, franchise filings, ESPNcricinfo, major business press.
   - Astronomy: NASA/ESA/ISRO pages and budget documents.
   - Same two-source rule as everything else.
9. **Captions match the topics people pick in Instagram's "Your Algorithm" interest controls.** Line 1 names the topic plainly: "Formula 1", "F1", "cricket", "IPL", "space", "ISRO", "Indian history", plus the specific team or driver. Use at most 5 hashtags; Instagram caps posts at 5.
10. **Profile (owner action, once).** Name field "Behind The Hype | F1, Cricket & Money" (30 characters). Bio line 1: "The money & engineering behind sport, brands and history." Pin the three best reels. Claude can't edit the profile through the API; remind the owner only once.

**Tools checked on 19 Nov:**
- **instagram-agent-skill** (Jakeschincariol, 7.1K stars). We already use its ideas: hook scoring (tools/ytkit), outlier ranking and the safe zone. Adopted from it: the series/one-ask ending, the "pinned three" and "name field" profile fixes, and "sends per reach first".
- **cinematic-skill** (Moh4696). Can't run here: skia-python has no build for this Python, and Wikimedia is blocked from the shell. Adopted its rules into bth_long.py scripts: one hero per line; hits land on the spoken word; type readable on a phone in 1 s; nothing invented that looks real.
- **Agent Reach** (113K stars). A CLI for reading X, Reddit and YouTube. Its hosts are blocked from this shell; WebSearch/WebFetch cover the same ground.
- **Gemini.** Already used free via Make for the voice. A Gemini fact-check route would cost Make credits; only add it if a factual error ever ships.
- **ChatGPT.** Has no free API, so it's not used.

## Real pictures (from 19 Nov; owner allowed NASA, Wikimedia Commons and the F1 data API)
- **Get them** with `python3 -I tools/fetch_image.py search commons|nasa "<query>"`, then `get` the chosen one into `img/<name>.jpg`.
  - The tool refuses non-free Commons licences and writes `<file>.credit.txt`.
  - The Commons API often rate-limits this workspace, so search once and then get. Downloads go through curl (Python's client gets 429). Prefer NASA for space.
- **Allowed subjects:** places, buildings, monuments, machines, maps, space.
  - **NEVER** a photo of a real person: drivers, players, founders and leaders are all out.
  - No logos as the subject. Modern F1 team cars carry sponsor logos, so for F1 use circuits, historic cars, engines and parts, or keep the drawn style.
  - Look at every picture with the Read tool before using it.
- **Use:** on a beat, add `"photo": "img/<name>.jpg"` and `"credit": "<credit line>"`. This works in both bth_reel3.py and bth_long.py.
  - The picture shows as a tilted print with a slow zoom; any art shrinks to one sticker on its corner.
  - Optional `"pc": [fx, fy, w, h]` rings a spot on the picture in red (fractions of the picture), drawn as the narrator says it.
  - Use 1–3 photo beats per reel: the reveal and the "look at this" moment. Illustrations carry the rest.
- **Credit:** CC BY / BY-SA pictures need their credit line in the Instagram caption and the YouTube description too ("Photo: <author>, <licence>, Wikimedia Commons"). NASA pictures are public domain: write "Image: NASA", and never use NASA logos or imply endorsement.
- **F1 facts and stats:** `https://api.jolpi.ca/ergast/f1/<year>/...json` (standings, results, circuits; the free successor to Ergast). Cross-check headline facts with formula1.com or the FIA.

## Visual identity
Python Pillow, fonts in /usr/share/fonts/truetype/google-fonts/ (Poppins-Bold/Medium/Regular). Background #0E1116, accent #FFC72C, text #F5F5F0, secondary #969BA5. Small "BEHIND THE HYPE" label top-left in yellow with a short yellow underline, big bold headline, 90px margins, @behind.the.hype.in at the bottom. Avoid glyphs Poppins lacks (arrows, special symbols); check a render with the Read tool before using it.

## Reels (default format — about 5 of every 7 posts)
Every reel has a voiceover AND original background music. Silent reels are not allowed unless the voice step fails (then say so to the owner).

### Growth rules (from 2026-11-07; the first 3 reels got almost no reach)
- **Short.** 25–35 s (hard max 40). 5–7 beats, 70–100 spoken words. One surprising fact, one twist, one takeaway — cut everything else. Watch-through matters more than completeness.
- **Frame 1 is the hook and the Instagram cover** (the publisher uses frame 0). It must read on its own in under a second: the payoff claim or a tension, e.g. "Same gold. 12% pricier." Never a setup line, never "Today we look at...".
- **Spoken hook = the claim**, said in the first 2 seconds. Rotate hook types day to day: shocking number, "X vs Y", "Why does...?", "Nobody talks about...", "You paid ___ for ___".
- **Frame 1 text ≠ spoken line.** The on-screen hook and the spoken first line make the same promise in different words, so a muted viewer and a listening viewer each get the full hook (from youtube-agent-skill's Shorts rules).
- **Hold the answer back.** The hook opens a question the viewer can't close; the payoff comes in the last third. Don't answer your own hook in the same sentence.
- **Pick topics people forward.** Before choosing, ask: would someone send this to a friend or argue about it? Favour money in the viewer's pocket, price comparisons (India vs abroad, then vs now), famous brands, cricketers and films, and things everyone is talking about this week. Plain "news recap" is the weakest choice.
- **Be first.** When a topic is tied to a date (festival, match, launch, results), the post must be ready before or on that day, not after. Say "time-sensitive: approve today" in the owner message.
- **Rotate the ending.** Alternate: "Send this to whoever...", a one-line question that invites a comment, "Follow for a daily breakdown". Don't use the same ending two days running.
- **Loop the ending when it fits.** Write the last line so it leads back into the first (e.g. it ends on the question frame 1 asks), so a replay feels natural. Replays count as watch time on both platforms.
- Vary mood and seed every day; never reuse a script.

### Pipeline
1. **Script.** Each beat = one on-screen frame + one spoken line. Conversational and human: contractions, short sentences, a natural reaction now and then ("Wait, it gets better."). On-screen text max 4 short lines per beat: the key number or phrase in big type ("y"/"w"), a short context line ("s" or "W"), source in small grey ("g").
   **Hook gate (from 9 Nov).** Before recording, write 5 hook options (the spoken first line), each built on a different formula from `tools/ytkit/hooks.json`, put them in a text file one per line and run `python3 -I tools/ytkit/hookscore.py hooks.txt`. Use the top scorer unless it breaks a brand or accuracy rule; if the best is still "WEAK", rewrite it to fix the weakest property the tool names (often: say "you" early, name what's at stake, leave the answer open) and score again. Save the chosen hook's score on the dashboard row as "hookScore" and note it in PERFORMANCE.md so we learn whether the score predicts skip rate. A score is a check, not a promise.
2. **Voice.** Find the Make scenario named "BTH – Voiceover" (Make tool scenarios_list, teamId 3492645; currently id 8424575). Run it once (scenarios_run, responsive true) with:
   - `script`: all spoken lines joined with a blank line between beats (the pauses are used for timing),
   - `style`: a one-line direction, e.g. "Confident Indian-English male storyteller, like a sharp business YouTuber. Relaxed, unhurried pace with clear pauses between sentences; light emphasis on numbers." (owner, 8 Nov: not too fast). If the take runs over 40 s, shorten pauses over 0.3 s and speed up by at most 1.15x with ffmpeg atempo (see p006), or trim the script,
   - `file_name`: `post_NNN_vo` (or `post_NNN_vo_v2` for a rework).
   It saves `audio/<file_name>.wav` in this repo through Make's GitHub connection. `git pull --rebase` and use it. Default voice is Sadaltager on gemini-2.5-flash-preview-tts; keep the same voice so the page sounds consistent. Gemini can return an EMPTY file with a "success" status (seen 9 Nov at ~7:50 AM IST, likely the free-tier limit): check the .wav is not 0 bytes; if it is, delete it, do the rest of the run and retry later in the run (it worked again by ~12:50 PM IST). Never switch to gemini-2.5-pro-preview-tts (no free quota). If the saved file is tiny (under ~100 KB) or silent, Gemini returned an empty take (this happens on the free tier): retry with a NEW file_name (e.g. `post_NNN_vo_b`) and a much shorter style line (one plain sentence, e.g. "Read aloud in a warm, relaxed Indian-English male voice, unhurried, with a short pause between sentences."); that fixed p008 on 11 Nov after three empty takes. Never reuse the empty file's name in the same run. If the scenario is missing or fails, check the execution with executions_get-detail once, then fall back to music only and report it.
3. **Timing.** List the pauses (`ffmpeg -i audio/X.wav -af silencedetect=n=-35dB:d=0.2 -f null -`), match them to the sentence ends of each beat, and put the beat boundaries in the spec as `"cuts": [...]`. The automatic matcher is often a beat off; hand-checked cuts keep frames and captions in sync.
4. **Build.** Write `posts/post_NNN.json` (same format as before: out, voice, mood, seed, cuts, beats with `say` + `lines`) and run `python3 tools/bth_reel2.py posts/post_NNN.json`. v2 makes a hook-only first frame (no label, no slide counter, no progress bar), a slowly moving background, lines that pop in one by one, a count-up on the first big yellow number of each later beat (`"count": false` on a beat turns it off), word-by-word captions of the voiceover in the lower third, original music ducked under the voice, 1080x1920 H.264/AAC MP4. The `say` text must match the script sent to the voiceover, beat for beat. (`tools/bth_reel.py` is the old slideshow builder; don't use it for new posts.) Style reference: `posts/post_004_v2.mp4` (never published).
   **Illustrated A/B test (owner approved 9 Nov). Illustrated reels made so far: 3 of 3 (p006, p007, p008). Test complete. Owner's note on p009 (12 Nov) rejected the v2 look in favour of the illustrated style, so p009 was rebuilt with bth_reel3.py and new reels use the illustrated style (bth_reel3.py) by default unless the owner says otherwise.** Until 3 are made, every NEW reel uses `python3 tools/bth_reel3.py posts/post_NNN.json` instead, then update the count on this line and push. Same spec, plus on each beat `"art"`: 1–3 illustrations, biggest first, as emoji from Google's Noto Color Emoji (e.g. "🏭", "🚜", "📈", "🪔") or `"coin:₹"` / `"coin:%"` for a drawn coin. Pick art that shows the beat's idea literally (the thing, the place, the action). Never use money emoji with dollar signs (💰💵💸) for rupee stories: use `"coin:₹"`. No flags or emoji that stand for a specific real person. Optional `"bg"`: sun, sky, mint, coral or lilac (default rotates). v3 adds bright backgrounds, bouncing illustrations, outlined big text, a dark kicker pill from a short first "Y"/"W" line, and synthesised sound effects (whoosh on cuts, pop when art lands, tick when a number finishes counting). Put `"style": "illustrated"` on the dashboard row and note the style in PERFORMANCE.md. Revisions keep the post's original style. After the 3rd illustrated reel, go back to v2 and, once all 3 have 48-hour numbers, compare skip rate, average watch time and views against the last 3 v2 reels in PERFORMANCE.md and tell the owner which won; the owner decides the default.
5. Keep reels 25–40 s and under 4.6 MB (Make's free plan refuses files over 5 MB); confirm with ffprobe and ls.
6. Look at frame 0 and 3–4 other frames (stitched side by side) with the Read tool before delivering: hook readable, captions in step with the voice, nothing overlapping.

## YouTube thumbnail and tags (every reel)
- Make a cover with `python3 tools/bth_thumb.py '{"kicker": "...", "big": "...", "sub": "...", "hook": "..."}' posts/post_NNN_thumb.jpg`.
  - kicker: 1–3 word topic tag (e.g. "IPL auction", "UPI record").
  - big: the single most surprising number or claim, 2–4 words; use "|" to split into two lines (e.g. "₹25.2 cr bid|₹18 cr paid"). Keep it to 3 words or fewer where possible and do NOT repeat the YouTube title's words: the thumbnail says what the title doesn't.
  - sub: a short curiosity line that makes people want the answer (a question works best).
  - hook: one grey line of context. Look at the result with the Read tool; every fact on it must be in the reel.
- `youtube_tags`: 8–14 comma-separated search phrases people actually type (topic, people/brands, the general niche), always ending with "Behind The Hype,shorts".
- The publishing scenario already sets: public, NOT made for kids, Education category, English (India) audio, embedding allowed, subscribers notified. The AI-content label is off: a stock AI narrator over our own text graphics doesn't need it. Never add realistic AI images or video of real people or events without telling the owner, because those do need the label.

## Stay clear of YouTube's "inauthentic content" rule
YouTube demonetises channels that look mass-produced. Keep every reel clearly original: a researched angle and our own commentary (not just reading facts), varied structure and hooks from day to day, a different music seed and mood, no more than one upload a day, and never reuse a script.

## Topics come from the outlier matrix (tools/IDEAS.md)
- Pick each new post from tools/IDEAS.md: a timely news hook first if one fits a pattern there, otherwise the next unused idea, rotating subtopic and format day to day. Mark it "made (pNNN)" and push.
- Put a rupee number in the hook and the YouTube title whenever the story has one; origin stories with a twist and "X vs Y: which makes more?" are the proven patterns.
- Winners (see IDEAS.md) get remade within 2 weeks with a new hook and a different example. Never repost the same video.

## Deals (M&A) pillar (owner request, 8 Nov)
Trending and lesser-known ("hidden") mergers and acquisitions, India and global. Aim for about one deal post a week, more when a big deal breaks.
- Every Monday, as part of the research scan, search the news for the past 7 days' deals (Indian and global; also smaller deals the mainstream missed: a quiet stake buy, an open offer, a deal blocked or approved by a regulator). Add the best 1–2 to the IDEAS.md matrix under "Deals (M&A)".
- Every deal post explains the deal through these lenses, picking the 1–2 that make the story: **the money** (price, cash vs shares, how it's funded, debt taken on); **valuation** (the multiple paid, e.g. price ÷ revenue or ÷ profit, and the premium over the share price before the news; compute in Python); **synergy** (the cost savings or extra sales the buyer has said it expects, and by when; say it's the company's own target); **regulation** (CCI, RBI, SEBI open offer, foreign regulators such as the US FTC or the EU; what still needs approval); **why it matters to an ordinary viewer** (prices, jobs, a brand they use).
- Say whether a deal is announced, approved or completed. Rumoured deals only if reported by a major outlet, and say "reported".
- Educational only: no buy/sell/hold views, no "this stock will rise", no price targets. If a post discusses a listed company's shares, the caption ends with "Educational, not investment advice."
- Quick-commerce and food-delivery deals are fine (owner, 8 Nov), using public information only. Don't call any deal a failure unless the companies' own write-downs or results show it.
- Make the jargon plain on screen: "paid 4x its yearly sales", not "4x EV/Sales".

## Results decoded (owner request, 8 Nov)
From time to time, a brief decode of a company's latest quarterly or yearly results. Aim for about one every 1–2 weeks, more during results season (mid-Jan to mid-Feb, mid-Apr to mid-May, mid-Jul to mid-Aug, mid-Oct to mid-Nov for Indian companies), and always within 1–3 days of the results coming out.
- Pick companies viewers know and use (brands, banks, telecom, airlines, IT, carmakers, listed startups, quick commerce included) or a global giant with an India angle. Every Monday, as part of the research scan, check which well-known companies report that week and add 1–2 to the IDEAS.md matrix under "Results decoded".
- Source: the company's own results filing or investor presentation (BSE/NSE, or SEC for global companies), with major business press as a cross-check. Public information only.
- Structure (30–40 s): the headline number everyone will quote → the number that tells the real story (margin, a segment, cash flow, a one-off gain, cost per user, debt) → one line on why → what to watch next quarter.
- Always state the period and the basis exactly: "Q2 FY27 (Jul–Sep 2026), consolidated, vs the same quarter last year". Never mix periods. Compute every growth rate and margin in Python from the filed figures.
- Educational only: no buy/sell/hold views, no share-price predictions. The caption ends with "Educational, not investment advice." Say plainly what management said versus what the numbers show.
- On screen, plain words: "kept ₹12 of every ₹100 of sales as profit", not "12% PAT margin".

## Performance dashboard (owner request, 9 Nov)
"Behind The Hype performance" (Dashboard artifact https://claude.ai/artifact/JwC3Z7xK7iKJYQj2iAfrX3) is where the owner checks numbers; don't paste stats into chats or notifications beyond one line. Live Instagram/YouTube numbers come straight from Make data store 248952, so every insights pull shows up on its own. Two attached files need the run to keep them current (ArtifactData on that url; upload the new JSON with Artifact publish asset:true, then `update` the dataset's `url`, `name`, `updated` {at, by} and `edit` {via:"claude", at}):
- `datasets/posts` (bth_posts.json): one row per reel {post, short (a 1–2 word name the owner will recognise, e.g. "KKR", "UPI", "Dhanteras", "Tata Steel"), number, title, style, hook_type, hook_score, length_s, published_at, ig_media_id, youtube_id}. Add each new reel when it's made (ids null) and fill the ids once it is published (from the dashboard row's youtubeId and the data store's pNNN_instagram record, or match by publish time).
- `datasets/history` (bth_history.json): on every learn day append one row per published reel {post, checked (YYYY-MM-DD), ig_views, reach, avg_watch_s, skip_rate, shares, saves, yt_views}.
Never change the page (files/index.html) unless the owner asks for a change to the dashboard.

## Story reels (from 14 Nov, learned from ZeroInOn)
A new Bangalore history page (ZeroInOn) gets ~20x our Instagram views per reel with: one story about a person with a turning point ("He built H.A.L. Then lost it."), a well-known local place in the hook (Bellandur Lake, HAL Bangalore), cinematic scenes instead of text, and a long video with Shorts cut from it.
- Story reels are now a way of telling, used inside the series (F1 legends, cricket history, India Built This, brand stories) rather than a fixed 2-in-7 quota: a real person, team, brand or place; who → what they built → the turn → what's left today. Same research and sourcing rules as everything else.
- Hook = the person and the twist in under 8 words ("He sold detergent on a bicycle. Then beat HUL."). Put the city or landmark in the hook or title when the story has one (people share stories about their own city).
- Write it as a story, not a list of numbers: one number at most per beat, a short line that pulls to the next beat ("And then the government called."), the twist in the last third.
- Series: when a story has a natural second half, end Part 1 on the cliffhanger with "Part 2 tomorrow. Follow so you don't miss it." and make Part 2 the next day. Series give people a reason to follow/subscribe, which one-off facts don't.
- Visuals: illustrated style with art that shows the scene (place, product, era); at most one stat card per story reel.

## Weekly long video (from 14 Nov; owner uploads it by hand, no paid plan)
Long videos earn subscribers; Shorts earn views. One 4–7 minute story video a week, plus the following days' Shorts cut from the same story.
- When: the Friday daily run makes the long video INSTEAD of that day's reel. Saturday's and Sunday's reels are two Shorts from the same story (the hook moment, and the twist). Never say just "our channel": the spoken/on-screen ending is "The full story is on our YouTube channel, Behind The Hype."; the Instagram caption says "▶️ Watch the full N-minute <topic> story on our YouTube channel: link in bio."; the YouTube description names the long video's exact title, and once the owner has sent its link (recorded in PERFORMANCE.md under Long videos) includes that URL. Remind the owner in the notification to set the Short's Related video to the long video in YouTube Studio.
- Topic: rotate F1 story → cricket story → history story → brand story (IDEAS.md sport/history lists and story queue; person + turning point + twist). Sport long videos have strong YouTube search demand ("F1 engineering explained", "how IPL teams make money"), so put the search phrase in the title, researched like everything else: two sources for every key fact, a claim with only one source gets cut or softened.
- Script: 6–8 chapters, 600–900 words. Chapter 1 is a 20–30 s cold open that states the stakes and the mystery ("Twenty years later, India's biggest soap company had a plan with one goal. Stop him."). End with next week's teaser, "Subscribe so you don't miss it", and one comment question.
- Spec: `long/long_NNN.json` (format in the docstring of `tools/bth_long.py`): title_bar (brand, line1 white, line2 yellow, sub = brand · place · year), sections with chapter, bg, voice and beats (say, lines, art, optional circle = index of the illustration to ring in red, count false for years).
- Voice: one "BTH – Voiceover" run PER SECTION (file_name `long_NNN_sN`), never one long run: Gemini returns empty or cut-off takes on long text. Check every take: file over 100 KB, and transcribe it (reel-transcriber skill, `--lang en`) to confirm the whole section is there with no long silence. Redo a bad take with a NEW file_name and the short style line.
- Build: `python3 tools/bth_long.py long/long_NNN.json` (1920x1080, 25 fps; writes the .mp4, .srt subtitles and _chapters.txt). Thumbnail: `python3 tools/bth_thumb_long.py '{"line1": ..., "line2": ..., "tag": ..., "art": ..., "art2": ..., "bg": ...}' long/long_NNN_thumb.jpg` (two lines of 2–3 words, words different from the title, one illustration ringed in red). Check frames at 0 s and every chapter, and the thumbnail, with the Read tool.
- Deliver: push the mp4, srt, thumbnail and `long/long_NNN_upload.md` (title under 60 characters with the brand/person name first, description with a 2-line summary, the chapters list, sources and links, tags, upload steps). Then PushNotification: "This week's long video is ready to upload: <title>. Steps: https://github.com/hypebehindthe-spec/bth-media/blob/main/long/long_NNN_upload.md". Never upload it ourselves (Make's free plan can't carry files over 5 MB).

## Research scan (weekly, Mondays)
Run the publishing scenario 8381063 ONLY with post_type "research" (scenarios_run, responsive true):
- `media_url`: comma-separated Instagram usernames to study (business/creator accounts only; personal accounts come back empty). Current list: untoldlessons_0, labourlawadvisor, marketingmind.in, thebetterindia (zerodhaonline swapped out 19 Nov; also try 1–2 F1/cricket business pages found in the week's search, never the giant official accounts) — add or swap handles that fit the pillars; drop any that return nothing twice.
- `youtube_tags`: 5–6 comma-separated search phrases (Shorts, India, last 45 days, by views), rotate across the series, e.g. "f1 engineering explained,cricket money explained,who keeps how much india,indian engineering marvel history,isro cost explained" plus one timely phrase for the week.
Results land in data store 248952 under keys `rs_ig_<username>` (posts as `type|views|likes|comments|time|link|caption` joined by ";;") and `rs_yt_<query>` (detail = `videoIds##views##channelIds##titles` with titles split by "~~"; media_id = `channelIds##subs##videoCounts##channelViews`). Compute outlier scores in Python (method in IDEAS.md); for YouTube, a channel's median views over its recent Shorts is a better baseline than its lifetime average when that data is available, and skip channels with fewer than 4 data points, update the scan table and add/replace ideas in the matrix. Costs roughly 60–80 Make credits per scan.

## Format mix
- Reels every day except Friday (long video). The series calendar in "Growth reset" decides the topic. A "guess the number" opening can be used inside any series (ask on beat 1, reveal on the last beat).
- Every second week, the Sunday slot can instead be a save-worthy carousel cheat sheet for a series (e.g. "F1 team budgets 2026 in one table", "Every IPL team's value"). People save tables, and saves and sends lift reach.
- No quote posts and no AI presenter/character: they look mass-produced and blur what the page is for.

## Carousels / photos
1080x1350 JPEG (quality 92); build with `python3 tools/bth_carousel.py posts/post_NNN_carousel.json` (see p006 for the spec). Carousel 5–8 slides: hook, one idea per slide, takeaway + "Follow @behind.the.hype.in for a new breakdown every day".

## Captions
Instagram search reads captions and on-screen text, so write for search, not hashtags.
- Line 1: the hook, with the words people would search (e.g. "Dhanteras gold price", "IPL auction", "iPhone price India").
- 2–3 short lines of value (the twist and one extra fact that isn't in the reel, to reward reading).
- One question that's easy to answer in a word or a number.
- Blank line, then 3–5 hashtags: #behindthehype plus 2–4 specific ones. No hashtag walls.
- Under 1,000 characters.
Reels also get `youtube_title` (aim for 60 characters or fewer including " #Shorts", search keyword first; lint it with `python3 -I tools/ytkit/title.py --title "..." --thumb "<thumbnail big text>"` and fix every "x" it reports) and `youtube_description` (2–3 lines with the keywords, 3–5 hashtags, "Follow on Instagram @behind.the.hype.in").

## Delivery
1. Push media to this repo under posts/ (public URL: https://raw.githubusercontent.com/hypebehindthe-spec/bth-media/main/posts/<file>).
2. Upload the same files to the dashboard as assets (Artifact tool: action publish, url https://claude.ai/artifact/1woM1FGHPUQU3JzWR7DAr3, asset true, file_path).
3. Write/update the row in the dashboard's "posts" collection (ArtifactData tool). Row: { number, title, type ("Reel"|"Carousel"|"Photo"), status "pending", caption, media [{kind, src "/_blob/..."}] (for reels: the video first, then the thumbnail image so the owner can review both), publish {post_type, media_url | carousel_files, youtube_title, youtube_description, youtube_tags, thumbnail_url (raw GitHub URL of the thumbnail JPEG)}, sources, createdAt }. For a rework: pass if_version, set status "pending", remove "note" with {"__delete__": true}, keep the same number.
4. Never run the Instagram/YouTube publishing scenario yourself — the owner's Approve button does that.
5. Tell the owner in one short message what's ready (SendUserMessage if available). If any step failed, say exactly which.

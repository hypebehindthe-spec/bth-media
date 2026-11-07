# Behind The Hype — production playbook

Read this before making or reworking any post. The owner's notes on a specific post override this file for that post only.

## Brand
- Instagram @behind.the.hype.in · YouTube Shorts @behindthehype_in_speed
- Promise: the story behind everything India is hyped about. Pillars: business of sport (IPL, cricket, F1), gadget economics, viral brands & startups, economics in 60 seconds.
- Language: ALL on-screen text, headlines, captions and YouTube titles/descriptions in clear English. Never write the word "Hinglish" anywhere. The voiceover may drop in an occasional Hindi phrase for flavour, but stays mostly English.
- The owner works at Blinkit: quick-commerce topics use public information only, never insider claims, and never criticise Blinkit's competitors.
- Every number must be confirmed in a reputable source (filings, major business press, official bodies); keep URLs in the row's `sources`. Drop anything you can't verify.

## Visual identity
Python Pillow, fonts in /usr/share/fonts/truetype/google-fonts/ (Poppins-Bold/Medium/Regular). Background #0E1116, accent #FFC72C, text #F5F5F0, secondary #969BA5. Small "BEHIND THE HYPE" label top-left in yellow with a short yellow underline, big bold headline, 90px margins, @behind.the.hype.in at the bottom. Avoid glyphs Poppins lacks (arrows, special symbols); check a render with the Read tool before using it.

## Reels (default format — about 5 of every 7 posts)
Every reel has a voiceover AND original background music. Silent reels are not allowed unless the voice step fails (then say so to the owner).

### Growth rules (from 2026-11-07; the first 3 reels got almost no reach)
- **Short.** 25–35 s (hard max 40). 5–7 beats, 70–100 spoken words. One surprising fact, one twist, one takeaway — cut everything else. Watch-through matters more than completeness.
- **Frame 1 is the hook and the Instagram cover** (the publisher uses frame 0). It must read on its own in under a second: the payoff claim or a tension, e.g. "Same gold. 12% pricier." Never a setup line, never "Today we look at...".
- **Spoken hook = the claim**, said in the first 2 seconds. Rotate hook types day to day: shocking number, "X vs Y", "Why does...?", "Nobody talks about...", "You paid ___ for ___".
- **Pick topics people forward.** Before choosing, ask: would someone send this to a friend or argue about it? Favour money in the viewer's pocket, price comparisons (India vs abroad, then vs now), famous brands, cricketers and films, and things everyone is talking about this week. Plain "news recap" is the weakest choice.
- **Be first.** When a topic is tied to a date (festival, match, launch, results), the post must be ready before or on that day, not after. Say "time-sensitive: approve today" in the owner message.
- **Rotate the ending.** Alternate: "Send this to whoever...", a one-line question that invites a comment, "Follow for a daily breakdown". Don't use the same ending two days running.
- Vary mood and seed every day; never reuse a script.

### Pipeline
1. **Script.** Each beat = one on-screen frame + one spoken line. Conversational and human: contractions, short sentences, a natural reaction now and then ("Wait, it gets better."). On-screen text max 4 short lines per beat: the key number or phrase in big type ("y"/"w"), a short context line ("s" or "W"), source in small grey ("g").
2. **Voice.** Find the Make scenario named "BTH – Voiceover" (Make tool scenarios_list, teamId 3492645; currently id 8424575). Run it once (scenarios_run, responsive true) with:
   - `script`: all spoken lines joined with a blank line between beats (the pauses are used for timing),
   - `style`: a one-line direction, e.g. "Energetic, confident Indian-English male storyteller, like a sharp business YouTuber. Brisk pace, punchy delivery, first line hits hard, light emphasis on numbers.",
   - `file_name`: `post_NNN_vo` (or `post_NNN_vo_v2` for a rework).
   It saves `audio/<file_name>.wav` in this repo through Make's GitHub connection. `git pull --rebase` and use it. Default voice is Sadaltager on gemini-2.5-flash-preview-tts; keep the same voice so the page sounds consistent. If the scenario is missing or fails, check the execution with executions_get-detail once, then fall back to music only and report it.
3. **Timing.** List the pauses (`ffmpeg -i audio/X.wav -af silencedetect=n=-35dB:d=0.2 -f null -`), match them to the sentence ends of each beat, and put the beat boundaries in the spec as `"cuts": [...]`. The automatic matcher is often a beat off; hand-checked cuts keep frames and captions in sync.
4. **Build.** Write `posts/post_NNN.json` (same format as before: out, voice, mood, seed, cuts, beats with `say` + `lines`) and run `python3 tools/bth_reel2.py posts/post_NNN.json`. v2 makes a hook-only first frame (no label, no slide counter, no progress bar), a slowly moving background, lines that pop in one by one, a count-up on the first big yellow number of each later beat (`"count": false` on a beat turns it off), word-by-word captions of the voiceover in the lower third, original music ducked under the voice, 1080x1920 H.264/AAC MP4. The `say` text must match the script sent to the voiceover, beat for beat. (`tools/bth_reel.py` is the old slideshow builder; don't use it for new posts.) Style reference: `posts/post_004_v2.mp4` (never published).
5. Keep reels 25–40 s and under 4.6 MB (Make's free plan refuses files over 5 MB); confirm with ffprobe and ls.
6. Look at frame 0 and 3–4 other frames (stitched side by side) with the Read tool before delivering: hook readable, captions in step with the voice, nothing overlapping.

## YouTube thumbnail and tags (every reel)
- Make a cover with `python3 tools/bth_thumb.py '{"kicker": "...", "big": "...", "sub": "...", "hook": "..."}' posts/post_NNN_thumb.jpg`.
  - kicker: 1–3 word topic tag (e.g. "IPL auction", "UPI record").
  - big: the single most surprising number or claim, 2–4 words; use "|" to split into two lines (e.g. "₹25.2 cr bid|₹18 cr paid").
  - sub: a short curiosity line that makes people want the answer (a question works best).
  - hook: one grey line of context. Look at the result with the Read tool; every fact on it must be in the reel.
- `youtube_tags`: 8–14 comma-separated search phrases people actually type (topic, people/brands, the general niche), always ending with "Behind The Hype,shorts".
- The publishing scenario already sets: public, NOT made for kids, Education category, English (India) audio, embedding allowed, subscribers notified. The AI-content label is off: a stock AI narrator over our own text graphics doesn't need it. Never add realistic AI images or video of real people or events without telling the owner, because those do need the label.

## Stay clear of YouTube's "inauthentic content" rule
YouTube demonetises channels that look mass-produced. Keep every reel clearly original: a researched angle and our own commentary (not just reading facts), varied structure and hooks from day to day, a different music seed and mood, no more than one upload a day, and never reuse a script.

## Format mix
- Reels about 5 of 7 days. Once a week make the reel a "guess the number" (ask on beat 1, reveal on the last beat) to pull comments.
- Once a week a data carousel (Instagram re-shows carousels to people who scrolled past the first slide).
- No quote posts and no AI presenter/character: they look mass-produced and blur what the page is for.

## Carousels / photos
1080x1350 JPEG (quality 92). Carousel 5–8 slides: hook, one idea per slide, takeaway + "Follow @behind.the.hype.in for a new breakdown every day".

## Captions
Instagram search reads captions and on-screen text, so write for search, not hashtags.
- Line 1: the hook, with the words people would search (e.g. "Dhanteras gold price", "IPL auction", "iPhone price India").
- 2–3 short lines of value (the twist and one extra fact that isn't in the reel, to reward reading).
- One question that's easy to answer in a word or a number.
- Blank line, then 3–5 hashtags: #behindthehype plus 2–4 specific ones. No hashtag walls.
- Under 1,000 characters.
Reels also get `youtube_title` (under 70 characters, search keyword first, ends with " #Shorts") and `youtube_description` (2–3 lines with the keywords, 3–5 hashtags, "Follow on Instagram @behind.the.hype.in").

## Delivery
1. Push media to this repo under posts/ (public URL: https://raw.githubusercontent.com/hypebehindthe-spec/bth-media/main/posts/<file>).
2. Upload the same files to the dashboard as assets (Artifact tool: action publish, url https://claude.ai/artifact/1woM1FGHPUQU3JzWR7DAr3, asset true, file_path).
3. Write/update the row in the dashboard's "posts" collection (ArtifactData tool). Row: { number, title, type ("Reel"|"Carousel"|"Photo"), status "pending", caption, media [{kind, src "/_blob/..."}] (for reels: the video first, then the thumbnail image so the owner can review both), publish {post_type, media_url | carousel_files, youtube_title, youtube_description, youtube_tags, thumbnail_url (raw GitHub URL of the thumbnail JPEG)}, sources, createdAt }. For a rework: pass if_version, set status "pending", remove "note" with {"__delete__": true}, keep the same number.
4. Never run the Instagram/YouTube publishing scenario yourself — the owner's Approve button does that.
5. Tell the owner in one short message what's ready (SendUserMessage if available). If any step failed, say exactly which.

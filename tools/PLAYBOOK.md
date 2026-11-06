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

1. **Script.** 7–10 beats. Each beat = one on-screen frame + one spoken line. Spoken lines are conversational and human: contractions, short sentences, a natural reaction now and then ("Wait, it gets better."). 90–130 words total so the reel lands at 35–55 s. Beat 1 is a hook spoken in the first 2 seconds. Last beat: takeaway + "Follow for a new breakdown every day."
2. **Voice.** Find the Make scenario named "BTH – Voiceover" (Make tool scenarios_list, teamId 3492645). Run it once (scenarios_run, responsive true) with:
   - `script`: all spoken lines joined with a blank line between beats (the pauses are used for timing),
   - `style`: a one-line direction, e.g. "Warm, confident Indian-English male storyteller, like a sharp business YouTuber. Natural pace, slight smile, light emphasis on numbers.",
   - `file_name`: `post_NNN_vo` (or `post_NNN_vo_v2` for a rework).
   It saves `audio/<file_name>.wav` in this repo through Make's GitHub connection. `git pull --rebase` and use it. Default voice is Sadaltager on gemini-2.5-flash-preview-tts; keep the same voice so the page sounds consistent. If the scenario is missing or fails, check the execution with executions_get-detail once, then fall back to music only and report it.
3. **Build.** Write a spec file `posts/post_NNN.json` (format in the docstring of `tools/bth_reel.py`: out, voice, mood, seed, and one entry per beat with its spoken line `say` and on-screen `lines`), then run `python3 tools/bth_reel.py posts/post_NNN.json`. It renders the frames in the brand style, times each frame to its spoken line using the pauses in the voiceover, adds a slow push-in, cross-fades and a progress bar, composes original music (`tools/bth_music.py`; moods: drive, chill, bright, dark; use the post number as the seed), ducks the music under the voice and exports a 1080x1920 H.264/AAC MP4. On-screen text should be shorter than the spoken line: the key number or phrase in big type, a short grey line for context. The `say` text must match the script sent to the voiceover, beat for beat.
4. Keep reels 35–58 s (YouTube Shorts must stay under 60 s); check with ffprobe.
5. Look at 2–3 key frames with the Read tool before publishing to the dashboard.

## Carousels / photos
1080x1350 JPEG (quality 92). Carousel 5–8 slides: hook, one idea per slide, takeaway + "Follow @behind.the.hype.in for a new breakdown every day".

## Captions
Hook line, 2–4 short lines of value, a question for comments, blank line, 8–12 hashtags including #behindthehype. Under 2,000 characters. Reels also get `youtube_title` (under 90 characters, ends with " #Shorts") and `youtube_description` (2–4 lines, 3–5 hashtags, "Follow on Instagram @behind.the.hype.in").

## Delivery
1. Push media to this repo under posts/ (public URL: https://raw.githubusercontent.com/hypebehindthe-spec/bth-media/main/posts/<file>).
2. Upload the same files to the dashboard as assets (Artifact tool: action publish, url https://claude.ai/artifact/1woM1FGHPUQU3JzWR7DAr3, asset true, file_path).
3. Write/update the row in the dashboard's "posts" collection (ArtifactData tool). Row: { number, title, type ("Reel"|"Carousel"|"Photo"), status "pending", caption, media [{kind, src "/_blob/..."}], publish {post_type, media_url | carousel_files, youtube_title, youtube_description}, sources, createdAt }. For a rework: pass if_version, set status "pending", remove "note" with {"__delete__": true}, keep the same number.
4. Never run the Instagram/YouTube publishing scenario yourself — the owner's Approve button does that.
5. Tell the owner in one short message what's ready (SendUserMessage if available). If any step failed, say exactly which.

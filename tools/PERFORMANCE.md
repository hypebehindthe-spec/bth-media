# Behind The Hype: performance log

Updated by the daily run on Mondays and Thursdays from the Make "insights" pull. Instagram numbers come from the reel insights; avg watch is in seconds; skip rate is Instagram's "reels skip rate" (the share of viewers who swiped away in the first seconds).

| # | Title | Format | Style | Hook type | Hook score | Length s | IG views | Reach | Avg watch s | Skip rate % | Shares | Saves | YT views | Checked |
|---|-------|--------|-------|-----------|------------|----------|----------|-------|-------------|-------------|--------|-------|----------|---------|
| 002 | KKR bid ₹25.20 crore. Green gets ₹18 crore. Why? | Reel | v1 slideshow | Shocking number + why | – | 48.8 | 123 | 109 | 5.1 | 75.9 | 0 | 0 | 29 | 2026-11-09 (Make insights) |
| 003 | India now moves ₹1 lakh crore a day on UPI | Reel | v1 slideshow | Big number | – | 50.1 | 88 | 84 | 2.5 | 89.2 | 0 | 0 | 11 | 2026-11-09 (Make insights) |
| 004 | ₹60,000 crore on Dhanteras gold. Same amount of gold. | Reel | v1 slideshow | Big number + catch | – | 48.0 | 118 | 102 | 6.4 | 74.5 | 0 | 0 | 16 | 2026-11-09 (Make insights) |
| 005 | Guess: one town makes what % of India's Diwali crackers? | Reel | v2 | Guess the number | – | 39.5 | 120 | 108 | 3.8 | 78.4 | 0 | 0 | 111 | 2026-11-09 (Make insights, only ~19 h old) |

## What's working / what isn't (9 Nov, 4 reels)
- Instagram is flat: every reel lands at 88–123 views, all from cold audiences. Median 119 views, average skip rate 79.5%. Nothing has broken out yet, and no reel has a single share or save.
- First v2 reel (005, guess the number) did not fix the skip problem on Instagram: 78.4% skip and 3.8 s average watch, inside the v1 range (74.5–89.2%). Only ~19 h of data; re-check Thursday.
- YouTube is where 005 moved: 111 views in under a day, about 5x the other Shorts (11–29). Same video, different platform behaviour, as with UPI. Keep YouTube titles keyword-first.
- Best Instagram hold is still the money-in-your-pocket/famous-name topics (004 gold 6.4 s, 002 cricket 5.1 s); the abstract economy number (003 UPI) is worst on every measure.
- From 006 the hook gate scores each spoken hook (tools/ytkit/hookscore.py); log the score here to test whether it predicts skip rate.

## Audience (Instagram, posts 002 and 004, 8 Nov)
- 100% of views from non-followers; 84–86% from the Reels tab, 14–15% from Explore. Instagram is testing every reel on cold audiences, so the first second decides everything.
- Men 94–99%; ages 18–34 make up 85–90% (25–34 slightly ahead on cricket, 18–24 on gold); India 84–88%, small NRI share (US, UK, Canada, Australia).
- Write for young Indian men: cricket, phones and gadgets, money in your pocket, cars and bikes, jobs and salaries, startups and famous brands. Keep language simple and direct.

## Posting time
- 002 and 003 went live at about 1–2 AM IST (approved late at night); 004 at 2:38 PM IST and got the best watch time and lowest skip rate of the three. Not proof on its own, but posting into dead hours wastes the first test audience.
- From 8 Nov, Approve queues a post for 6:47 PM IST (12:47 PM too when there is a backlog or the topic is about today). "Post now" stays available for urgent posts.

## YouTube Shorts
- 23 views in the first 2 days; 74% from the Shorts feed, 13% from YouTube search, 13% from channel pages. Search already brings views, so titles keep their keywords.
- The UPI Short held viewers for 55% of its length on YouTube versus 2 s on Instagram: same video, very different first-second behaviour. Don't judge a topic on Instagram alone.

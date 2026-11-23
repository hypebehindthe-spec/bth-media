# Experiments log

The page is run like a business: one change at a time, decided by numbers, written down. On every learn day (Mon/Thu), fill in the results for running experiments and decide **keep / drop / extend** once an experiment has its minimum number of reels.

**Metrics, in order of importance**
1. Follows from the reel, when the insights data has it (Instagram "follows"; otherwise the change in follower count during the reel's first 48 h).
2. Sends per reach: shares ÷ reach. This is what pushes a reel to non-followers.
3. Skip rate and average watch.
4. Views and reach.

YouTube: subscribers gained (from the channel total) and views at 48 h.

**Baseline (18 Nov, 15 reels):**
- Reach 84–142 per reel.
- Sends per reach about 0.06% (1 share in about 1,650 reached).
- Saves 1 in total.
- Skip rate: last 6 reels about 50%, first 9 about 75%.
- Average watch: last 6 reels 7–11 s.
- YouTube views per Short: median about 99 (range 12–347).
- Followers 1, subscribers 2.

| ID | Started | Hypothesis | Change | Minimum | Status / result |
|---|---|---|---|---|---|
| E1 | 23 Nov | Sport content (F1 and cricket) gets more sends and follows than business-only reels, because fans forward to fans | Mon Cricket Money, Tue F1 Explained | 4 reels each | running. 23 Nov: F1 1/4 (p017: 135 views, 47.2% skip, 8.3 s, 0 shares at 19 h); cricket 0/4 (p019 Cricket Money #1 made today). Baseline: pre-series median 128 views, 0.15% sends/reach |
| E2 | 19 Nov | A named, numbered series with a specific "follow for #N" promise converts better than a generic follow CTA | Every reel from 20 Nov carries a series kicker + promise | 8 reels | running. 23 Nov: 3/8 (p016–p018): 113/135/150 views, skip 68.9/47.2/63.6%, 1 share in 354 reach (0.28% vs 0.15% pre-series). Follows not in the insights data yet |
| E3 | 25 Nov | A 60–90 s deep walk-through (Who Keeps What) beats a 30 s reel on sends and saves despite lower completion | One deep reel a week (Wed) | 3 reels | running |
| E4 | 19 Nov | India's engineering marvels (history) can reach past the test pool, like the 500–900x outliers in scan 4 | Thu India Built This | 4 reels | running. 23 Nov: 1/4. p016 Kailasa 113 views, 68.9% skip, 3.9 s watch, 0 shares, 2 YT views at 85 h: weakest series start (dud) |
| E5 | 22 Nov | Space with an India money angle works for this page | Sun Space Money, alternating weeks | 4 reels | running. 23 Nov: 1/4. p018 150 views, 63.6% skip, 1 share (0.81% sends/reach, best early rate) at 13 h |
| E6 | 19 Nov | Mixing Hindi lines into the English voiceover (on-screen text stays English) lifts watch time and sends; scan 4's 10M-view twin of p013 was in Hindi | Owner approved 19 Nov: every new reel mixes in about 1 Hindi line in 3, accent-checked by transcription | 6 reels vs the last 6 English-only | running. 23 Nov: 2/6 (p016 romanised, p018 Devanagari): skip 68.9/63.6% vs 52.6% avg for the last 6 English-only (p010–p015). Early, and both are test pillars, so not yet a fair read |
| E9 | 19 Nov | Real pictures (Commons/NASA) at the reveal moment lift watch time for history and space | 1–3 photo beats in India Built This / Space Money reels | 4 reels | running. 23 Nov: 2/4 (p016, p018), avg watch 3.9 and 5.7 s vs 9.0 s avg on p013–p015 |
| E7 | 6 Dec | A carousel cheat sheet gets saves | Sunday carousel every second week | 2 posts | planned |
| E8 | — | Profile fixes (name field, bio, pinned three) raise profile-visit → follow conversion | Owner edits the profile once | before/after 7 days | waiting for owner |

## Learn-day notes
- **23 Nov (Mon):** no experiment at its minimum yet, so no decisions. Headline: p014 (restaurant water, pre-series) is the first reel past the test pool (306 views, 255 reach, 303 YT); its "is that legal?" everyday-money pattern goes into the Who Keeps What queue. The two test pillars started below the everyday-money reels on skip and watch; watch whether that holds at reels 2–4 before judging Hindi mix (E6), since E6 and E4/E5 overlap.
- **19 Nov (Thu):** no series reel has numbers yet (p016 India Built This #1 is the first; E2/E4/E6/E9 data starts Monday 23 Nov). Pre-series baseline refreshed from 14 reels: IG median 124 views, sends per reach 0.07% (1 share / 1,535 reach), skip 49.7% on the last 6 vs 75.7% on the first 8, YouTube median 99. No decisions due.

## Ideas not yet scheduled (free only)
- **Collab posts with a small sports/business page.** Instagram shows a collab to both audiences. This needs the owner to accept invites, so it's paused while the owner has no time.
- **Trial reels.** They unlock at 1,000 followers.
- **Gemini second-opinion fact check through Make.** It costs credits, so only add it if an error ships.
- **Long video → Instagram.** A vertical 90–120 s "Part 1" cut of each long video, built from the same section voice files with bth_reel3.py at 720x1280 to stay under 4.6 MB. Try it once the history and F1 long videos start.

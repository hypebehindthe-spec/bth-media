# ytkit (vendored)

`hooks.json`, `hookscore.py` and `title.py` come from Jake Schincariol's youtube-agent-skill
(https://github.com/Jakeschincariol/youtube-agent-skill, MIT, see LICENSE), copied 9 Nov 2026.
Pure Python, no network. Our only change: hookscore.py also counts ₹ amounts and lakh/crore as concrete.

- `python3 tools/ytkit/hookscore.py hooks.txt` ranks hook lines (one per line); `--hook "..."` scores one.
- `python3 tools/ytkit/title.py --title "..." --thumb "..."` lints a YouTube title + thumbnail pairing.
- `hooks.json` holds 21 hook formulas with examples and failure modes.
A low score means look again; a high score is not a promise (the author says so too).

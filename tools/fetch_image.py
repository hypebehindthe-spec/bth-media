"""Fetch free-to-use pictures for reels and long videos, with licence and credit recorded.

Sources (allowed in the owner's claude.ai network settings, 19 Nov 2026):
  nasa     NASA Image and Video Library: public domain (NASA logos/insignia excluded; never imply endorsement)
  commons  Wikimedia Commons: only public domain / CC0 / CC BY / CC BY-SA files are accepted; the credit line
           is written to <out>.credit.txt and must go into the caption/description ("Photo: <author>, <licence>, Wikimedia Commons").

The Commons API often rate-limits this shared workspace (429, retry-after up to ~2 min): search once,
note the exact File: title, then get it; prefer NASA for space. Downloads come from upload.wikimedia.org.

Rules (PLAYBOOK "Real pictures"): places, buildings, objects, machines, maps, space only. NEVER a photo of a
real person (drivers, players, founders, leaders), never team or brand logos. Look at every picture with the
Read tool before using it.

Usage:
  python3 -I tools/fetch_image.py search commons "Kailasa temple Ellora"      # list candidates
  python3 -I tools/fetch_image.py search nasa "Chandrayaan"
  python3 -I tools/fetch_image.py get commons "File:Kailasa temple.jpg" out.jpg
  python3 -I tools/fetch_image.py get nasa PIA12235 out.jpg
"""
import json, sys, time, urllib.parse, urllib.request

UA = "BehindTheHype/1.0 (hypebehindthe@gmail.com)"
FREE = ("public domain", "pd", "cc0", "cc by", "cc-by", "cc by-sa", "cc-by-sa")


def http(url, binary=False, tries=3):
    if binary:   # Wikimedia answers 429 to Python's client but serves curl fine (tested 19 Nov)
        import subprocess
        r = subprocess.run(["curl", "-sfL", "--max-time", "120", "--retry", "3", "--retry-delay", "20",
                            "-A", UA, url], capture_output=True)
        if r.returncode or len(r.stdout) < 2000:
            sys.exit(f"download failed ({r.returncode}): {url}")
        return r.stdout
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
                return data if binary else json.loads(data)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and i < tries - 1:
                wait = min(int(e.headers.get("retry-after") or 10) + 2, 150)
                print(f"rate limited, waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise


def strip(html):
    import re
    return re.sub(r"<[^>]+>", "", html or "").strip()


def _commons(params):
    u = ("https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=url|extmetadata|size"
         "&iiurlwidth=1280&format=json&" + params)
    pages = (http(u).get("query") or {}).get("pages", {}).values()
    out = []
    for p in pages:
        if "imageinfo" not in p:
            continue
        ii = p["imageinfo"][0]
        m = ii.get("extmetadata", {})
        lic = strip(m.get("LicenseShortName", {}).get("value", ""))
        ok = lic.lower().startswith(FREE)
        out.append({"title": p["title"], "licence": lic, "free": ok, "w": ii.get("width"), "h": ii.get("height"),
                    "author": strip(m.get("Artist", {}).get("value", ""))[:80],
                    "desc": strip(m.get("ImageDescription", {}).get("value", ""))[:100],
                    # thumb.wikimedia.org is blocked here; the same path works on upload.wikimedia.org
                    "url": (ii.get("thumburl") or ii["url"]).replace("//thumb.wikimedia.org/", "//upload.wikimedia.org/").split("?")[0],
                    "page": ii.get("descriptionurl")})
    return out


def commons_search(q, n=12):
    return _commons(f"generator=search&gsrnamespace=6&gsrlimit={n}&gsrsearch={urllib.parse.quote(q)}")


def nasa_search(q, n=12):
    u = f"https://images-api.nasa.gov/search?media_type=image&q={urllib.parse.quote(q)}"
    items = http(u)["collection"]["items"][:n]
    out = []
    for it in items:
        d = it["data"][0]
        out.append({"title": d.get("title"), "id": d.get("nasa_id"), "date": (d.get("date_created") or "")[:10],
                    "center": d.get("center"), "desc": (d.get("description") or "")[:100]})
    return out


def get(src, ident, path):
    if src == "commons":
        title = ident if ident.startswith("File:") else "File:" + ident
        res = _commons("titles=" + urllib.parse.quote(title))   # one API call: the Commons API rate-limits this workspace
        if not res:
            sys.exit("not found: " + title)
        r = res[0]
        if not r["free"]:
            sys.exit(f"refused: licence '{r['licence']}' is not public domain / CC0 / CC BY / CC BY-SA")
        open(path, "wb").write(http(r["url"], binary=True))
        credit = f"Photo: {r['author'] or 'unknown'}, {r['licence']}, via Wikimedia Commons ({r['page']})"
    else:
        assets = http(f"https://images-api.nasa.gov/asset/{urllib.parse.quote(ident)}")["collection"]["items"]
        hrefs = [a["href"] for a in assets if a["href"].lower().endswith((".jpg", ".jpeg", ".png"))]
        pick = next((h for h in hrefs if "~large" in h), None) or next((h for h in hrefs if "~orig" in h), hrefs[0])
        open(path, "wb").write(http(pick.replace("http://", "https://"), binary=True))
        credit = f"Image: NASA ({ident}), public domain"
    open(path + ".credit.txt", "w").write(credit + "\n")
    print(path, "|", credit)


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 3:
        sys.exit(__doc__)
    if a[0] == "search":
        rows = commons_search(a[2]) if a[1] == "commons" else nasa_search(a[2])
        for r in rows:
            print(json.dumps(r, ensure_ascii=False))
    elif a[0] == "get":
        get(a[1], a[2], a[3])

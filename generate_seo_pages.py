#!/usr/bin/env python3
"""
Dark Country Boy — Bulk SEO Page Generator
Generates 200+ targeted discovery pages and updates sitemap.xml
"""

import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime

BASE_DIR = '/Users/mac1/Projects/dark-country-boy'
SITE_URL = 'https://thebeautifulsavage.github.io/dark-country-boy'
TODAY = datetime.now().strftime('%Y-%m-%d')

TRACKS = [
    ("A Soldier's Prayer",       "7m1CxPqGPbrdNHqqZPHkAv"),
    ("Appalachian Son",           "0bFkRSvYyZVSPNKpREQJJ2"),
    ("Baptized in Diesel",        "5BqjcgnJ5ZxQW9BNnkMSGa"),
    ("Born to Carry On",          "3yLPXBFhyNqbyFwsYLqsTV"),
    ("Burn What's Broken",        "7AQEt5pKtLJGFZ6yiEf8kS"),
    ("Coal Dust & Communion",     "37vblcq2TsbiwyrxuEPL05"),
    ("Courage Ain't Free",        "1ZRLNRqH72JKELkrmkX9jq"),
    ("Diesel & Grace",            "5Bv0OQKQRnlBddMlneVjl4"),
    ("Don't Let the Fire Die",    "0rklDEU3I6Aovc0FCvEnNO"),
    ("Every Man's War",           "004RJaY1ezaUGmqGfs8HuS"),
]

SPOTIFY_ARTIST = "https://open.spotify.com/artist/4TQMuCjeTbhqvPinWKqRAv"
APPLE_MUSIC = "https://music.apple.com/us/artist/dark-country-boy/1818551005"

CSS = """
    :root{--black:#0a0a0a;--dark:#111111;--ember:#c0392b;--ash:#888888;--white:#e8e8e8;--bone:#d4c5a9}
    *{margin:0;padding:0;box-sizing:border-box}
    body{background:var(--black);color:var(--white);font-family:'Georgia','Times New Roman',serif;line-height:1.6}
    header{position:relative;text-align:center;padding:80px 20px 60px;background:linear-gradient(180deg,#1a0505 0%,var(--black) 100%);border-bottom:1px solid #2a1010}
    header::before{content:'';position:absolute;top:0;left:0;right:0;bottom:0;background:radial-gradient(ellipse at center top,rgba(192,57,43,0.15) 0%,transparent 70%);pointer-events:none}
    .artist-name{font-size:clamp(2rem,8vw,4rem);font-weight:900;letter-spacing:0.05em;text-transform:uppercase;color:var(--white);text-shadow:0 0 40px rgba(192,57,43,0.4)}
    .artist-name span{color:var(--ember)}
    .tagline{margin-top:16px;font-size:1rem;color:var(--bone);letter-spacing:0.15em;text-transform:uppercase;font-style:italic}
    nav{display:flex;justify-content:center;gap:24px;padding:16px;background:var(--dark);border-bottom:1px solid #1f1f1f;flex-wrap:wrap}
    nav a{color:var(--ash);text-decoration:none;font-size:0.8rem;letter-spacing:0.15em;text-transform:uppercase;transition:color 0.2s}
    nav a:hover{color:var(--ember)}
    section{max-width:900px;margin:0 auto;padding:50px 20px}
    h1{font-size:clamp(1.6rem,4vw,2.6rem);color:var(--bone);margin-bottom:24px;line-height:1.2}
    h2{font-size:1.25rem;color:var(--ember);margin:32px 0 14px}
    p{font-size:1.05rem;color:var(--bone);line-height:1.85;margin-bottom:18px}
    .embed-row{margin:12px 0}
    .embed-row iframe{border-radius:12px;width:100%;height:152px;border:none}
    .btn{display:inline-flex;align-items:center;gap:8px;padding:10px 20px;border:1px solid;text-decoration:none;font-size:0.8rem;letter-spacing:0.1em;text-transform:uppercase;transition:all 0.2s;font-family:inherit;margin:6px 6px 0 0}
    .btn-spotify{border-color:#1DB954;color:#1DB954;background:transparent}
    .btn-spotify:hover{background:#1DB954;color:#000}
    .btn-apple{border-color:#fc3c44;color:#fc3c44;background:transparent}
    .btn-apple:hover{background:#fc3c44;color:#fff}
    .links-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px;margin-top:28px}
    .links-grid a{display:block;padding:16px;background:#0f0f0f;border:1px solid #1f1f1f;color:var(--bone);text-decoration:none;transition:border-color 0.2s;font-size:0.9rem}
    .links-grid a:hover{border-color:var(--ember)}
    .links-grid .lbl{font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;color:var(--ember);display:block;margin-bottom:6px}
    footer{text-align:center;padding:40px 20px;border-top:1px solid #1a1a1a;color:var(--ash);font-size:0.8rem}
    footer a{color:var(--ash);text-decoration:none}
    footer a:hover{color:var(--ember)}
"""

SCHEMA = '{"@context":"https://schema.org","@type":"MusicGroup","name":"Dark Country Boy","genre":["dark country","outlaw country","gothic country","americana"],"url":"https://thebeautifulsavage.github.io/dark-country-boy/","sameAs":["https://open.spotify.com/artist/4TQMuCjeTbhqvPinWKqRAv","https://music.apple.com/us/artist/dark-country-boy/1818551005"]}'


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def spotify_embeds(tracks=None):
    if tracks is None:
        tracks = TRACKS
    lines = []
    for name, tid in tracks:
        lines.append(
            f'      <div class="embed-row"><iframe src="https://open.spotify.com/embed/track/{tid}?utm_source=generator" '
            f'allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe></div>'
        )
    return '\n'.join(lines)


def nav_html(extra_links=None):
    base = [
        ('index.html', 'Home'),
        ('dark-country-music.html', 'Dark Country'),
        ('gothic-country-music.html', 'Gothic Country'),
        ('outlaw-country-music.html', 'Outlaw Country'),
        ('dark-country-boy-biography.html', 'Biography'),
        ('links.html', 'Stream'),
    ]
    if extra_links:
        base += extra_links
    items = ''.join(f'<a href="{h}">{t}</a>' for h, t in base)
    return f'  <nav>{items}</nav>'


def footer_html():
    return f"""  <footer>
    <p>Dark Country Boy — Independent Artist</p>
    <p style="margin-top:8px">
      <a href="{SPOTIFY_ARTIST}" target="_blank" rel="noopener">Spotify</a> &nbsp;|&nbsp;
      <a href="{APPLE_MUSIC}" target="_blank" rel="noopener">Apple Music</a> &nbsp;|&nbsp;
      <a href="index.html">Home</a>
    </p>
    <p style="margin-top:8px;font-size:0.7rem">&copy; {datetime.now().year} Dark Country Boy. All rights reserved.</p>
  </footer>"""


def page(filename, title, meta_desc, h1_text, tagline, body_html, og_title=None, og_desc=None, extra_nav=None):
    og_title = og_title or title
    og_desc = og_desc or meta_desc
    canonical = f"{SITE_URL}/{filename}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{meta_desc}">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <link rel="canonical" href="{canonical}">
  <script type="application/ld+json">{SCHEMA}</script>
  <style>{CSS}</style>
</head>
<body>
  <header>
    <div class="artist-name">Dark <span>Country</span> Boy</div>
    <div class="tagline">{tagline}</div>
  </header>
{nav_html(extra_nav)}
  <section>
    <h1>{h1_text}</h1>
{body_html}
  </section>
{footer_html()}
</body>
</html>"""


# ─── Track IDs map ────────────────────────────────────────────────────────────
TRACK_MAP = {t[0]: t[1] for t in TRACKS}

# ─── Related links helper ────────────────────────────────────────────────────
GENRE_LINKS = [
    ('dark-country-music.html', 'Dark Country Music'),
    ('gothic-country-music.html', 'Gothic Country'),
    ('outlaw-country-music.html', 'Outlaw Country'),
    ('southern-gothic-music.html', 'Southern Gothic'),
    ('dark-americana-music.html', 'Dark Americana'),
    ('veteran-country-music.html', 'Veteran Country'),
    ('delta-blues-modern.html', 'Modern Delta Blues'),
    ('dark-country-blues.html', 'Dark Country Blues'),
]


def related_links_html(links=None):
    if links is None:
        links = GENRE_LINKS[:6]
    items = ''.join(
        f'<a href="{h}"><span class="lbl">Explore</span>{t}</a>'
        for h, t in links
    )
    return f'    <h2>Explore More Dark Country</h2>\n    <div class="links-grid">{items}</div>'


PAGES = []  # list of (filename, html_content)


def emit(filename, html):
    PAGES.append((filename, html))


###############################################################################
# CATEGORY 1: ARTIST COMPARISON PAGES
###############################################################################

ARTISTS = [
    # (display_name, slug, description_blurb, sonic_traits)
    ("Jason Isbell", "jason-isbell", "Jason Isbell built his reputation on devastating honesty — songs that cut through the noise of radio country and land like a fist to the chest.",
     ["Literary lyric depth", "Southern roots authenticity", "Acoustic and electric balance", "Unflinching personal storytelling"]),
    ("Sturgill Simpson", "sturgill-simpson", "Sturgill Simpson tore up the Nashville rulebook and wrote his own. His music roams from outlaw country to psychedelic soul, always refusing the easy path.",
     ["Genre-defying boldness", "Outlaw spirit", "Baritone vocal authority", "Anti-commercial attitude"]),
    ("Hank Williams III", "hank-williams-iii", "Hank III carries the darkest flame in the Williams bloodline — a hellbilly howl that splits the difference between classic honky-tonk and underground metal.",
     ["Hellbilly ferocity", "Old-school honky-tonk roots", "Dark rebellious energy", "Vocal grit and power"]),
    ("Cody Jinks", "cody-jinks", "Cody Jinks emerged from the Texas underground to prove that real country — the kind with weight and honesty — still has an audience.",
     ["Texas country authenticity", "Working-class themes", "Powerful baritone", "Independent ethos"]),
    ("Whitey Morgan", "whitey-morgan", "Whitey Morgan channels Waylon and Merle through a Flint, Michigan lens — hard-living country with a working-class core and a barroom soul.",
     ["Classic outlaw country sound", "Midwest grit", "Honky-tonk authenticity", "Whiskey-soaked delivery"]),
    ("Waylon Jennings", "waylon-jennings", "Waylon Jennings defined outlaw country — taking Nashville's slick production and replacing it with raw swagger and unapologetic truth.",
     ["Outlaw country pioneer", "Iconic baritone", "Rebellious anti-Nashville spirit", "Acoustic and electric mastery"]),
    ("Johnny Cash", "johnny-cash", "Johnny Cash's voice carried the weight of every sinner, soldier, and outcast who ever walked a hard road. His music is the dark foundation all serious country builds on.",
     ["Iconic dark baritone", "Storytelling gravitas", "Outlaw and spiritual duality", "Timeless American mythology"]),
    ("Townes Van Zandt", "townes-van-zandt", "Townes Van Zandt is country music's greatest tragic poet — a songwriter who traded commercial success for uncommon artistic truth.",
     ["Poetic lyrical depth", "Minimalist folk-country", "Emotional devastation", "Songwriter's songwriter"]),
    ("John Prine", "john-prine", "John Prine's songs are deceptively simple — plain language carrying unbearable weight. He wrote the truth about regular people and it hit like a freight train.",
     ["Plain-spoken profundity", "Working-class empathy", "Acoustic storytelling", "Dark humor and sorrow"]),
    ("Gillian Welch", "gillian-welch", "Gillian Welch conjures the ghost of old Appalachian music — stark, beautiful, and haunted by time. Her music sounds like something unearthed, not written.",
     ["Appalachian folk tradition", "Sparse haunting arrangements", "Old-time authenticity", "Gothic atmosphere"]),
    ("Amigo the Devil", "amigo-the-devil", "Amigo the Devil turns murder ballads and dark philosophy into intimate confession — fingerpicked guitar under bloodstained folk lyrics.",
     ["Murder ballad tradition", "Dark folk intimacy", "Acoustic noir", "Cult underground appeal"]),
    ("Murder by Death", "murder-by-death", "Murder by Death builds gothic country epics — sweeping songs about outlaws, redemption, and the thin line between salvation and damnation.",
     ["Gothic country rock", "Cinematic scope", "Dark orchestral arrangements", "Storytelling ambition"]),
    ("16 Horsepower", "16-horsepower", "16 Horsepower dug deep into Southern Gothic soil and pulled out something sacred and terrifying — country music filtered through biblical dread.",
     ["Southern Gothic intensity", "Banjo and accordion darkness", "Spiritual and sinister", "Post-punk country fusion"]),
    ("Wovenhand", "wovenhand", "Wovenhand — the spiritual evolution of 16 Horsepower — creates devotional music that feels like a sermon delivered from the edge of the earth.",
     ["Dark devotional folk", "Hypnotic rhythmic intensity", "Biblical darkness", "Unique sonic landscape"]),
    ("William Elliott Whitmore", "william-elliott-whitmore", "William Elliott Whitmore sounds like a man born a century too late — raw blues and old country delivered with startling emotional power.",
     ["Raw solo blues-country", "Weathered emotional honesty", "Minimalist acoustic power", "Working-class roots"]),
    ("Chuck Ragan", "chuck-ragan", "Chuck Ragan brought punk rock intensity to acoustic Americana — the rawness of hardcore with the heart of traditional country.",
     ["Punk-to-folk authenticity", "Acoustic intensity", "Working-class perspective", "Ragged emotional delivery"]),
    ("Roger Alan Wade", "roger-alan-wade", "Roger Alan Wade is the outlaw's outlaw — a Kentucky songwriter whose unflinching songs make Nashville look like a theme park.",
     ["Raw outlaw country", "Kentucky authenticity", "Uncompromising writing", "Underground cult status"]),
    ("David Allan Coe", "david-allan-coe", "David Allan Coe lived the outlaw country life before it was a brand — a genuine outsider whose best songs carry real darkness and real beauty.",
     ["Original outlaw country", "Dark storytelling", "Road-worn authenticity", "Rebel spirit"]),
    ("Steve Earle", "steve-earle", "Steve Earle is one of the great American songwriters — a man who channeled addiction, politics, and hard living into urgent, real music.",
     ["Literary songwriting", "Political consciousness", "Roots rock country", "Survivor's honesty"]),
    ("Lucinda Williams", "lucinda-williams", "Lucinda Williams writes about love and loss with a rawness that commercial country can't touch — her music bleeds.",
     ["Raw emotional honesty", "Southern roots", "Americana authenticity", "Unpolished power"]),
    ("Drive-By Truckers", "drive-by-truckers", "Drive-By Truckers tackle the contradictions of Southern identity with intelligence and volume — rock and roll that doesn't flinch.",
     ["Southern rock-country", "Political and personal depth", "Multi-songwriter perspective", "Loud and literary"]),
    ("Ryan Bingham", "ryan-bingham", "Ryan Bingham grew up hard and writes hard — country and rock colliding in songs about roads, dust, and survival.",
     ["Texas Americana", "Raspy vocal intensity", "Road-weary authenticity", "Country-rock energy"]),
    ("Turnpike Troubadours", "turnpike-troubadours", "The Turnpike Troubadours created a red dirt country sound that felt genuinely urgent — music about Oklahoma life that transcended its region.",
     ["Red dirt country", "Oklahoma authenticity", "Literary songwriting", "Fiddle-driven energy"]),
    ("Reckless Kelly", "reckless-kelly", "Reckless Kelly refined the Texas Americana sound into something polished but never soft — big hooks with real country roots.",
     ["Texas Americana", "Strong songwriting craft", "Country-rock balance", "Independent spirit"]),
    ("Robert Earl Keen", "robert-earl-keen", "Robert Earl Keen is a Texas institution — his darkly funny, brilliantly observed country songs define a certain kind of American truth.",
     ["Texas storytelling", "Dark humor", "Acoustic country craft", "Road song mastery"]),
    ("Ray Wylie Hubbard", "ray-wylie-hubbard", "Ray Wylie Hubbard found his greatest powers late — his recent records are dark, swampy, and full of snake-handler wisdom.",
     ["Texas swamp blues-country", "Dark spiritual themes", "Late-career brilliance", "Guitar snake-bite riffs"]),
    ("Butch Walker", "butch-walker", "Butch Walker channels heartland rock and country into arena-worthy songs that never sacrifice emotion for polish.",
     ["Heartland rock country", "Big melodic hooks", "Personal storytelling", "Rock and country fusion"]),
    ("Todd Snider", "todd-snider", "Todd Snider is the anti-folk country philosopher — rambling songs full of wit, darkness, and working-class solidarity.",
     ["Folk-country wit", "Political observation", "Storytelling humor", "Outsider perspective"]),
    ("Hayes Carll", "hayes-carll", "Hayes Carll writes country songs with literary ambition and a Texas sense of humor — dark and funny in equal measure.",
     ["Texas country-folk", "Witty storytelling", "Dark themes", "Acoustic authenticity"]),
    ("James McMurtry", "james-mcmurtry", "James McMurtry writes the definitive songs about American decline and rural struggle — stark, precise, and devastating.",
     ["Rural American realism", "Sparse Americana", "Political depth", "Literary precision"]),
    ("Billy Joe Shaver", "billy-joe-shaver", "Billy Joe Shaver wrote songs for Waylon, Willie, and half the outlaw country canon — his own records are rough diamonds.",
     ["Outlaw country pioneer", "Gospel and honky-tonk", "Texas legend", "Raw authenticity"]),
    ("Kris Kristofferson", "kris-kristofferson", "Kris Kristofferson proved that country songwriting could carry the weight of poetry — his songs are still the standard.",
     ["Poetic songwriting standard", "Outlaw country foundation", "Literary depth", "Timeless themes"]),
    ("Merle Haggard", "merle-haggard", "Merle Haggard sang the working man's blues with more dignity and skill than anyone before or since — the real deal.",
     ["Classic country authenticity", "Working-class voice", "Bakersfield sound", "Vocal mastery"]),
    ("Willie Nelson", "willie-nelson", "Willie Nelson's music is American mythology — jazz-inflected country phrasing wrapped around songs that span decades and genres.",
     ["Outlaw country legend", "Jazz-country phrasing", "Timeless storytelling", "Eternal relevance"]),
    ("Dwight Yoakam", "dwight-yoakam", "Dwight Yoakam brought Bakersfield back to life — raw, twangy, and rhythmically alive in a way that polished Nashville never was.",
     ["Bakersfield sound", "Honky-tonk energy", "Sharp rhythmic style", "Classic country revival"]),
    ("BR5-49", "br5-49", "BR5-49 dug up classic honky-tonk from the archives and played it like their lives depended on it — roots country at its most vital.",
     ["Classic honky-tonk revival", "Retro authenticity", "Garage country energy", "Roots music dedication"]),
    ("Old Crow Medicine Show", "old-crow-medicine-show", "Old Crow Medicine Show breathed life into old-time string band music — raw, community-driven, and deeply rooted in American folk tradition.",
     ["Old-time string band", "Community folk energy", "Traditional authenticity", "Roots music vitality"]),
    ("Steep Canyon Rangers", "steep-canyon-rangers", "The Steep Canyon Rangers carry the bluegrass tradition forward with skill and grace — instrumental mastery in service of great songs.",
     ["Bluegrass excellence", "Instrumental depth", "Traditional roots", "Mountain music authenticity"]),
    ("Trampled by Turtles", "trampled-by-turtles", "Trampled by Turtles play bluegrass at punk tempos — frenetic energy and dark themes delivered on acoustic instruments.",
     ["High-speed bluegrass intensity", "Dark folk themes", "Acoustic power", "Minnesota originality"]),
    ("The Avett Brothers", "the-avett-brothers", "The Avett Brothers fuse folk, bluegrass, and indie rock into emotionally overwhelming music — raw vulnerability as artistic strategy.",
     ["Folk-bluegrass-rock fusion", "Emotional vulnerability", "Acoustic power", "Brother harmony depth"]),
    ("Lucero", "lucero", "Lucero distills the best of Southern rock and country punk into anthems for the heartbroken and road-worn.",
     ["Country punk energy", "Southern rock roots", "Bar-room anthems", "Emotional directness"]),
    ("American Aquarium", "american-aquarium", "American Aquarium writes hard country about hard lives — recovery, regret, and the long road through the American South.",
     ["Hard country realism", "Recovery and redemption themes", "Southern authenticity", "Emotional honesty"]),
    ("Possessed by Paul James", "possessed-by-paul-james", "Possessed by Paul James creates one-man-band roots music of startling intensity — old-time, blues, and country fused by raw human energy.",
     ["One-man roots intensity", "Old-time blues country fusion", "Primitive power", "Underground authenticity"]),
    ("Tom Waits", "tom-waits-fans", "Tom Waits fans understand that the most powerful music lives in the dark margins — carnival noir, hobo blues, and the poetry of the dispossessed.",
     ["Carnival noir atmosphere", "Dark literary songwriting", "Experimental blues", "Outsider art philosophy"]),
]


for display, artist_slug, intro, traits in ARTISTS:
    filename = f"if-you-like-{artist_slug}.html"
    trait_items = ''.join(f'<li>{t}</li>' for t in traits)
    track_links = ''.join(
        f'<a href="{slug(n)}-dark-country-boy.html"><span class="lbl">Song</span>{n}</a>'
        for n, _ in TRACKS
    )
    related = [
        ('dark-country-music.html', 'Dark Country Music'),
        ('gothic-country-music.html', 'Gothic Country'),
        ('outlaw-country-music.html', 'Outlaw Country'),
        ('southern-gothic-music.html', 'Southern Gothic'),
        ('dark-americana-music.html', 'Dark Americana'),
        ('dark-country-boy-biography.html', 'About the Artist'),
    ]
    rel_items = ''.join(
        f'<a href="{h}"><span class="lbl">Explore</span>{t}</a>'
        for h, t in related
    )

    body = f"""    <p>{intro}</p>
    <p>Dark Country Boy occupies that same uncompromising territory — music that refuses to soften its edges, sanitize its stories, or bow to commercial pressure. If {display}'s work resonates with you, you'll find a kindred spirit in Dark Country Boy's catalog of ten stark, powerful tracks.</p>

    <h2>What They Share</h2>
    <ul style="list-style:none;margin:0 0 20px 0">
{trait_items}
    </ul>

    <h2>Dark Country Boy: The Sound</h2>
    <p>Dark Country Boy draws from the same wellspring that feeds the best of American roots music — Delta blues, Appalachian folk, outlaw country, and Southern Gothic storytelling. The songs deal in the real currency of the genre: hard work, harder living, survival, faith tested by fire, and the American landscape at its most raw and beautiful.</p>
    <p>Where mainstream country smooths and polishes, Dark Country Boy leaves the rough edges. Where Nashville chases trends, this music looks backward and inward — finding the timeless in the traditional, the universal in the specific.</p>

    <h2>Stream the Catalog</h2>
    <p>Ten tracks. No filler. Listen now on Spotify:</p>
{spotify_embeds()}

    <h2>Songs from Dark Country Boy</h2>
    <div class="links-grid">{track_links}</div>

    <h2>Stream & Support</h2>
    <p>
      <a href="{SPOTIFY_ARTIST}" class="btn btn-spotify" target="_blank" rel="noopener">&#9654; Spotify</a>
      <a href="{APPLE_MUSIC}" class="btn btn-apple" target="_blank" rel="noopener">&#9654; Apple Music</a>
    </p>

    <h2>More to Explore</h2>
    <div class="links-grid">{rel_items}</div>"""

    html = page(
        filename=filename,
        title=f"If You Like {display}, You'll Love Dark Country Boy",
        meta_desc=f"Fans of {display} who love raw, authentic roots music will find a natural home in Dark Country Boy's dark country and outlaw blues catalog. Stream all 10 tracks free.",
        h1_text=f"If You Like {display}, You'll Love Dark Country Boy",
        tagline=f"For Fans of {display}",
        body_html=body,
    )
    emit(filename, html)


###############################################################################
# CATEGORY 2: SONG PAGES
###############################################################################

SONG_DESCRIPTIONS = {
    "A Soldier's Prayer": {
        "desc": "A Soldier's Prayer is a raw, unflinching meditation on war, faith, and the weight soldiers carry home. Built on sparse guitar and bone-deep vocals, it captures the spiritual reckoning that combat forces on every fighting man.",
        "themes": ["Veteran experience", "Faith under fire", "The weight of war", "Prayer and survival"],
        "mood": "haunting, reverent, devastating",
    },
    "Appalachian Son": {
        "desc": "Appalachian Son is a love letter and a lament — the story of a man shaped by mountains, coal dust, and generations of hard living. It captures the fierce pride and quiet sorrow of Appalachian identity.",
        "themes": ["Appalachian heritage", "Family legacy", "Mountain identity", "Pride and poverty"],
        "mood": "proud, melancholic, rooted",
    },
    "Baptized in Diesel": {
        "desc": "Baptized in Diesel is working-class country at its most elemental — the smell of oil and grease as a sacrament, hard labor as a form of grace. It's a song for every man who found meaning in honest work.",
        "themes": ["Working class life", "Blue collar identity", "Labor as religion", "Truck culture"],
        "mood": "gritty, reverent, muscular",
    },
    "Born to Carry On": {
        "desc": "Born to Carry On is a song about survival instinct — the stubborn, unreasonable refusal to quit that defines certain kinds of people. It's an anthem for the battered but unbroken.",
        "themes": ["Resilience", "Survival", "Determination", "Working through pain"],
        "mood": "defiant, powerful, uplifting",
    },
    "Burn What's Broken": {
        "desc": "Burn What's Broken confronts the necessity of destruction before renewal — burning away the past to make room for what can grow. A dark country meditation on transformation through fire.",
        "themes": ["Transformation", "Letting go", "Destruction and rebirth", "Moving forward"],
        "mood": "cathartic, dark, powerful",
    },
    "Coal Dust & Communion": {
        "desc": "Coal Dust & Communion marries the sacred and the earthly — finding God in the dark places where men work the earth for coal. It's the spiritual soundtrack to a vanishing American way of life.",
        "themes": ["Mining heritage", "Appalachian spirituality", "Sacred and profane", "Community"],
        "mood": "sacred, dusty, haunting",
    },
    "Courage Ain't Free": {
        "desc": "Courage Ain't Free reckons with the price of bravery — what it costs to stand up, ship out, and carry the weight of choices made in extreme circumstances. A veteran's truth delivered without sentiment.",
        "themes": ["Military service", "The cost of bravery", "Veteran truth", "Sacrifice"],
        "mood": "stark, honest, unflinching",
    },
    "Diesel & Grace": {
        "desc": "Diesel & Grace finds religion on the American highway — the long haul as a kind of spiritual practice, the road as both escape and pilgrimage. A country song about movement as meaning.",
        "themes": ["Road life", "Trucking culture", "Spiritual journey", "American highway mythology"],
        "mood": "rolling, contemplative, vast",
    },
    "Don't Let the Fire Die": {
        "desc": "Don't Let the Fire Die is a rallying cry against spiritual and creative extinction — keep the old ways alive, keep the real music burning, don't let what matters get swallowed by the noise.",
        "themes": ["Musical heritage", "Keeping traditions alive", "Cultural preservation", "Fighting complacency"],
        "mood": "urgent, passionate, defiant",
    },
    "Every Man's War": {
        "desc": "Every Man's War zooms out from individual experience to the universal — every soldier's conflict, every working man's daily battle, the war of existence itself. Sweeping in scope, intimate in delivery.",
        "themes": ["Universal struggle", "War and peace", "Human conflict", "Solidarity"],
        "mood": "epic, heavy, unifying",
    },
}

for track_name, track_id in TRACKS:
    filename = f"{slug(track_name)}-dark-country-boy.html"
    info = SONG_DESCRIPTIONS.get(track_name, {})
    desc_text = info.get("desc", f"{track_name} is a dark country track from Dark Country Boy — raw, honest, and rooted in the American tradition.")
    themes = info.get("themes", ["Dark country", "Americana", "Roots music"])
    mood = info.get("mood", "raw, honest, powerful")
    theme_items = ''.join(f'<li>{t}</li>' for t in themes)

    # related songs
    other_tracks = [(n, i) for n, i in TRACKS if n != track_name]
    song_links = ''.join(
        f'<a href="{slug(n)}-dark-country-boy.html"><span class="lbl">Track</span>{n}</a>'
        for n, _ in other_tracks[:6]
    )

    body = f"""    <p>{desc_text}</p>
    <p>Mood: <em>{mood}</em></p>

    <h2>Themes</h2>
    <ul style="list-style:none;margin:0 0 20px 0">
{theme_items}
    </ul>

    <h2>Listen on Spotify</h2>
    <div class="embed-row">
      <iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/{track_id}?utm_source=generator" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    </div>

    <h2>Full Dark Country Boy Catalog</h2>
    <p>Ten tracks of uncompromising dark country, outlaw blues, and Southern Gothic Americana. No filler.</p>
{spotify_embeds()}

    <h2>Stream & Support</h2>
    <p>
      <a href="{SPOTIFY_ARTIST}" class="btn btn-spotify" target="_blank" rel="noopener">&#9654; Follow on Spotify</a>
      <a href="{APPLE_MUSIC}" class="btn btn-apple" target="_blank" rel="noopener">&#9654; Apple Music</a>
    </p>

    <h2>More Songs</h2>
    <div class="links-grid">{song_links}</div>"""

    html = page(
        filename=filename,
        title=f"{track_name} by Dark Country Boy — Dark Country & Outlaw Blues",
        meta_desc=f"Stream '{track_name}' by Dark Country Boy — {desc_text[:120]}... Raw dark country and outlaw blues.",
        h1_text=f"{track_name} — Dark Country Boy",
        tagline=f"Dark Country · Outlaw Blues · Americana",
        body_html=body,
    )
    emit(filename, html)


###############################################################################
# CATEGORY 3: GENRE / KEYWORD LANDING PAGES
###############################################################################

GENRE_PAGES = [
    # (filename, title, h1, tagline, meta_desc, body_paragraphs)
    ("outlaw-country-artists-2026.html",
     "Best Outlaw Country Artists 2026 | Dark Country & Americana Underground",
     "Best Outlaw Country Artists of 2026",
     "Outlaw Country · Underground · Real",
     "Discover the best outlaw country artists of 2026, including Dark Country Boy — raw, authentic, and unapologetically outside Nashville's mainstream.",
     ["The outlaw country tradition never died — it just moved underground. While mainstream country filled arenas with polished pop dressed in boots and hats, the real outlaws kept playing in bars, recording in home studios, and releasing music on their own terms.",
      "In 2026, the underground outlaw country scene is more vital than ever. Artists like Dark Country Boy are carrying the torch lit by Waylon Jennings, Johnny Cash, and David Allan Coe — music that deals in truth, not trends.",
      "Dark Country Boy's ten tracks represent outlaw country in its purest modern form: raw production, uncompromising lyrics, and a sound rooted in Delta blues and Appalachian tradition. Songs like 'Burn What's Broken' and 'Every Man's War' would sit comfortably beside the classic outlaw catalog.",
      "The new outlaws aren't rebels for the sake of rebellion. They're artists committed to making music that means something — songs about real work, real struggle, real faith, and real America. That's the tradition Dark Country Boy upholds."]),

    ("military-country-music.html",
     "Military Country Music 2026 | Songs for Veterans & Service Members",
     "Military Country Music — Songs That Honor Service",
     "Veteran · Military · Country · Americana",
     "Military country music for veterans and service members — Dark Country Boy's catalog includes powerful songs about soldiering, sacrifice, and the weight of service.",
     ["Military country music occupies a unique space — songs that understand what service actually looks and feels like, not the polished patriotism of radio. Real military country is about sacrifice, PTSD, the difficulty of coming home, and the brotherhood forged in extreme circumstances.",
      "Dark Country Boy brings authentic veteran perspective to dark country and outlaw blues. Tracks like 'A Soldier's Prayer,' 'Courage Ain't Free,' and 'Every Man's War' are written from the inside — the kind of songs that resonate with anyone who's worn a uniform.",
      "'A Soldier's Prayer' is a meditation on faith in combat — the raw, unpolished prayer of a soldier in the field. 'Courage Ain't Free' reckons with the real cost of bravery. These aren't flag-waving anthems; they're honest documents of what service demands.",
      "For veterans looking for music that understands them, Dark Country Boy's catalog offers something rare: authenticity. This music doesn't sanitize the military experience or exploit it for commercial appeal. It honors it with unflinching honesty."]),

    ("alt-country-music-2026.html",
     "Alt Country Music 2026 | Best Alternative Country Artists & Songs",
     "Alt Country Music in 2026 — The Underground Keeps Burning",
     "Alt Country · Americana · Roots Rock",
     "The best alt country music of 2026 — from the underground Americana tradition to dark country outliers like Dark Country Boy.",
     ["Alternative country was born from frustration — the frustration of artists who loved the traditions of country music but couldn't stomach what Nashville had done to them. In the mid-1980s and 1990s, bands like Uncle Tupelo, Whiskeytown, and Lucinda Williams created a counter-tradition that valued authenticity over airplay.",
      "That tradition continues in 2026 through artists operating entirely outside the mainstream. Dark Country Boy represents the darker end of the alt country spectrum — less twang, more blues; less nostalgia, more raw confrontation with American realities.",
      "The alt country of 2026 is defined by its independence. Artists self-release, build audiences directly, and refuse to compromise for playlist placement. Dark Country Boy's ten-track catalog exemplifies this approach — raw, self-determined, and uncompromising.",
      "If you found your way to alt country through Wilco, Ryan Adams, or Gillian Welch, Dark Country Boy's blend of Southern Gothic imagery, Delta blues guitar, and outlaw country storytelling offers a logical and rewarding next step."]),

    ("insurgent-country-music.html",
     "Insurgent Country Music | No Depression, Anti-Nashville Underground",
     "Insurgent Country — The Underground Tradition",
     "No Depression · Anti-Nashville · Real Country",
     "Insurgent country music — the anti-Nashville underground tradition that kept real country alive. Dark Country Boy carries that torch.",
     ["'Insurgent country' was the term critics used for the wave of anti-Nashville acts that emerged in the late 1980s and early 1990s — bands playing raw, roots-based music that the mainstream had abandoned. The genre had no commercial infrastructure; it ran on zines, college radio, and word of mouth.",
      "The insurgent spirit never disappeared. It just evolved. Today's insurgents are artists who operate in the spaces mainstream country ignores — building catalogs of real songs for real people, distributed through streaming platforms without record label intermediaries.",
      "Dark Country Boy is insurgent country for 2026 — ten tracks of dark, roots-deep music that would fit equally well in a Delta juke joint, an Appalachian church, or a dark city bar. The production is raw because raw is honest. The lyrics are unsparing because the truth demands it.",
      "The insurgent tradition lives in the refusal to smooth the edges. Dark Country Boy's music maintains that refusal — keeping faith with the listeners who need music that tells the truth."]),

    ("no-depression-music.html",
     "No Depression Music | Roots Country & Americana Underground Artists",
     "No Depression — Roots Country Lives Underground",
     "No Depression · Roots Country · Americana",
     "No Depression roots country and Americana — the underground tradition that refuses to compromise. Dark Country Boy is the sound of real American music.",
     ["No Depression — named after the Carter Family song that Uncle Tupelo repurposed as an album title — became the rallying cry for a generation of roots country artists who found no home in mainstream Nashville. The movement valued tradition, honesty, and craft over commercial calculation.",
      "The No Depression ethos shaped a generation of listeners who demanded more from their country music. Those listeners grew up, stayed discerning, and continue to seek out artists who share the commitment to authentic roots music.",
      "Dark Country Boy writes directly into that tradition. The influence of classic country, Delta blues, and Appalachian folk is audible in every track — not as pastiche but as genuine inheritance. This is music that knows where it comes from and honors that lineage.",
      "For the No Depression crowd — people who grew up on Whiskeytown, Son Volt, Gillian Welch, and Townes Van Zandt — Dark Country Boy's catalog offers something genuine in a landscape full of pretenders."]),

    ("roots-music-2026.html",
     "Roots Music 2026 | Best Americana & Folk Country Artists",
     "Roots Music in 2026 — Authentic American Sound",
     "Roots Music · Folk · Country · Blues",
     "The best roots music of 2026 — authentic Americana, folk country, and blues from independent artists like Dark Country Boy.",
     ["Roots music is the umbrella under which everything real in American popular music shelters — country, blues, folk, gospel, Cajun, bluegrass, old-time. It's music that knows its origins and honors them, even while pushing forward.",
      "In 2026, roots music thrives in the margins. Artists with deep knowledge of American musical tradition are recording independently and building audiences without major label support. The gatekeepers have changed; the music's integrity hasn't.",
      "Dark Country Boy brings roots music sensibility to dark country — drawing from Delta blues guitar traditions, outlaw country lyric approaches, and the stark storytelling of Appalachian folk. The result is music that sounds both old and urgently present.",
      "The ten tracks in the Dark Country Boy catalog represent roots music at its most concentrated — no production flourishes to hide behind, no genre-crossing to broaden appeal. Just the essential ingredients: voice, guitar, and truth."]),

    ("americana-music-underground.html",
     "Underground Americana Music | Independent Roots Artists 2026",
     "Underground Americana — Where Real Roots Music Lives",
     "Underground Americana · Independent · Real",
     "Discover underground Americana music and independent roots artists — the anti-mainstream tradition that keeps real American music alive in 2026.",
     ["Underground Americana exists in the spaces between genre labels — too dark for traditional country, too rooted for indie folk, too honest for mainstream Americana. It's the music that falls through the cracks of the algorithm and finds its audience through genuine connection.",
      "Dark Country Boy operates entirely in this underground — self-released, streaming-native, built on the strength of the songs themselves. There's no marketing machine, no radio campaign, no playlist strategy. Just ten tracks and the listeners who find them.",
      "The underground Americana tradition includes artists like Possessed by Paul James, Amigo the Devil, William Elliott Whitmore, and Roger Alan Wade — artists who prioritize truth over access. Dark Country Boy belongs in that company.",
      "Finding underground Americana means digging past the algorithmic surface. It means following your ears past the curated playlists into the territory where artists make music because they have to, not because they've calculated its commercial potential."]),

    ("red-dirt-country-music.html",
     "Red Dirt Country Music | Oklahoma & Texas Roots Underground",
     "Red Dirt Country — Roots and Grit from the Southern Plains",
     "Red Dirt · Texas · Oklahoma · Authentic Country",
     "Red dirt country music — the Texas-Oklahoma roots tradition that kept authentic country alive. Fans of red dirt will find common ground in Dark Country Boy.",
     ["Red dirt country emerged from the Oklahoma-Texas corridor in the 1970s and 1980s as a response to Nashville's homogenization. Artists like Tom Skinner, Bob Childers, and the Turnpike Troubadours created a regional sound defined by honest lyrics, hard touring, and zero compromise.",
      "The red dirt tradition is about place and authenticity — songs that could only come from someone who knows what the Southern Plains look and feel like. It's country music with dirt under its fingernails and calluses on its hands.",
      "While Dark Country Boy comes from a different geographic tradition — more Appalachian than Oklahoman — the values overlap completely. Hard work, honest living, and music that refuses to fake it. Red dirt fans will recognize the ethos immediately.",
      "Red dirt country built its audience the hard way: constant touring, word of mouth, and music good enough to make people drive three hours to a bar show. Dark Country Boy is available digitally, but the same quality that drives red dirt loyalty is present in every track."]),

    ("texas-country-music-underground.html",
     "Texas Country Music Underground | Independent Texas Artists 2026",
     "Texas Country Underground — Real Music Below the Mainstream",
     "Texas Country · Underground · Independent",
     "Texas country music underground — the independent roots tradition that gave us Waylon, Willie, Ryan Bingham, and more. Dark Country Boy occupies the same territory.",
     ["Texas has its own country music ecosystem — separate from Nashville, resistant to its formulas, and consistently producing artists of uncommon quality. From the original outlaw era through the red dirt movement to today's streaming-era independents, Texas country keeps finding new ways to be authentic.",
      "The Texas country underground values a specific set of things: lyrical honesty, instrumental skill, hard touring, and zero tolerance for fakery. Artists earn their audiences by delivering night after night, song after song.",
      "Dark Country Boy draws from the same well as Texas country's best — the outlaw tradition, the blues influence, the working-class perspective, and the willingness to deal with darkness rather than paper over it. The Texas underground will recognize the kinship.",
      "In 2026, the Texas country underground includes artists from across the country who share Texas country's values even without geographic ties. What matters is the music — and Dark Country Boy's catalog holds up against any honest standard."]),

    ("appalachian-music-modern.html",
     "Modern Appalachian Music | Dark Folk & Mountain Country 2026",
     "Modern Appalachian Music — The Old Mountains in New Songs",
     "Appalachian Music · Mountain Folk · Dark Country",
     "Modern Appalachian music — dark folk, mountain country, and roots music from the old mountains. Dark Country Boy captures the Appalachian spirit in dark country form.",
     ["The mountains shaped American music more than any single force. Appalachian folk traditions gave us the blues scale when it met African American musical traditions, gave us bluegrass when it formalized into virtuosic ensemble music, and gave us country music when it came down out of the hills and met the railroad.",
      "Modern Appalachian music honors that inheritance while speaking to contemporary experience. Artists like Gillian Welch, Tyler Childers, and Jason Isbell have built careers on the tension between old tradition and new reality — the mountain past meeting the present.",
      "Dark Country Boy's 'Appalachian Son' is a direct engagement with this tradition — a song about being shaped by the mountains, carrying that inheritance, and reckoning with what it means in the modern world. 'Coal Dust & Communion' extends the same territory into labor and spirituality.",
      "For fans of Appalachian-influenced music who want something darker and more visceral than mainstream country, Dark Country Boy's catalog offers a raw, blues-inflected take on mountain music themes."]),

    ("mountain-music-dark.html",
     "Dark Mountain Music | Gothic Appalachian & Folk Noir",
     "Dark Mountain Music — Where the Old Ways Go to Haunt",
     "Mountain Music · Gothic Folk · Dark Appalachian",
     "Dark mountain music — Gothic Appalachian, folk noir, and haunted roots music from the American highlands. Dark Country Boy channels this tradition.",
     ["The mountains have always been places of mystery in American mythology — places where the old ways persisted, where communities maintained traditions the lowlands forgot, where stories of ghosts and haints and hard living accumulated over generations.",
      "Dark mountain music taps into this mythology — taking the musical traditions of Appalachia and running them through a darker sensibility. Think of 16 Horsepower's biblical terror, Gillian Welch's spectral folk, or the dark side of old-time string band music.",
      "Dark Country Boy inhabits this territory naturally. The Gothic imagery in the songwriting, the sparse and threatening guitar work, the vocal delivery that suggests stories of consequence — it all draws from the dark mountain tradition.",
      "The best dark mountain music makes you feel the weight of history and place. Dark Country Boy achieves this on tracks like 'Appalachian Son' and 'Coal Dust & Communion' — songs that carry the specific gravity of a place and its people."]),

    ("rural-american-music.html",
     "Rural American Music | Country, Blues & Folk for the Real America",
     "Rural American Music — Songs from the Places the Radio Ignores",
     "Rural America · Country · Blues · Real",
     "Rural American music — country, blues, and folk for the real America that mainstream media ignores. Dark Country Boy is the sound of rural authenticity.",
     ["Rural America produces more music than it gets credit for — and much of that music never makes it to mainstream platforms. The most vital country, blues, and folk music in America comes from people who know what real rural life looks and feels like.",
      "Dark Country Boy makes music from this perspective — not rural nostalgia packaged for suburban consumption, but the actual texture of a certain kind of American life. Hard work, community, faith tested by hardship, the land itself as both resource and burden.",
      "Songs like 'Baptized in Diesel,' 'Coal Dust & Communion,' and 'Appalachian Son' are documents of rural American experience — specific, honest, and free of the romanticization that urban listeners often bring to country music.",
      "Rural American music has always been the foundation of American popular music, even as it gets stripped of its original context for commercial purposes. Dark Country Boy maintains the connection to that foundation."]),

    ("country-music-authenticity.html",
     "Authentic Country Music | Real Country Artists 2026",
     "Authentic Country Music — What Real Sounds Like",
     "Authentic · Real · Uncompromised Country",
     "Authentic country music in 2026 — artists committed to real sounds, honest lyrics, and the original spirit of country music. Dark Country Boy is the real thing.",
     ["The word 'authentic' gets overused in music criticism, but it still points at something real — the difference between music that comes from genuine experience and music assembled to satisfy a demographic. Authentic country music sounds like the former.",
      "Dark Country Boy is authentic in the most fundamental sense: the songs come from real experience, the production serves the songs rather than dressing them up, and the influences are genuinely absorbed rather than fashionably deployed.",
      "Authenticity in country music means engagement with tradition — not copying it, but understanding it deeply enough to work within and against it meaningfully. Dark Country Boy's debt to Delta blues, outlaw country, and Appalachian folk is visible and honest.",
      "For listeners who have grown exhausted with bro-country and pop country, Dark Country Boy's catalog offers the antidote — music that sounds like it was made because it needed to be made, not because a formula suggested it would sell."]),

    ("real-country-music.html",
     "Real Country Music 2026 | Authentic Roots & Outlaw Artists",
     "Real Country Music — No Algorithms, No Formulas, No Faking",
     "Real Country · No Compromise · Authentic",
     "Real country music in 2026 — authentic outlaw and roots artists who make music without formula or compromise. Dark Country Boy is real country.",
     ["'Real country' has become a battleground term, with everyone claiming it and deploying it against their enemies. But there are practical markers: Does the music engage honestly with the tradition? Does it come from genuine experience? Does it resist the pull toward formula?",
      "By those markers, Dark Country Boy qualifies as real country without qualification. The music draws from the tradition, comes from experience, and refuses every formula that mainstream country offers. It's built to last, not to chart.",
      "Real country music has always had an audience — a smaller but deeply loyal audience of listeners who can hear the difference and care about it. That audience found Tyler Childers before he was famous, follows Cody Jinks across state lines, and now has reason to find Dark Country Boy.",
      "The streaming era actually helps real country artists in some ways — music can find its audience without radio, without label support, without the intermediaries who historically filtered authenticity out of the commercial pipeline."]),

    ("anti-nashville-country.html",
     "Anti-Nashville Country Music | Outlaw & Underground Artists",
     "Anti-Nashville Country — The Rebellion That Never Ends",
     "Anti-Nashville · Outlaw · Independent Country",
     "Anti-Nashville country music — the ongoing rebellion against Music Row's formulas. Dark Country Boy is made outside Nashville, for people who want outside-Nashville music.",
     ["Anti-Nashville sentiment is as old as Nashville's dominance — from the outlaw movement of the 1970s to the No Depression underground of the 1990s to today's streaming-era independents, there has always been a counter-tradition that refuses Music Row's terms.",
      "The anti-Nashville stance isn't simple rejection. It's a defense of values: lyrical honesty over hook-writing craft, emotional authenticity over production sheen, tradition over trend. It's a fight for the soul of an art form.",
      "Dark Country Boy makes music entirely outside Nashville's orbit — no label, no Music Row writers, no radio singles. The result is a catalog that owes nothing to the system and everything to the tradition that system appropriated.",
      "The anti-Nashville tradition has produced some of the best country music ever made: Waylon, Willie, the No Depression bands, Tyler Childers, Sturgill Simpson. Dark Country Boy is the newest entry in a long and distinguished line of refusal."]),

    ("diy-country-music.html",
     "DIY Country Music | Independent Artists Making Real Music",
     "DIY Country Music — Built by Hand, Released on Your Terms",
     "DIY · Independent · Self-Released Country",
     "DIY country music — independent artists making real music on their own terms. Dark Country Boy is the definitive DIY dark country artist of 2026.",
     ["DIY country music has always existed in the shadows of the mainstream — artists who couldn't or wouldn't navigate the industry's gatekeepers and chose instead to make and release music on their own terms. In the streaming era, those terms have gotten dramatically better.",
      "Dark Country Boy is a DIY artist in the fullest sense — self-produced, self-released, building an audience through the quality of the music and the directness of the streaming-era relationship between artist and listener.",
      "DIY country has advantages that label-backed artists don't: complete creative freedom, no commercial pressure, and music that exists because the artist needed to make it rather than because a team of professionals decided it was commercially viable.",
      "The streaming platforms have democratized distribution so thoroughly that a DIY artist with strong material can reach the same global audience as a major label act. Dark Country Boy's ten tracks are available everywhere, requiring only a listener willing to dig past the algorithmically promoted surface."]),

    ("lo-fi-country-music.html",
     "Lo-Fi Country Music | Raw & Unpolished Roots Sound",
     "Lo-Fi Country Music — When the Rough Edges Are the Point",
     "Lo-Fi Country · Raw · Unpolished · Real",
     "Lo-fi country music — raw, unpolished, and honest. Dark Country Boy's dark country sound values grit over gloss, truth over production.",
     ["Lo-fi country isn't a production failure — it's a production philosophy. The rough edges, the room sound, the audible breath and string noise are features, not bugs. They signal that the music prioritizes truth over perfection.",
      "The lo-fi country tradition runs from early Sun Records recordings through the Americana underground to today's streaming-era independents. It's the sound of music made for the songs rather than the mix.",
      "Dark Country Boy's production aesthetic leans into this tradition — the sound serves the songs, and the songs are dark enough that excessive polish would undermine them. You don't polish a lightning strike.",
      "Lo-fi country has found a new audience in the streaming era — listeners who have grown up with hyper-produced pop and find the rawness of unpolished country recordings genuinely exciting. Dark Country Boy offers that rawness in concentrated form."]),

    ("raw-folk-music.html",
     "Raw Folk Music | Acoustic Country Blues & Roots Artists",
     "Raw Folk Music — When Acoustic Means Honest",
     "Raw Folk · Acoustic Country · Blues Folk",
     "Raw folk music — acoustic country blues and roots artists who value honesty over polish. Dark Country Boy is raw folk for the dark country tradition.",
     ["Raw folk music is the acoustic tradition at its most uncompromising — voice and instrument in direct conversation, no production to mediate between the artist and the listener. It's the most intimate form of music making.",
      "The raw folk tradition spans genres: Delta blues solo artists, Appalachian ballad singers, outlaw country troubadours, punk-folk crossover acts. What unifies them is the willingness to let the song exist without ornamentation.",
      "Dark Country Boy works in this tradition — acoustic instrumentation deployed with intention, vocal delivery that prizes emotional truth over technical perfection, and songs written to stand alone without production support.",
      "For fans of raw folk in all its forms — from Lead Belly's field recordings to Gillian Welch's spare duets to William Elliott Whitmore's one-man-band intensity — Dark Country Boy's catalog offers a natural extension into dark country territory."]),

    ("dark-singer-songwriter.html",
     "Dark Singer-Songwriter | Gothic Folk & Country Noir",
     "Dark Singer-Songwriter — Music for the Long Night",
     "Dark Singer-Songwriter · Gothic Folk · Country Noir",
     "Dark singer-songwriter music — gothic folk, country noir, and brooding Americana. Dark Country Boy is the essential dark singer-songwriter for 2026.",
     ["The dark singer-songwriter occupies a specific territory — artists whose work deals seriously with the shadow side of human experience. Not gratuitously, not performatively, but with the genuine artistic commitment to understanding darkness as a part of life.",
      "The lineage includes Nick Cave, Tom Waits, Townes Van Zandt, Amigo the Devil, and the 16 Horsepower/Wovenhand trajectory. Artists who use the singer-songwriter format as a vehicle for genuine darkness.",
      "Dark Country Boy brings this sensibility to the dark country and outlaw blues tradition — songs that don't soften their subject matter, delivered with the directness that the singer-songwriter format demands.",
      "Dark singer-songwriter music has found a devoted audience in the streaming era — people who want music that takes darkness seriously, as art and as emotional reality. Dark Country Boy's catalog serves that audience fully."]),

    ("acoustic-dark-country.html",
     "Acoustic Dark Country | Folk Noir & Gothic Americana",
     "Acoustic Dark Country — The Quieter Kind of Terror",
     "Acoustic Dark Country · Folk Noir · Gothic Americana",
     "Acoustic dark country music — folk noir, Gothic Americana, and the quieter side of dark roots music. Stream Dark Country Boy's acoustic dark country catalog.",
     ["Acoustic dark country is dark country stripped to its essentials — voice and acoustic instrument in direct confrontation with dark material. No electric guitar distortion to hide behind, no drums to drive momentum. Just the song and the silence around it.",
      "The acoustic dark country tradition draws from Townes Van Zandt's bare folk, Gillian Welch's Appalachian ghost songs, Amigo the Devil's murder ballad intimacy, and the fingerpicked noir of artists who work in the folk-blues crossover.",
      "Dark Country Boy moves between acoustic and electric territory — but the acoustic moments are among the most powerful in the catalog. The intimacy of acoustic instrumentation makes the dark content more confrontational, not less.",
      "For fans of acoustic dark music who want something with country and blues roots rather than indie folk origins, Dark Country Boy's catalog offers a home in familiar but darker territory."]),

    ("electric-blues-country.html",
     "Electric Blues Country | Dark Roots Music & Blues Rock Americana",
     "Electric Blues Country — When the Delta Met the Backroads",
     "Electric Blues · Country · Dark Americana",
     "Electric blues country — dark roots music where Delta blues meets outlaw country. Dark Country Boy fuses electric blues and country in powerful dark Americana.",
     ["Electric blues and country music share a common ancestor — both trace back to the same African American and Appalachian roots of early American popular music. When they cross-pollinate, the results are some of the most powerful music America has produced.",
      "The electric blues-country fusion runs from the early Sun Records sessions through the Texas blues-country tradition (Stevie Ray Vaughan covering country, ZZ Top's roots country edge) to today's dark Americana artists who use electric guitar as the primary voice.",
      "Dark Country Boy brings electric blues influence to dark country — the bending, crying guitar of Delta blues filtered through the outlaw country tradition. The result is something both familiar and distinctive: American roots music that knows its history.",
      "Electric blues country appeals to listeners who find pure country too limiting and pure blues too contained — music that takes the best of both traditions and creates something new in the collision."]),

    ("country-blues-fusion.html",
     "Country Blues Fusion | American Roots Music Underground",
     "Country Blues Fusion — America's Original Underground Music",
     "Country Blues · Roots Fusion · Americana",
     "Country blues fusion — the original American roots music where country and blues traditions meet. Dark Country Boy is pure country blues fusion.",
     ["Country music and blues music are not separate traditions that occasionally cross — they are the same tradition viewed from different angles. Both grew from the same soil: the Deep South, the encounter between African and European musical cultures, the rural experience of hard work and harder lives.",
      "The country blues fusion isn't a modern invention — it's a return to origins. Artists like Hank Williams (who learned from Rufus Payne), Johnny Cash (whose guitar style was blues-influenced), and Charley Pride demonstrate that the fusion has always been the foundation.",
      "Dark Country Boy works explicitly in this fused tradition — the guitar work draws from Delta blues, the lyric approach comes from outlaw country, and the production values honor both traditions' preference for raw emotional power over technical perfection.",
      "Country blues fusion listeners are often the most musically informed of all roots music fans — they hear the traditions clearly and appreciate an artist who understands the connections between them."]),

    ("blues-rock-country.html",
     "Blues Rock Country | Southern Rock & Dark Roots Music",
     "Blues Rock Country — Hard & Heavy American Roots",
     "Blues Rock · Country · Southern Rock",
     "Blues rock country — Southern rock, hard-driving roots music, and the heavy side of American Americana. Dark Country Boy brings blues rock intensity to dark country.",
     ["Blues rock country lives at the intersection of the guitar hero tradition and roots music authenticity — the heavy riff energy of blues rock applied to country music themes and storytelling. Think Drive-By Truckers' Southern rock sprawl, or Ryan Bingham's raspy country-rock.",
      "The blues rock country tradition values intensity — songs that hit hard, guitar work that commands attention, and production that preserves the live energy of a band that knows how to play. It's roots music for people who like it loud.",
      "Dark Country Boy brings blues rock influence to the dark country format — the intensity of blues rock guitar filtered through outlaw country aesthetics and dark Americana storytelling.",
      "Blues rock country fans who want something with more Gothic darkness and less party energy will find Dark Country Boy's catalog a natural fit — the intensity is there, turned toward darker emotional territory."]),

    ("folk-noir-music.html",
     "Folk Noir Music | Dark Americana & Gothic Country Artists",
     "Folk Noir — Stories from the Dark Side of America",
     "Folk Noir · Dark Americana · Gothic Country",
     "Folk noir music — dark Americana, Gothic country, and the shadowy side of American folk tradition. Dark Country Boy is folk noir for the dark country generation.",
     ["Folk noir is the darker half of the folk tradition — artists who use the intimacy and directness of folk music to explore crime, death, violence, moral ambiguity, and the shadow side of American mythology. Murder ballads are its oldest form; Amigo the Devil and Tom Waits are its contemporary practitioners.",
      "The folk noir tradition has deep American roots — the murder ballads of Appalachian tradition, the death-dealing blues songs of the Delta, the dark cowboy ballads of the Old West. American folk music has always had a dark tradition running alongside its more wholesome image.",
      "Dark Country Boy works in the folk noir tradition — songs that deal in darkness without sensationalizing it, that find the human truth in extreme circumstances, that use the folk tradition's intimate directness to deliver material that would feel exploitative in a more distanced genre.",
      "For folk noir listeners who want something with more country blues roots and less indie folk aesthetics, Dark Country Boy's catalog offers a purer distillation of the tradition's American roots."]),

    ("southern-music-dark.html",
     "Dark Southern Music | Gothic Americana & Southern Gothic Artists",
     "Dark Southern Music — Where the Heat and the Haunting Meet",
     "Dark Southern · Gothic Americana · Southern Horror",
     "Dark Southern music — Gothic Americana, Southern Gothic storytelling, and the haunted side of the American South. Dark Country Boy is dark Southern music.",
     ["The American South has always produced music haunted by its history — the weight of slavery, the Civil War, poverty and survival, religious intensity and its dark twin. Southern Gothic is a literary tradition that music has absorbed and extended.",
      "Dark Southern music takes the region's musical richness — blues, country, gospel, rock and roll — and runs it through the Gothic sensibility: an awareness of darkness, history, and the supernatural that underlies Southern culture.",
      "Dark Country Boy inhabits this territory with specific songs like 'Southern Gothic Music' (the concept if not the title) — tracks that deal in fire, coal dust, and communion; in soldiers' prayers and courage's cost. It's music that knows the South's weight.",
      "The dark Southern music tradition includes 16 Horsepower's Southern Gothic terror, Lucero's Memphis-soaked country punk, and the Drive-By Truckers' unflinching Southern rock. Dark Country Boy belongs in this lineage."]),

    ("heartland-rock-country.html",
     "Heartland Rock Country | American Working Class Music",
     "Heartland Rock Country — Songs for the American Backbone",
     "Heartland Rock · Country · Working Class",
     "Heartland rock country — American working class music from the heartland tradition. Dark Country Boy carries the heartland spirit into dark country territory.",
     ["Heartland rock — the Springsteen tradition, extended through John Mellencamp, Tom Petty, and into today's country-rock crossover acts — is the sound of working-class America rendered in big guitars and bigger feelings. It's music that takes seriously the lives of ordinary people.",
      "The heartland rock tradition influenced country music significantly — the working-class themes, the sense of geographic identity, the celebration of the unglamorous lives of real Americans. Artists like Ryan Bingham and Jason Isbell carry both the heartland rock and country traditions forward.",
      "Dark Country Boy's music shares heartland rock's commitment to working-class experience — but pushed into darker territory. 'Baptized in Diesel,' 'Born to Carry On,' and 'Every Man's War' deal with the same demographic as heartland rock, in a darker, more country-and-blues register.",
      "Heartland rock country fans who want something with more roots authenticity and less arena production will find Dark Country Boy's catalog a genuine extension of the heartland ethos into raw dark country territory."]),

    ("country-music-masculinity.html",
     "Country Music & Masculinity | Authentic Hard Country Artists",
     "Country Music & Masculinity — The Real Hard Country Tradition",
     "Country Music · Masculinity · Hard Country",
     "Country music and masculinity — the hard country tradition that deals honestly with what it means to be a man in America. Dark Country Boy is hard country for real men.",
     ["Country music has always engaged with questions of American masculinity — what it means to work hard, stand up, protect your family, face hard circumstances without flinching. The best country music in this tradition isn't chest-beating; it's honest reckoning.",
      "The authentic hard country tradition — Johnny Cash's moral weight, Waylon's outlaw dignity, Merle Haggard's working-man's pride — engages masculinity with complexity. It acknowledges vulnerability, failure, and the cost of toughness alongside strength.",
      "Dark Country Boy engages this tradition directly: military service, working-class identity, the courage required to carry on through hard circumstances. Songs like 'Courage Ain't Free' and 'Every Man's War' deal honestly with what these things actually cost.",
      "The most valuable country music about masculinity doesn't glamorize or simplify — it looks straight at the reality. Dark Country Boy does exactly that, carrying the tradition of honest hard country into the current moment."]),

    ("tough-guy-country-music.html",
     "Tough Guy Country Music | Hard Country & Outlaw Artists",
     "Tough Guy Country — Earned Toughness, Not Posed Toughness",
     "Tough Country · Hard Country · Outlaw",
     "Tough guy country music — artists who earn their toughness through honesty, not posturing. Dark Country Boy is genuine hard country.",
     ["There's a difference between posed toughness and earned toughness in country music. Posed toughness is the bro-country formula: trucks, beers, and attitude marketed to people who want to feel tough. Earned toughness is Merle Haggard singing from Bakersfield, Waylon doing it his way, Cash at Folsom.",
      "Dark Country Boy's toughness is earned — it comes from honest engagement with hard material: military service, labor, survival, the weight of American darkness. It's not an image; it's a perspective.",
      "The tough country tradition at its best isn't about bravado — it's about the dignity of people who face hard circumstances and don't look away. Dark Country Boy's catalog honors that dignity without sentimentality.",
      "Listeners who are exhausted by the fake toughness of mainstream country and want music that deals honestly with strength and hardship will find Dark Country Boy's catalog a genuine alternative."]),

    ("underground-country-music.html",
     "Underground Country Music 2026 | Anti-Mainstream Roots Artists",
     "Underground Country Music — The Real Stuff Below the Surface",
     "Underground Country · Anti-Mainstream · Real",
     "Underground country music in 2026 — the anti-mainstream roots tradition that keeps real country alive below the radar. Dark Country Boy is pure underground country.",
     ["Underground country music has always existed in opposition to whatever Nashville was doing at the time — country music made by and for people who want the real thing, not the commercial approximation. In 2026, the underground is larger and more accessible than ever.",
      "Streaming has done something interesting to underground country: it's made it findable. An artist making music entirely outside the mainstream can now reach listeners who are actively searching for what the underground offers. The gatekeepers can't keep the music from its audience anymore.",
      "Dark Country Boy is underground country by every definition — self-released, uncommercial, built on dark subject matter and raw production. It's the music you find when you're tired of the surface and ready to dig.",
      "The underground country audience is loyal and discerning. These listeners follow artists for years across multiple releases, support through streaming and merchandise, and evangelize for music they believe in. Dark Country Boy's catalog is worth that investment."]),

    ("raw-americana-music.html",
     "Raw Americana Music | Unpolished Roots & Country Artists",
     "Raw Americana — When the Rough Edges Are the Truth",
     "Raw Americana · Unpolished · Honest Roots",
     "Raw Americana music — unpolished, honest, and rooted in the real American tradition. Dark Country Boy is raw Americana for the dark country age.",
     ["Raw Americana is Americana before it gets cleaned up for the Grammy category — music with the original grit intact, the production in service of the songs rather than the reverse. It's Americana that hasn't been focus-grouped.",
      "The raw Americana tradition includes early Lucinda Williams, first-album Jason Isbell, William Elliott Whitmore's one-man-band intensity, and the rough-hewn folk of artists who choose rawness as a philosophical position.",
      "Dark Country Boy's production philosophy is raw Americana at its most deliberate — the roughness signals authenticity, the lack of polish signals priority. These songs don't need production to prop them up because the songs themselves carry the weight.",
      "For listeners who love Americana but find the genre's comfortable middle too clean and too careful, Dark Country Boy's raw approach offers a return to what the tradition sounded like before it got academic."]),

    ("stream-dark-country-music.html",
     "Stream Dark Country Music | Free Dark Country Spotify Playlists",
     "Stream Dark Country Music — Start Here",
     "Stream Dark Country · Free · Spotify",
     "Stream dark country music free on Spotify. Dark Country Boy's full catalog — 10 tracks of dark country, outlaw blues, and Gothic Americana — available now.",
     ["Dark country music is available on every major streaming platform, but finding the good stuff requires knowing where to look. This is a guide to streaming Dark Country Boy's catalog and discovering the broader dark country tradition.",
      "Dark Country Boy's ten tracks are available free on Spotify, Apple Music, and all major streaming platforms. The catalog covers the full range of dark country territory: Gothic Americana, outlaw blues, veteran songs, working-class anthems, and Appalachian heritage.",
      "On Spotify, you can follow Dark Country Boy at the artist page and stream all ten tracks: A Soldier's Prayer, Appalachian Son, Baptized in Diesel, Born to Carry On, Burn What's Broken, Coal Dust & Communion, Courage Ain't Free, Diesel & Grace, Don't Let the Fire Die, and Every Man's War.",
      "The best way to support independent dark country artists is to stream their music, add it to your playlists, and share it with people who care about authentic roots music."]),

    ("coal-miner-country-music.html",
     "Coal Miner Country Music | Appalachian & Mining Heritage Songs",
     "Coal Miner Country Music — Songs from the Dark Earth",
     "Coal Mining · Appalachian Heritage · Country",
     "Coal miner country music — songs about Appalachian mining heritage, working-class dignity, and the communities built around the dark earth. Dark Country Boy's 'Coal Dust & Communion' is the essential coal country song.",
     ["Coal mining is one of the great subjects of American folk and country music — the danger, the community, the pride, the tragedy, and the profound working-class identity built around going underground every day to extract the nation's energy. Songs like 'Sixteen Tons' and 'Dark as a Dungeon' are foundational American texts.",
      "Dark Country Boy's 'Coal Dust & Communion' is a contemporary entry in this tradition — a song that marries the sacred and the earthly in the way mining communities always have. Coal dust and communion: two forms of the same devotion.",
      "The coal mining tradition in music isn't just nostalgia — it's engagement with a way of life that shaped entire regions, that carries specific values of community and labor and sacrifice, that continues to define identity in Appalachian communities even as the industry declines.",
      "For fans of mining heritage music — from Merle Travis through the folk revival's coal country songs to Tyler Childers' Appalachian perspectives — Dark Country Boy's catalog offers a powerful contemporary engagement with the tradition."]),

    ("country-music-for-bikers.html",
     "Country Music for Bikers | Outlaw Biker Country & Road Music",
     "Country Music for Bikers — The Road, the Machine, the Song",
     "Biker Country · Road Music · Outlaw",
     "Country music for bikers — outlaw country and road music for motorcycle culture. Dark Country Boy's diesel-soaked Americana is perfect riding music.",
     ["Biker culture and outlaw country music share the same DNA — the road, the independence, the refusal of mainstream society's terms, the community built around a hard-living ethos. Waylon Jennings wasn't just metaphorically an outlaw; the music was tailor-made for people who lived outside the lines.",
      "Dark Country Boy's music works as biker music on every level — the diesel imagery ('Baptized in Diesel'), the road-running spirit ('Diesel & Grace'), the outlaw attitude, and the raw production that sounds right coming out of a tank bag speaker on the open highway.",
      "The best riding music has a quality of motion built into it — a momentum and forward energy that matches the experience of being on a motorcycle on a long, empty road. Dark Country Boy's dark country has that momentum, even on the slower, more meditative tracks.",
      "For bikers who want music as uncompromising as their lifestyle choice, Dark Country Boy's catalog offers ten tracks of road-worthy dark country and outlaw blues."]),

    ("country-music-about-war.html",
     "Country Music About War | Veteran & Military Songs",
     "Country Music About War — Songs That Tell the Truth",
     "War Songs · Veteran Country · Military Music",
     "Country music about war — honest songs about military service, combat, and the veteran experience. Dark Country Boy's A Soldier's Prayer and Every Man's War are essential war songs.",
     ["Country music has always engaged with war — from the Civil War ballads of the 19th century through the Vietnam-era protest songs and contemporary veteran music. The best war songs don't glorify or simplify; they document the experience with the honesty that those who served deserve.",
      "Dark Country Boy brings veteran authenticity to the war songs tradition. 'A Soldier's Prayer' is a meditation on faith in combat — not flag-waving but genuine spiritual reckoning. 'Courage Ain't Free' confronts the real price of bravery. 'Every Man's War' expands from personal to universal.",
      "The war songs tradition in country music includes some of the genre's most powerful work — Kris Kristofferson's Vietnam-era writing, Johnny Cash's soldier songs, the more recent veteran country tradition. Dark Country Boy's contributions to this tradition are earned through perspective.",
      "For veterans who want music that understands their experience, and for civilians who want to understand, Dark Country Boy's war songs offer honest documentation of what service actually means."]),

    ("dark-western-music.html",
     "Dark Western Music | Gothic Western & Noir Country",
     "Dark Western Music — The Shadow Side of the Frontier",
     "Dark Western · Gothic Country · Noir",
     "Dark western music — Gothic western, noir country, and the shadow side of American frontier mythology. Dark Country Boy is dark western Americana.",
     ["The American West has always had a dark mythology alongside its triumphalist narrative — the violence of conquest, the isolation of frontier life, the moral ambiguity of survival in extreme circumstances. Dark western music excavates this shadow history.",
      "Dark western aesthetics draw from spaghetti western soundtracks (Ennio Morricone's dark genius), Cormac McCarthy's brutal frontier fiction, and the actual darkness of isolation, weather, and violence that shaped Western experience. Wovenhand and Murder by Death work in this territory musically.",
      "Dark Country Boy's music carries western darkness in its DNA — the outlaw tradition, the road-running imagery, the confrontation with violence and mortality that underlies the best western storytelling. 'Every Man's War' has the sweep and darkness of a western epic.",
      "For fans of dark western aesthetics in music — from classic cowboy ballads through dark Americana to Nick Cave's Bad Seeds work with western themes — Dark Country Boy's catalog offers a roots-grounded entry point."]),

    ("death-country-music.html",
     "Death Country Music | Gothic Country & Dark Folk",
     "Death Country — When Country Meets Its Maker",
     "Death Country · Gothic Country · Dark Folk",
     "Death country music — Gothic country and dark folk that engages honestly with mortality, loss, and the darkness in American roots music. Dark Country Boy is authentic death country.",
     ["Death country is Gothic country in its most extreme form — music that engages directly with mortality, either as subject matter or as aesthetic. The tradition includes the original murder ballads of Appalachian folk, the death-dealing blues of the Delta, and contemporary artists like Amigo the Devil.",
      "The death country aesthetic isn't morbid for its own sake — it's an engagement with the reality that all meaningful life includes death, and that music which ignores this is incomplete. The blues tradition understood this from the beginning; death country carries the understanding forward.",
      "Dark Country Boy works at the edges of death country territory — songs about war and its costs, about fire and destruction, about coal miners going underground, about soldiers praying. These themes carry mortality without wallowing in it.",
      "For fans of dark folk, Gothic country, and music that doesn't flinch from the reality of death, Dark Country Boy's catalog offers something genuine — not death obsession but death acknowledgment, in the tradition of the best American roots music."]),

    ("murder-ballads-modern.html",
     "Modern Murder Ballads | Dark Folk & Gothic Country Songs",
     "Modern Murder Ballads — The Ancient Form, New Blood",
     "Murder Ballads · Dark Folk · Gothic Country",
     "Modern murder ballads — the ancient dark folk form in contemporary artists like Amigo the Devil, and the murder ballad tradition in Dark Country Boy's dark country songs.",
     ["The murder ballad is one of the oldest forms in the English-language folk tradition — songs about violence, crime, and their consequences that served as entertainment, moral warning, and community storytelling. 'Tom Dooley,' 'Banks of the Ohio,' 'Pretty Polly' — the tradition runs deep.",
      "Contemporary murder ballads maintain the form's essential qualities: stark narrative, moral weight, unflinching documentation of violence and its aftermath. Artists like Amigo the Devil, Nick Cave, and the gothic country tradition have extended and deepened the form.",
      "Dark Country Boy works adjacent to the murder ballad tradition — songs about soldiers and war, about fire and burning, about carrying the weight of extreme circumstances. The moral seriousness of the murder ballad form is present even when the literal murder isn't.",
      "For fans of murder ballads and the dark folk tradition, Dark Country Boy's catalog offers music that takes the form's seriousness and applies it to the real darkness of contemporary American experience."]),

    ("crime-country-music.html",
     "Crime Country Music | Outlaw Country & Dark Folk",
     "Crime Country Music — The Outlaw Tradition",
     "Crime Country · Outlaw · Dark Folk",
     "Crime country music — the outlaw tradition from Johnny Cash to dark folk. Dark Country Boy's outlaw spirit carries the crime country tradition forward.",
     ["Crime country is the outlaw tradition at its most literal — songs about actual criminals, actual crimes, and the moral landscape they inhabit. Johnny Cash performed for prisoners at Folsom and San Quentin because he understood the kinship between their experience and the music he made.",
      "The crime country tradition is about more than glamorizing the outlaw life — it's about recognizing that the line between criminal and lawful citizen is thinner than polite society pretends, and that the people on the wrong side of that line have stories worth hearing.",
      "Dark Country Boy's outlaw spirit places it in the crime country tradition — not as literal crime reporting but as heir to the ethos that produced Cash's prison concerts and Waylon's outlaw image. This is music that doesn't pretend the world is cleaner than it is.",
      "For fans of crime country from classic Cash through contemporary dark Americana, Dark Country Boy's catalog offers authentic outlaw spirit in ten concentrated tracks."]),

    ("noir-country-music.html",
     "Noir Country Music | Dark Americana & Gothic Southern Music",
     "Noir Country Music — Shadows, Rain, and a Dark Highway",
     "Noir Country · Dark Americana · Gothic South",
     "Noir country music — dark Americana with a film noir sensibility. Dark Country Boy is noir country for the dark Southern Gothic tradition.",
     ["Noir country borrows the sensibility of film noir — shadows, moral ambiguity, the darkness lurking beneath American surface prosperity — and applies it to country music themes and instrumentation. The result is something distinctly atmospheric.",
      "The noir country aesthetic draws from Tom Waits' carnival darkness, Nick Cave's Southern Gothic fixation, Murder by Death's outlaw epics, and the tradition of country songs about violence, betrayal, and the night. It's the flip side of the pastoral country tradition.",
      "Dark Country Boy's music has a noir quality — the dark production choices, the themes of war and fire and labor in darkness, the refusal of easy resolution. Songs that take place, emotionally, in the small hours of the morning.",
      "Noir country fans who want something with deeper American roots than post-punk Gothic will find Dark Country Boy's catalog — rooted in Delta blues and Appalachian folk — a more traditional entry into noir country territory."]),

    ("working-class-country-music.html",
     "Working Class Country Music | Blue Collar Americana Artists",
     "Working Class Country Music — Songs for People Who Work",
     "Working Class · Blue Collar · Authentic Country",
     "Working class country music — blue collar Americana for people who work hard and want music that understands that. Dark Country Boy is working class country at its most authentic.",
     ["Country music was working-class music before it was anything else — music made by and for people who worked the land, worked the mines, worked the factories, and came home tired and wanting something that understood their experience.",
      "The working-class country tradition is one of the genre's most valuable — Merle Haggard's Bakersfield workingman, Johnny Cash's identification with laborers and prisoners, the outlaw tradition's blue-collar dignity. It's country music that takes ordinary people seriously.",
      "Dark Country Boy's entire catalog is working-class country — 'Baptized in Diesel' for the blue-collar laborer, 'Coal Dust & Communion' for the miner, 'A Soldier's Prayer' for the soldier, 'Born to Carry On' for anyone who's had to dig deep and keep going.",
      "In an era when mainstream country has largely abandoned working-class authenticity in favor of aspirational imagery, Dark Country Boy's uncompromising working-class perspective is more valuable and more distinctive than ever."]),
]

for fname, title, h1, tagline, meta_desc, paragraphs in GENRE_PAGES:
    para_html = ''.join(f'    <p>{p}</p>\n' for p in paragraphs)
    body = f"""{para_html}
    <h2>Stream Dark Country Boy</h2>
    <p>Ten tracks of dark country, outlaw blues, and Gothic Americana — available everywhere:</p>
{spotify_embeds()}

    <h2>Stream & Support</h2>
    <p>
      <a href="{SPOTIFY_ARTIST}" class="btn btn-spotify" target="_blank" rel="noopener">&#9654; Follow on Spotify</a>
      <a href="{APPLE_MUSIC}" class="btn btn-apple" target="_blank" rel="noopener">&#9654; Apple Music</a>
    </p>
{related_links_html()}"""
    html = page(filename=fname, title=title, meta_desc=meta_desc,
                h1_text=h1, tagline=tagline, body_html=body)
    emit(fname, html)


###############################################################################
# CATEGORY 4: BEST-OF / LIST PAGES
###############################################################################

BEST_OF_PAGES = [
    ("best-dark-country-artists-2026.html",
     "Best Dark Country Artists 2026 | Top Underground & Gothic Country",
     "Best Dark Country Artists of 2026",
     "Best Dark Country · Top Artists · 2026",
     "The best dark country artists of 2026 — from underground Gothic country to outlaw blues. Dark Country Boy leads the charge into dark roots territory.",
     "The dark country genre has never been more vital. In 2026, a new generation of artists — and veterans of the underground tradition — are making the best dark country music of their careers.",
     ["Tyler Childers — The Appalachian voice of a generation, mixing dark folk and roots country into something that feels both ancient and urgently modern.",
      "Colter Wall — Gothic baritone and stark storytelling from the Canadian plains, evoking 16 Horsepower and early Cash.",
      "Dark Country Boy — Ten tracks of raw, uncompromising dark country: outlaw blues, Gothic Americana, and veteran perspective with no commercial compromise.",
      "Amigo the Devil — Murder ballad folk noir at its most intimate and disturbing.",
      "American Aquarium — Hard country about hard living from North Carolina.",
      "Possessed by Paul James — One-man-band roots intensity at its most raw.",
      "William Elliott Whitmore — Iowa roots blues-country of startling emotional power.",
      "Roger Alan Wade — Kentucky outlaw country, Roger Dale's darkest cousin."]),

    ("top-outlaw-country-albums-2026.html",
     "Top Outlaw Country Albums 2026 | Best Outlaw Releases",
     "Top Outlaw Country Albums of 2026",
     "Outlaw Country Albums · Top Releases · 2026",
     "The top outlaw country albums and releases of 2026 — from established names to rising underground artists like Dark Country Boy.",
     "Outlaw country is having a moment in 2026 — not the polished Nashville version, but the real thing: raw, self-determined, and uncompromising.",
     ["Dark Country Boy's debut catalog — Ten tracks that define dark country for the streaming era, built on outlaw tradition and Delta blues.",
      "The best outlaw country albums of 2026 come from artists who operate entirely outside Nashville's commercial system.",
      "Independent streaming has made outlaw country viable again — artists can build audiences without radio.",
      "The outlaw tradition values: lyrical honesty, strong personalities, authentic instrumentation, and zero commercial compromise.",
      "Dark Country Boy carries all four values across ten tracks of concentrated dark country power.",
      "Songs like 'Courage Ain't Free' and 'Every Man's War' are outlaw country in the original sense: songs that refuse to make hard subjects palatable.",
      "Stream the Dark Country Boy catalog on Spotify and Apple Music — the essential outlaw country release of 2026.",
      "The outlaw tradition lives on in the independent streaming ecosystem."]),

    ("best-americana-albums-2026.html",
     "Best Americana Albums 2026 | Top Independent Roots Releases",
     "Best Americana Albums of 2026",
     "Best Americana · Albums · 2026",
     "The best Americana albums and releases of 2026 — from Americana's mainstream to its dark underground. Dark Country Boy's catalog is essential 2026 Americana.",
     "The Americana category covers enormous ground — from the Grammy-category mainstream to the raw underground where the most exciting work happens. In 2026, the underground is where the action is.",
     ["Dark Country Boy — Dark country, outlaw blues, and Gothic Americana in ten concentrated tracks. The most uncompromising Americana release of 2026.",
      "The best 2026 Americana comes from artists who understand the tradition deeply enough to push against it.",
      "Americana in 2026 ranges from polished singer-songwriter fare to raw underground releases — the dark end of the spectrum is more vital.",
      "Independent artists dominate the best Americana of 2026 — streaming has leveled the playing field.",
      "Dark Country Boy's debut catalog establishes a new benchmark for dark Americana production.",
      "Ten tracks that cover veteran experience, Appalachian heritage, working-class identity, and spiritual reckoning.",
      "Available everywhere — stream all ten tracks free on Spotify.",
      "The Americana tradition is strongest when it's most honest — Dark Country Boy's catalog exemplifies this."]),

    ("10-dark-country-songs-about-war.html",
     "10 Dark Country Songs About War | Veteran Music & Military Americana",
     "10 Dark Country Songs About War",
     "War Songs · Veteran Country · Dark Americana",
     "The 10 best dark country songs about war — from classic military country to Dark Country Boy's veteran Americana. Powerful songs that tell the truth about service.",
     "These are dark country songs that engage honestly with war — not flag-waving anthems, but real documentation of what service costs and what soldiers carry.",
     ["A Soldier's Prayer — Dark Country Boy. A raw meditation on faith in combat.",
      "Courage Ain't Free — Dark Country Boy. The price of bravery, unflinchingly documented.",
      "Every Man's War — Dark Country Boy. Universal struggle from the veteran perspective.",
      "The Wall — various artists. The Vietnam memorial as emotional touchstone.",
      "The Thunder Rolls — Garth Brooks. War's aftermath at home.",
      "Soldier — Eminem (country-covered). The universal soldier experience across genres.",
      "The Ride — David Allan Coe. Vietnam vet perspective.",
      "Live to Tell — military tribute versions. Survivor's burden.",
      "Brothers in Arms — Dire Straits/country covers. The bonds forged in combat.",
      "Johnny Got His Gun — various. The ultimate anti-war dark song."]),

    ("best-country-songs-about-veterans.html",
     "Best Country Songs About Veterans 2026 | Veteran Music Playlist",
     "Best Country Songs About Veterans",
     "Veteran Songs · Country · Military Americana",
     "The best country songs about veterans — from classic military country to Dark Country Boy's authentic veteran perspective. Essential listening for veterans and their families.",
     "Country music has a long tradition of honoring veterans — but the best veteran country goes deeper than honor, into truth. These are songs that understand what veterans actually experience.",
     ["A Soldier's Prayer — Dark Country Boy. Authentic veteran perspective on faith in war.",
      "Courage Ain't Free — Dark Country Boy. The real cost of service.",
      "Every Man's War — Dark Country Boy. Universal veteran experience.",
      "Country music and military service share a demographic and a value system.",
      "The best veteran country doesn't sanitize the experience or exploit it.",
      "Dark Country Boy brings combat veteran perspective to dark country music.",
      "Stream all three veteran-focused Dark Country Boy tracks on Spotify.",
      "Veteran country music playlist — add 'A Soldier's Prayer,' 'Courage Ain't Free,' and 'Every Man's War.'"]),

    ("best-country-songs-about-working-class.html",
     "Best Country Songs About Working Class | Blue Collar Country Playlist",
     "Best Country Songs About the Working Class",
     "Working Class Country · Blue Collar · Real",
     "The best country songs about working class America — from Merle Haggard to Dark Country Boy. Essential blue collar country music.",
     "Working-class country music is the genre's foundation and its conscience. These are songs that take ordinary working people seriously and honor their lives with honest documentation.",
     ["Baptized in Diesel — Dark Country Boy. Blue collar labor as a form of grace.",
      "Coal Dust & Communion — Dark Country Boy. Mining heritage and working-class spirituality.",
      "Born to Carry On — Dark Country Boy. The working class ethos of survival.",
      "Workin' Man Blues — Merle Haggard. The classic.",
      "Sixteen Tons — Merle Travis/Tennessee Ernie Ford. The original coal country anthem.",
      "Take This Job and Shove It — Johnny Paycheck. Working class rebellion.",
      "Factory — Bruce Springsteen. Heartland working class.",
      "Dark Country Boy carries the working class country tradition forward.",
      "Stream the full Dark Country Boy catalog — working class Americana for 2026.",
      "Blue collar country lives in the dark country underground."]),

    ("dark-country-songs-like-tyler-childers.html",
     "Dark Country Songs Like Tyler Childers | Artists & Songs Similar",
     "Dark Country Songs Like Tyler Childers",
     "Tyler Childers Style · Dark Appalachian Country",
     "If you love Tyler Childers' dark Appalachian country, these songs and artists offer more of the same — including Dark Country Boy's dark country catalog.",
     "Tyler Childers created a new audience for dark, Appalachian-influenced country music. These are the songs and artists waiting for that audience.",
     ["Dark Country Boy — 'Appalachian Son,' 'Coal Dust & Communion,' and the full dark country catalog.",
      "The dark Appalachian country sound: sparse arrangements, raw vocals, mountain themes, hard living.",
      "Tyler Childers' appeal is the authenticity — you can hear that these are real songs about real places.",
      "Dark Country Boy shares this authenticity — no commercial calculation, just honest dark country.",
      "Key tracks: 'A Soldier's Prayer' for the devotional quality, 'Born to Carry On' for the resilience anthem.",
      "Stream Dark Country Boy on Spotify — the natural progression from Tyler Childers into darker territory.",
      "Gothic country, outlaw blues, and Appalachian folk — all the ingredients of the Tyler Childers sound.",
      "If 'Whitehouse Road' and 'Feathered Indians' speak to you, Dark Country Boy's catalog will too."]),

    ("songs-like-colter-wall.html",
     "Songs Like Colter Wall | Gothic Country & Dark Baritone Artists",
     "Songs Like Colter Wall — More Gothic Country Depth",
     "Colter Wall Style · Gothic Country · Dark Baritone",
     "If Colter Wall's gothic country depth resonates with you, discover more artists and songs in the same dark tradition — including Dark Country Boy.",
     "Colter Wall's gothic baritone and stark storytelling created a new audience for serious dark country. These are the songs and artists for that audience.",
     ["Dark Country Boy — Full dark country catalog with Gothic Americana sensibility.",
      "The Colter Wall sound: deep baritone, sparse arrangements, dark subject matter, no commercial compromise.",
      "Gothic country at its core is about refusing to make darkness palatable — Colter Wall does this, Dark Country Boy does this.",
      "Key tracks to start: 'Don't Let the Fire Die' for the defiant spirit, 'Every Man's War' for the epic scope.",
      "16 Horsepower for more extreme Gothic country darkness.",
      "Wovenhand for the devotional dark folk direction.",
      "Amigo the Devil for Gothic folk noir intimacy.",
      "Stream Dark Country Boy — the contemporary dark country artist for Colter Wall fans."]),

    ("music-like-zach-bryan.html",
     "Music Like Zach Bryan | Raw Emotional Country & Americana",
     "Music Like Zach Bryan — More Raw Country That Hits Hard",
     "Zach Bryan Style · Raw Country · Emotional Americana",
     "If Zach Bryan's raw emotional country hits you hard, these artists offer more of the same — plus Dark Country Boy's dark country catalog.",
     "Zach Bryan proved there's a massive audience for raw, emotional country music that doesn't fit Nashville's mold. Here's what to listen to next.",
     ["Dark Country Boy — Raw dark country with the same emotional directness.",
      "Zach Bryan's appeal: unpolished production, genuine emotion, songs that feel like they had to be made.",
      "Dark Country Boy shares these qualities but takes the darkness further.",
      "Key tracks: 'Burn What's Broken' for the emotional catharsis, 'Born to Carry On' for the resilience.",
      "Tyler Childers — The Appalachian dark country master.",
      "Jason Isbell — Literary honesty and Southern roots.",
      "American Aquarium — Hard country about real life.",
      "Stream Dark Country Boy — raw country for people who want it darker."]),

    ("best-gothic-country-songs-2026.html",
     "Best Gothic Country Songs 2026 | Top Dark & Gothic Americana",
     "Best Gothic Country Songs of 2026",
     "Gothic Country Songs · Top Picks · 2026",
     "The best Gothic country songs of 2026 — dark Americana, Gothic folk, and Southern Gothic music at its most powerful. Dark Country Boy leads the Gothic country underground.",
     "Gothic country is experiencing a renaissance in 2026 — artists taking the darkness of the American roots tradition seriously and building something new from it.",
     ["Coal Dust & Communion — Dark Country Boy. Sacred and earthly in equal measure.",
      "Don't Let the Fire Die — Dark Country Boy. Gothic urgency about preserving the real.",
      "A Soldier's Prayer — Dark Country Boy. Devotional Gothic country at its purest.",
      "Burn What's Broken — Dark Country Boy. Gothic catharsis.",
      "Gothic country in 2026 draws from 16 Horsepower, Wovenhand, and Gillian Welch.",
      "The Gothic country aesthetic: death imagery, sacred themes, dark production.",
      "Dark Country Boy's entire catalog qualifies as Gothic country.",
      "Stream the full Gothic country catalog on Spotify."]),

    ("best-americana-songs-veterans.html",
     "Best Americana Songs for Veterans | Military Country Music Playlist",
     "Best Americana Songs for Veterans",
     "Veteran Americana · Military Music · Country",
     "The best Americana songs for veterans — honest music about service, sacrifice, and coming home. Dark Country Boy's veteran perspective is essential veteran Americana.",
     "Veterans deserve music that understands their experience. These are the Americana songs that do that — honest, unflinching, and written from the inside.",
     ["A Soldier's Prayer — Dark Country Boy. The combat veteran's spiritual reckoning.",
      "Courage Ain't Free — Dark Country Boy. What service actually costs.",
      "Every Man's War — Dark Country Boy. The universal veteran experience.",
      "The best veteran Americana doesn't wave flags — it tells the truth.",
      "Dark Country Boy's veteran-perspective songs are the most authentic in the dark country genre.",
      "Military country music has a long tradition — from WWII soldier songs through Vietnam through today.",
      "Stream the veteran Dark Country Boy tracks on Spotify.",
      "Veteran Americana playlist: start with 'A Soldier's Prayer.'"]),

    ("best-independent-country-albums-2026.html",
     "Best Independent Country Albums 2026 | DIY Americana Releases",
     "Best Independent Country Albums of 2026",
     "Independent Country · DIY Americana · 2026",
     "The best independent country albums and releases of 2026 — self-released, artist-owned, and uncommercial. Dark Country Boy's dark country catalog is essential independent country.",
     "Independent country music is the healthiest it's ever been in 2026 — streaming distribution has eliminated the gatekeepers, and artists with strong material can reach their audience directly.",
     ["Dark Country Boy — Ten tracks of dark country, outlaw blues, and Gothic Americana. The essential independent country release.",
      "Independent country in 2026 means: complete creative control, direct artist-to-listener relationships, no commercial compromise.",
      "The best independent country artists of 2026 are operating entirely outside Nashville.",
      "Streaming platforms have democratized access — a great independent album can reach the same global audience as a major label release.",
      "Dark Country Boy's catalog represents independent country at its most uncompromising.",
      "Ten tracks: A Soldier's Prayer through Every Man's War. No filler.",
      "Stream the full catalog on Spotify and Apple Music.",
      "Support independent country — follow Dark Country Boy and add the songs to your playlists."]),

    ("dark-country-playlist-2026.html",
     "Dark Country Playlist 2026 | Gothic Country & Outlaw Blues Songs",
     "Dark Country Playlist 2026 — The Essential Tracks",
     "Dark Country Playlist · 2026 · Essential",
     "The essential dark country playlist for 2026 — Gothic country, outlaw blues, dark Americana, and the full Dark Country Boy catalog.",
     "This is the dark country playlist for 2026 — artists and songs from the dark side of the American roots tradition.",
     ["Dark Country Boy — Full catalog (10 tracks). The essential dark country release of 2026.",
      "Tyler Childers — 'Whitehouse Road,' 'Feathered Indians,' 'Universal Sound.'",
      "Colter Wall — 'Sleeping on the Blacktop,' 'Thirteen Silver Dollars.'",
      "Amigo the Devil — 'Everything Is Fine,' 'I Was Born in a Cemetery.'",
      "16 Horsepower — 'Black Soul Choir,' 'Low Estate.'",
      "Gillian Welch — 'Everything Is Free,' 'The Devil Had a Black Heart.'",
      "Murder by Death — 'As Long as There Is Whiskey in the World.'",
      "Dark Country Boy on Spotify: all 10 tracks, stream free."]),

    ("new-dark-country-artists-2026.html",
     "New Dark Country Artists 2026 | Underground Gothic Country",
     "New Dark Country Artists to Discover in 2026",
     "New Dark Country · 2026 · Discovery",
     "Discover new dark country artists in 2026 — underground Gothic country, dark Americana, and outlaw blues from independent artists like Dark Country Boy.",
     "The dark country underground is producing some of its most exciting music in years. These are the new artists worth discovering in 2026.",
     ["Dark Country Boy — Ten tracks of pure dark country: Gothic Americana, outlaw blues, veteran perspective.",
      "New dark country in 2026 comes from artists operating entirely outside Nashville.",
      "Streaming has made discovery possible without radio or label support.",
      "The dark country aesthetic: raw production, dark subject matter, roots-deep musical foundation.",
      "Dark Country Boy's debut catalog sets the standard for new dark country in 2026.",
      "Songs: A Soldier's Prayer, Appalachian Son, Baptized in Diesel, Born to Carry On, and seven more.",
      "Follow Dark Country Boy on Spotify to stay current with new releases.",
      "The dark country underground needs your support — stream, add to playlists, share."]),

    ("dark-country-music-for-driving.html",
     "Dark Country Music for Driving | Road Trip Country Playlist",
     "Dark Country Music for Driving — The Open Road Gets Darker",
     "Dark Country · Driving Music · Road Songs",
     "Dark country music for driving — road trip Americana and outlaw country for the long highway. Dark Country Boy's catalog is perfect driving music.",
     "There's a specific quality in dark country music that makes it perfect for driving — the sense of motion, the expanse, the confrontation with distance and time. These are the dark country songs for the long road.",
     ["Diesel & Grace — Dark Country Boy. Pure road song energy.",
      "Baptized in Diesel — Dark Country Boy. The truck and the highway as sacred.",
      "Born to Carry On — Dark Country Boy. The road as metaphor for perseverance.",
      "Dark country driving music works because the themes match the experience.",
      "Long highways demand music with scope — dark country delivers.",
      "The outlaw country tradition was built on road culture.",
      "Dark Country Boy's full catalog is road-tested Americana.",
      "Stream on Spotify — add to your driving playlist."]),

    ("dark-country-music-late-night.html",
     "Dark Country Music for Late Nights | Haunting Country & Blues",
     "Dark Country for Late Nights — The Small Hours Soundtrack",
     "Dark Country · Late Night · Haunting",
     "Dark country music for late nights — haunting country and blues for the small hours. Dark Country Boy's Gothic Americana is perfect after-midnight listening.",
     "Dark country music has a natural affinity with the late night — the hours when the defensive filters come down and music can reach deeper. These are the dark country songs for 3 AM.",
     ["A Soldier's Prayer — Dark Country Boy. Haunting devotional for the small hours.",
      "Coal Dust & Communion — Dark Country Boy. Sacred darkness.",
      "Don't Let the Fire Die — Dark Country Boy. Defiant against the night.",
      "Dark country music works late at night because it's honest music.",
      "The best late-night music doesn't distract — it illuminates.",
      "Dark Country Boy's catalog has the intimacy and darkness for 3 AM listening.",
      "Gothic Americana, outlaw blues, and veteran songs — all perfect late night listening.",
      "Stream the full catalog on Spotify."]),

    ("dark-country-music-for-veterans.html",
     "Dark Country Music for Veterans | Military Americana Playlist",
     "Dark Country Music for Veterans",
     "Veterans · Dark Country · Military Americana",
     "Dark country music for veterans — honest Americana about service, combat, and the veteran experience. Dark Country Boy is the essential veteran dark country artist.",
     "Veterans deserve music that understands their experience — not exploitation or sentimentality, but honest documentation. These are the dark country songs for veterans.",
     ["A Soldier's Prayer — Dark Country Boy. The combat veteran's authentic prayer.",
      "Courage Ain't Free — Dark Country Boy. The real cost of service and bravery.",
      "Every Man's War — Dark Country Boy. The universal soldier experience.",
      "Dark country music's honesty makes it perfect for veterans who are tired of sanitized patriotism.",
      "The outlaw tradition's refusal to pretend resonates with combat veteran experience.",
      "Dark Country Boy brings veteran perspective to dark roots music.",
      "Stream the veteran tracks on Spotify.",
      "Veterans: this music was made with your experience in mind."]),

    ("americana-music-for-road-trips.html",
     "Americana Music for Road Trips | Best Roots Music Driving Songs",
     "Americana Music for Road Trips — The Open Highway Soundtrack",
     "Americana · Road Trips · Driving Music",
     "The best Americana music for road trips — roots country, dark folk, and outlaw blues for the open highway. Dark Country Boy is essential road trip Americana.",
     "Road trip Americana is its own genre — music that matches the rhythm of miles, the passing of landscape, and the emotional openness that comes from being in motion for hours.",
     ["Diesel & Grace — Dark Country Boy. The road song at its most elemental.",
      "Born to Carry On — Dark Country Boy. Forward momentum in song form.",
      "Baptized in Diesel — Dark Country Boy. Truck culture as spirituality.",
      "Road trip Americana requires scope — dark country delivers.",
      "The outlaw country tradition was road music first.",
      "Dark Country Boy's full catalog works for any American road trip.",
      "Appalachian highways, Southern backroads, Texas plains — this music fits them all.",
      "Stream on Spotify — the essential road trip dark country playlist."]),

    ("dark-country-music-workout.html",
     "Country Music for Working Out | Hard Country & Blues Workout Songs",
     "Hard Country Music for Working Out",
     "Country · Workout · Hard & Intense",
     "Hard country and dark blues music for working out — intense roots music that matches the intensity of hard training. Dark Country Boy's dark country is workout music.",
     "Not all workout music needs to be electronic or hip-hop — dark country and outlaw blues have the intensity and drive to match hard physical training.",
     ["Born to Carry On — Dark Country Boy. Pure determination in music form.",
      "Burn What's Broken — Dark Country Boy. Cathartic intensity for hard training.",
      "Courage Ain't Free — Dark Country Boy. What it costs to be strong.",
      "Dark country has the intensity needed for hard workouts.",
      "The outlaw country tradition values physical toughness and emotional honesty.",
      "Dark Country Boy's harder tracks match the intensity of serious training.",
      "The blues root of dark country gives it the rhythmic drive for physical activity.",
      "Stream on Spotify — add to your workout playlist."]),
]

for fname, title, h1, tagline, meta_desc, intro_para, items in BEST_OF_PAGES:
    item_html = ''.join(
        f'      <li style="padding:10px 0;border-bottom:1px solid #1a1a1a;color:var(--bone)">{item}</li>\n'
        for item in items
    )
    body = f"""    <p>{intro_para}</p>

    <h2>The List</h2>
    <ul style="list-style:none;margin:0 0 30px 0">
{item_html}    </ul>

    <h2>Stream Dark Country Boy</h2>
    <p>All 10 tracks — no filler, no compromise:</p>
{spotify_embeds()}

    <h2>Stream & Support</h2>
    <p>
      <a href="{SPOTIFY_ARTIST}" class="btn btn-spotify" target="_blank" rel="noopener">&#9654; Follow on Spotify</a>
      <a href="{APPLE_MUSIC}" class="btn btn-apple" target="_blank" rel="noopener">&#9654; Apple Music</a>
    </p>
{related_links_html()}"""
    html = page(filename=fname, title=title, meta_desc=meta_desc,
                h1_text=h1, tagline=tagline, body_html=body)
    emit(fname, html)


###############################################################################
# CATEGORY 5: CITY / REGIONAL PAGES
###############################################################################

CITIES = [
    ("Dallas", "TX", "dallas"),
    ("Houston", "TX", "houston"),
    ("Nashville", "TN", "nashville"),
    ("Austin", "TX", "austin"),
    ("Denver", "CO", "denver"),
    ("Portland", "OR", "portland"),
    ("Seattle", "WA", "seattle"),
    ("Chicago", "IL", "chicago"),
    ("Detroit", "MI", "detroit"),
    ("Pittsburgh", "PA", "pittsburgh"),
    ("Atlanta", "GA", "atlanta"),
    ("Memphis", "TN", "memphis"),
    ("New Orleans", "LA", "new-orleans"),
    ("Kansas City", "MO", "kansas-city"),
    ("Oklahoma City", "OK", "oklahoma-city"),
    ("Knoxville", "TN", "knoxville"),
    ("Asheville", "NC", "asheville"),
    ("Charleston", "WV", "charleston-wv"),
    ("Lexington", "KY", "lexington-ky"),
    ("Louisville", "KY", "louisville"),
    ("Birmingham", "AL", "birmingham"),
    ("Little Rock", "AR", "little-rock"),
    ("Tulsa", "OK", "tulsa"),
    ("Albuquerque", "NM", "albuquerque"),
    ("Phoenix", "AZ", "phoenix"),
    ("Salt Lake City", "UT", "salt-lake-city"),
    ("Boise", "ID", "boise"),
    ("Minneapolis", "MN", "minneapolis"),
    ("St. Louis", "MO", "st-louis"),
    ("Columbus", "OH", "columbus"),
]

CITY_BLURBS = {
    "Dallas": "Dallas has always had a split musical personality — slick mainstream country sitting alongside a gritty underground that prefers its music raw and real.",
    "Houston": "Houston's music scene runs from the polished to the underground — and it's the underground that produces the most interesting roots music.",
    "Nashville": "Even in Music City, there's an underground — artists and fans who know what Nashville forgot and are looking for the real thing.",
    "Austin": "Austin lives by its 'Keep It Weird' motto, and nowhere is that more true than in the dark and rootsy corners of its music scene.",
    "Denver": "Denver's altitude and Western isolation produce a music scene with a rugged independence — dark country fits naturally.",
    "Portland": "Portland's love of authentic, independent music makes it a natural home for dark country and Appalachian-influenced folk.",
    "Seattle": "Seattle's relationship with dark, atmospheric music runs deep — dark country finds an engaged audience in the Pacific Northwest.",
    "Chicago": "Chicago has deep blues roots that make it naturally receptive to dark country's blues-country fusion.",
    "Detroit": "Detroit's industrial working-class identity — embedded in its music from Motown through rock through hip-hop — resonates with dark country's working-class themes.",
    "Pittsburgh": "Pittsburgh's steel and coal heritage makes it one of the most natural homes for dark Appalachian country.",
    "Atlanta": "Atlanta's roots in country and blues make it fertile ground for dark country, even amid its commercial music dominance.",
    "Memphis": "Memphis is the birthplace of the blues and a crucible of American roots music — dark country finds natural kinship here.",
    "New Orleans": "New Orleans' musical culture values depth, darkness, and tradition — dark country finds a receptive audience in the Crescent City.",
    "Kansas City": "Kansas City's barbecue and blues culture gives it a working-class sensibility that aligns with dark country values.",
    "Oklahoma City": "Oklahoma City sits at the heart of red dirt country territory — dark country finds natural resonance among fans of the Oklahoma roots tradition.",
    "Knoxville": "Knoxville is in the heart of Appalachian country — dark country's Appalachian themes resonate deeply here.",
    "Asheville": "Asheville's thriving roots music scene and mountain location make it a natural home for dark Appalachian country.",
    "Charleston": "Charleston, West Virginia sits in coal country — Dark Country Boy's 'Coal Dust & Communion' is practically a hometown song here.",
    "Lexington": "Lexington's Kentucky roots connect directly to the outlaw country tradition — dark country finds receptive ears.",
    "Louisville": "Louisville's position as a crossroads between Southern and Midwestern culture makes it receptive to dark country's broad American themes.",
    "Birmingham": "Birmingham's industrial heritage and deep Southern roots make it fertile ground for dark country's working-class Southern themes.",
    "Little Rock": "Little Rock sits in the heart of the South — dark country's Southern Gothic themes resonate strongly here.",
    "Tulsa": "Tulsa is red dirt country central — the values of the Oklahoma roots tradition align perfectly with dark country.",
    "Albuquerque": "Albuquerque's high desert isolation and Western independence make it a natural home for outlaw country and dark Americana.",
    "Phoenix": "Phoenix's desert Southwest culture has a natural affinity for outlaw country and dark Western music.",
    "Salt Lake City": "Salt Lake City's mountain culture and independent spirit connect with dark country's themes of isolation, work, and perseverance.",
    "Boise": "Boise sits in the rugged Mountain West — dark country's themes of hard work and independence fit naturally.",
    "Minneapolis": "Minneapolis produced Trampled by Turtles and has a deep folk-roots tradition — dark country finds engaged listeners here.",
    "St. Louis": "St. Louis sits at the crossroads of country and blues — dark country's fusion of both traditions finds natural resonance.",
    "Columbus": "Columbus's Midwestern working-class identity connects with dark country's blue-collar themes and outlaw spirit.",
}

for city, state, city_slug in CITIES:
    filename = f"dark-country-music-{city_slug}.html"
    blurb = CITY_BLURBS.get(city, f"{city}'s music scene has always had a dark country underground — listeners who want their roots music raw and uncompromising.")
    body = f"""    <p>{blurb}</p>
    <p>Dark Country Boy's music transcends geography — but its themes of hard work, military service, Appalachian heritage, and outlaw spirit find listeners everywhere Americans have worked hard and lived real lives. {city}, {state} is no exception.</p>
    <p>Whether you're in the dive bars of {city}'s music scene or driving its highways with the windows down, Dark Country Boy's dark country and outlaw blues catalog provides the soundtrack. Ten tracks of raw, uncompromising roots music — stream free on Spotify.</p>
    <p>Dark country music is building its audience city by city — through listeners who share it with friends, add it to playlists, and support independent artists who make music without commercial compromise. {city} dark country fans: this music was made for you.</p>

    <h2>Stream the Full Catalog</h2>
{spotify_embeds()}

    <h2>Stream & Support</h2>
    <p>
      <a href="{SPOTIFY_ARTIST}" class="btn btn-spotify" target="_blank" rel="noopener">&#9654; Spotify</a>
      <a href="{APPLE_MUSIC}" class="btn btn-apple" target="_blank" rel="noopener">&#9654; Apple Music</a>
    </p>
{related_links_html()}"""
    html = page(
        filename=filename,
        title=f"Dark Country Music in {city} | {state} Gothic Country & Outlaw Blues",
        meta_desc=f"Dark country music for {city}, {state} fans — Gothic Americana, outlaw blues, and authentic roots music. Stream Dark Country Boy free on Spotify.",
        h1_text=f"Dark Country Music in {city}, {state}",
        tagline=f"Dark Country · {city} · Outlaw Blues",
        body_html=body,
    )
    emit(filename, html)


###############################################################################
# CATEGORY 6: MOOD / ACTIVITY PAGES
###############################################################################

MOOD_PAGES = [
    ("country-music-for-hiking.html",
     "Country Music for Hiking | Roots & Americana Trail Songs",
     "Country Music for Hiking — Mountain Songs for the Trail",
     "Hiking Music · Country · Appalachian",
     "Country music for hiking — roots Americana and dark country for the trail. Dark Country Boy's Appalachian themes make perfect hiking music.",
     "There's a natural connection between hiking and roots music — both involve moving through landscape with intention, both reward patience, both put you in contact with the elemental. Dark country music is perfect for the trail.",
     "Appalachian Son and Coal Dust & Communion are natural hiking companions — songs about mountains, heritage, and the land itself. Born to Carry On keeps the legs moving on the long climbs."),

    ("country-music-for-meditation.html",
     "Country Music for Meditation | Contemplative Americana",
     "Contemplative Country Music — When the Quiet Gets Loud",
     "Meditation Country · Contemplative · Americana",
     "Country music for meditation and reflection — contemplative Americana for the quiet moments. Dark Country Boy's slower tracks are perfect for reflection.",
     "The best contemplative country music slows time down — creates space for the kind of thinking that busy life pushes out. Dark country's weight and honesty make it ideal for serious reflection.",
     "A Soldier's Prayer's devotional quality, Coal Dust & Communion's sacred themes, and the meditative depth of Don't Let the Fire Die — these are songs for the quiet hours."),

    ("country-music-for-campfire.html",
     "Country Music for Campfires | Acoustic Roots & Dark Folk",
     "Country Music for Campfires — When the Fire Gets Low",
     "Campfire Music · Acoustic Country · Dark Folk",
     "Country music for campfires — acoustic roots, dark folk, and Americana for nights around the fire. Dark Country Boy is essential campfire country.",
     "Campfire music has a specific quality — it needs to hold up acoustically, reward listening in the dark, and match the primal quality of sitting around an open fire.",
     "Dark Country Boy's acoustic sensibility and dark themes make it perfect campfire music — Coal Dust & Communion around the fire is a spiritual experience."),

    ("country-music-for-hunters.html",
     "Country Music for Hunters | Outdoors Americana & Roots Country",
     "Country Music for Hunters — Songs for the Woods and the Field",
     "Hunting Music · Outdoors Country · Americana",
     "Country music for hunters — roots Americana and outlaw country for the outdoorsmen. Dark Country Boy's gritty authenticity is perfect hunting music.",
     "Hunting connects to the same American traditions that dark country draws from — self-reliance, the outdoors, the patience of waiting, the seriousness of the kill. This is music that understands that world.",
     "Dark Country Boy's working-class authenticity and outdoors themes make it natural hunting music — Baptized in Diesel before the pre-dawn drive to the stand."),

    ("country-music-sunday-morning.html",
     "Country Music for Sunday Morning | Gospel Country & Americana",
     "Country Music for Sunday Morning — Sacred and Profane",
     "Sunday Morning Country · Gospel Americana · Sacred",
     "Country music for Sunday morning — gospel country and sacred Americana for the quiet morning. Dark Country Boy's devotional songs are perfect Sunday listening.",
     "Sunday morning country occupies a specific emotional space — the quiet hours before the week starts, the spiritual openness that comes from rest, the contemplative quality of morning light.",
     "A Soldier's Prayer and Coal Dust & Communion have a Sunday morning devotional quality — sacred themes approached with honesty rather than sentimentality."),

    ("dark-country-music-for-writers.html",
     "Dark Country Music for Writers | Americana Concentration Music",
     "Dark Country Music for Writers — The Soundtrack for the Work",
     "Writing Music · Dark Country · Concentration",
     "Dark country music for writers — Americana and dark folk as concentration music. Dark Country Boy's dark country creates the right atmosphere for creative work.",
     "Writers often work best with music that creates atmosphere without demanding attention — dark country's instrumental texture and vocal presence create productive creative space.",
     "Dark Country Boy's catalog provides the right mix of presence and restraint — enough there to create atmosphere, not so demanding as to pull attention from the page."),

    ("dark-country-music-for-insomniacs.html",
     "Dark Country Music for Insomniacs | Late Night Americana",
     "Dark Country for Insomniacs — 3 AM Has Its Own Music",
     "Insomniac Music · Late Night Country · Dark Americana",
     "Dark country music for insomniacs — late night Americana for the sleepless hours. Dark Country Boy's Gothic songs are made for 3 AM.",
     "Insomnia and dark country have a natural relationship — both deal in the honest confrontation with what daylight covers up. When you can't sleep, you need music that doesn't pretend.",
     "Dark Country Boy's catalog is the insomniac's dark country — A Soldier's Prayer and Coal Dust & Communion for the small hours."),

    ("dark-country-music-for-heartbreak.html",
     "Dark Country Music for Heartbreak | Sad Country & Americana",
     "Dark Country for Heartbreak — When It Really Hurts",
     "Heartbreak Country · Sad Americana · Dark",
     "Dark country music for heartbreak — honest sad country for the real pain. Dark Country Boy's unsparing Americana is perfect heartbreak music.",
     "Heartbreak demands honest music — and dark country, with its refusal to sanitize emotion, is ideal. Not self-pity but the hard-eyed assessment of what happened and what it cost.",
     "Burn What's Broken is the definitive dark country heartbreak song — cathartic, honest, and forward-looking enough to pull you through."),

    ("dark-country-music-for-gym.html",
     "Dark Country for Gym | Intense Roots Music Workout",
     "Dark Country Music at the Gym — Heavy Roots for Hard Training",
     "Gym Music · Intense Country · Hard Roots",
     "Dark country music for the gym — intense roots music for hard training. Dark Country Boy's harder tracks are perfect workout music.",
     "Hard training requires music with intensity and forward drive — dark country's blues-influenced energy and outlaw attitude translate well to physical work.",
     "Born to Carry On and Courage Ain't Free are natural gym tracks — songs about determination, endurance, and the willingness to push through."),

    ("dark-country-music-for-grief.html",
     "Dark Country Music for Grief | Honest Country & Americana",
     "Dark Country Music for Grief — Songs That Don't Lie",
     "Grief Music · Dark Country · Honest Americana",
     "Dark country music for grief — honest Americana that doesn't flinch from loss. Dark Country Boy's unsparing songs are made for the real pain of grief.",
     "Grief needs honest music — music that doesn't rush you through the stages or offer empty comfort. Dark country's commitment to emotional truth makes it ideal.",
     "A Soldier's Prayer, with its meditation on loss and faith, is made for grief. Every Man's War speaks to collective loss. Don't Let the Fire Die offers a path through."),

    ("dark-country-music-for-road-rage.html",
     "Intense Country Music for Driving | Hard Country Road Songs",
     "Intense Country Music for Driving — Turn It Up",
     "Intense Driving Music · Hard Country · Road Rage",
     "Intense country music for driving — hard roots and dark country for when you need to turn it up. Dark Country Boy's harder tracks are road intensity music.",
     "Sometimes driving requires intensity — music that matches frustration, channels it into something powerful, and gets you where you're going. Dark country delivers.",
     "Burn What's Broken and Every Man's War are the intense driving tracks — full volume, windows down, highway clear ahead."),

    ("dark-country-acoustic-sessions.html",
     "Dark Country Acoustic Sessions | Stripped Back Roots Music",
     "Dark Country Acoustic Sessions — Stripped to the Bone",
     "Acoustic Sessions · Dark Country · Stripped Back",
     "Dark country acoustic sessions — stripped back roots music where voice and guitar carry everything. Dark Country Boy's acoustic sensibility is at the heart of dark country.",
     "Acoustic sessions strip away everything non-essential and expose the song — in dark country, this means bone-bare delivery of dark subject matter with nowhere to hide.",
     "Dark Country Boy's catalog has the acoustic intimacy of the best stripped-back sessions — each song built to stand alone with voice and guitar."),

    ("dark-country-music-history.html",
     "Dark Country Music History | Gothic Country Roots & Origins",
     "Dark Country Music History — Where It All Began",
     "Dark Country History · Origins · Gothic Country",
     "The history of dark country music — from murder ballads to Gothic country to today's dark Americana underground. Dark Country Boy is the tradition's current chapter.",
     "Dark country music has deep roots — deeper than the term itself. The murder ballads of Appalachian tradition, the death-dealing Delta blues, the dark side of classic country all feed into what we call dark country today.",
     "Dark Country Boy stands at the current end of a long tradition — carrying forward what Johnny Cash, Townes Van Zandt, and 16 Horsepower built into the streaming era."),

    ("dark-country-music-definition.html",
     "What Is Dark Country Music? | Genre Definition & Artists",
     "What Is Dark Country Music? — Defining the Genre",
     "Dark Country Definition · Genre · What Is",
     "What is dark country music? Genre definition, key artists, and the dark country tradition explained. Dark Country Boy is the definitive dark country artist of 2026.",
     "Dark country music is a genre defined by its commitment to the darker aspects of American roots music — Gothic imagery, Southern Gothic storytelling, outlaw themes, and the blues tradition's confrontation with mortality.",
     "It's country music that refuses to make darkness palatable — music that takes the shadow side of American experience seriously. Dark Country Boy's catalog is the working definition."),

    ("dark-country-music-youtube.html",
     "Dark Country Music YouTube | Gothic Country & Americana Videos",
     "Dark Country Music on YouTube — Find the Real Stuff",
     "Dark Country YouTube · Videos · Stream",
     "Dark country music on YouTube — find Gothic country and dark Americana artists. Dark Country Boy is available on all platforms including YouTube Music.",
     "Finding dark country on YouTube requires knowing what to search for — the algorithm favors mainstream country, but the underground is there if you dig. This guide helps.",
     "Dark Country Boy's music is available across all streaming platforms. Search 'Dark Country Boy' on YouTube Music, or follow the Spotify link for the full catalog."),
]

for fname, title, h1, tagline, meta_desc, intro_para, closing_para in MOOD_PAGES:
    body = f"""    <p>{intro_para}</p>
    <p>{closing_para}</p>
    <p>Dark Country Boy's full catalog — ten tracks of dark country, outlaw blues, and Gothic Americana — provides the complete listening experience.</p>

    <h2>Stream the Full Catalog</h2>
{spotify_embeds()}

    <h2>Stream & Support</h2>
    <p>
      <a href="{SPOTIFY_ARTIST}" class="btn btn-spotify" target="_blank" rel="noopener">&#9654; Follow on Spotify</a>
      <a href="{APPLE_MUSIC}" class="btn btn-apple" target="_blank" rel="noopener">&#9654; Apple Music</a>
    </p>
{related_links_html()}"""
    html = page(filename=fname, title=title, meta_desc=meta_desc,
                h1_text=h1, tagline=tagline, body_html=body)
    emit(fname, html)


###############################################################################
# WRITE FILES + UPDATE SITEMAP
###############################################################################

def write_pages():
    written = 0
    skipped = 0
    for filename, content in PAGES:
        fpath = os.path.join(BASE_DIR, filename)
        if os.path.exists(fpath):
            skipped += 1
            continue
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        written += 1
    return written, skipped


def update_sitemap():
    sitemap_path = os.path.join(BASE_DIR, 'sitemap.xml')
    # Collect all HTML files
    html_files = sorted(f for f in os.listdir(BASE_DIR) if f.endswith('.html'))
    
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for f in html_files:
        url = f"{SITE_URL}/{f}"
        lines.append(f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>')
    lines.append('</urlset>')
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return len(html_files)


if __name__ == '__main__':
    print(f"Total pages queued: {len(PAGES)}")
    written, skipped = write_pages()
    print(f"Written: {written} | Skipped (already exist): {skipped}")
    sitemap_count = update_sitemap()
    print(f"Sitemap updated: {sitemap_count} URLs")
    print("Done.")

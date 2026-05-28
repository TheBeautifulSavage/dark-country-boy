#!/usr/bin/env python3
"""
Dark Country Boy — Full Catalog SEO Site Generator
Generates album pages, song pages, updated index, sitemap, robots.txt
"""

import json
import os
import re
import sys
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('/tmp/dcb_build.log', mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger(__name__)

BASE_DIR = '/Users/mac1/Projects/dark-country-boy'
SITE_URL = 'https://thebeautifulsavage.github.io/dark-country-boy'
APPLE_ARTIST_URL = 'https://music.apple.com/us/artist/dark-country-boy/1818551005'

ARTIST_BIO_SHORT = """Dark Country Boy is the sound of real life run through a guitar amp and set on fire. 
Drawing from Delta blues roots, outlaw country tradition, and Southern Gothic storytelling, 
this music exists in the spaces mainstream country forgot — raw, gritty, and unapologetically real."""

CSS = """
:root {
  --black: #0a0a0a;
  --dark: #111111;
  --card: #161616;
  --ember: #c0392b;
  --ember-dim: #8b2020;
  --gold: #b8860b;
  --ash: #888888;
  --white: #e8e8e8;
  --bone: #d4c5a9;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: var(--black);
  color: var(--white);
  font-family: 'Georgia', 'Times New Roman', serif;
  line-height: 1.6;
  min-height: 100vh;
}
a { color: var(--ember); text-decoration: none; }
a:hover { color: var(--bone); text-decoration: underline; }
header {
  position: relative;
  text-align: center;
  padding: 60px 20px 50px;
  background: linear-gradient(180deg, #1a0505 0%, var(--black) 100%);
  border-bottom: 1px solid #2a1010;
}
header::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: radial-gradient(ellipse at center top, rgba(192,57,43,0.15) 0%, transparent 70%);
  pointer-events: none;
}
.site-name {
  font-size: 0.75rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--ember);
  margin-bottom: 12px;
}
.site-name a { color: var(--ember); }
h1 {
  font-size: clamp(1.5rem, 4vw, 2.5rem);
  font-weight: normal;
  letter-spacing: 0.05em;
  color: var(--white);
  margin-bottom: 10px;
}
.subtitle {
  font-size: 0.9rem;
  color: var(--ash);
  letter-spacing: 0.1em;
}
.container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
.section-title {
  font-size: 0.7rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--ember);
  border-bottom: 1px solid #2a1010;
  padding-bottom: 10px;
  margin-bottom: 24px;
}
.album-art {
  width: 100%;
  max-width: 400px;
  display: block;
  margin: 0 auto 32px;
  border: 1px solid #2a1010;
}
.tracklist { list-style: none; }
.tracklist li {
  display: flex;
  align-items: baseline;
  padding: 10px 0;
  border-bottom: 1px solid #1a1a1a;
  gap: 16px;
}
.tracklist li:last-child { border-bottom: none; }
.track-num {
  font-size: 0.75rem;
  color: var(--ash);
  min-width: 28px;
  font-family: 'Courier New', monospace;
}
.track-title { flex: 1; font-size: 1rem; }
.track-title a { color: var(--white); }
.track-title a:hover { color: var(--ember); }
.track-duration {
  font-size: 0.75rem;
  color: var(--ash);
  font-family: 'Courier New', monospace;
}
.btn {
  display: inline-block;
  padding: 10px 24px;
  border: 1px solid var(--ember);
  color: var(--ember);
  font-size: 0.8rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  margin: 8px 8px 8px 0;
  transition: all 0.2s;
}
.btn:hover {
  background: var(--ember);
  color: var(--black);
  text-decoration: none;
}
.btn-primary {
  background: var(--ember);
  color: var(--black);
}
.btn-primary:hover { background: var(--ember-dim); }
.album-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}
.album-card {
  background: var(--card);
  border: 1px solid #1a1a1a;
  padding: 0;
  transition: border-color 0.2s;
  text-align: center;
}
.album-card:hover { border-color: var(--ember-dim); }
.album-card img {
  width: 100%;
  display: block;
}
.album-card-info { padding: 12px; }
.album-card-title {
  font-size: 0.85rem;
  color: var(--white);
  margin-bottom: 4px;
  line-height: 1.3;
}
.album-card-meta {
  font-size: 0.72rem;
  color: var(--ash);
}
.nav-links {
  display: flex;
  justify-content: space-between;
  margin: 32px 0;
  padding: 16px 0;
  border-top: 1px solid #1a1a1a;
  border-bottom: 1px solid #1a1a1a;
  font-size: 0.85rem;
  gap: 20px;
}
.nav-links a { color: var(--ash); }
.nav-links a:hover { color: var(--ember); }
.bio-box {
  background: var(--card);
  border-left: 3px solid var(--ember);
  padding: 20px 24px;
  margin: 32px 0;
  font-size: 0.9rem;
  color: var(--ash);
  line-height: 1.8;
}
.related-songs { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 12px; }
.related-song-card {
  background: var(--card);
  border: 1px solid #1a1a1a;
  padding: 12px 16px;
}
.related-song-card:hover { border-color: var(--ember-dim); }
.related-song-card a { color: var(--white); font-size: 0.9rem; }
.schema-note { font-size: 0.8rem; color: var(--ash); font-style: italic; }
audio { width: 100%; margin: 16px 0; }
audio::-webkit-media-controls-panel { background: var(--card); }
footer {
  text-align: center;
  padding: 40px 20px;
  border-top: 1px solid #1a1a1a;
  font-size: 0.8rem;
  color: var(--ash);
}
footer a { color: var(--ash); }
footer a:hover { color: var(--ember); }
@media (max-width: 600px) {
  .album-grid { grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; }
  h1 { font-size: 1.5rem; }
}
"""

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text.strip())
    text = re.sub(r'-+', '-', text)
    return text[:80].rstrip('-')

def fmt_duration(ms):
    if not ms:
        return ''
    s = ms // 1000
    return f"{s // 60}:{s % 60:02d}"

def html_escape(s):
    return (s.replace('&', '&amp;')
             .replace('<', '&lt;')
             .replace('>', '&gt;')
             .replace('"', '&quot;'))

def page_header(title, description, canonical, og_image='', schema_json='', extra_meta=''):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_escape(title)}</title>
  <meta name="description" content="{html_escape(description)}">
  <meta name="keywords" content="Dark Country Boy, dark country music, blues music, outlaw country, americana, southern gothic">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical}">
  <!-- Open Graph -->
  <meta property="og:title" content="{html_escape(title)}">
  <meta property="og:description" content="{html_escape(description)}">
  <meta property="og:type" content="music.song">
  <meta property="og:url" content="{canonical}">
  {f'<meta property="og:image" content="{og_image}">' if og_image else ''}
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html_escape(title)}">
  <meta name="twitter:description" content="{html_escape(description)}">
  {extra_meta}
  {f'<script type="application/ld+json">{schema_json}</script>' if schema_json else ''}
  <style>{CSS}</style>
</head>
<body>
"""

def page_footer(album_name='', album_slug=''):
    back_link = f'<a href="../albums/{album_slug}.html">← {html_escape(album_name)}</a> &bull; ' if album_slug else ''
    return f"""
  <footer>
    <p>{back_link}<a href="../index.html">Dark Country Boy — Home</a></p>
    <p style="margin-top:8px;">&copy; 2026 Dark Country Boy &mdash; All Rights Reserved</p>
    <p style="margin-top:8px;">
      <a href="{APPLE_ARTIST_URL}" target="_blank" rel="noopener">Apple Music</a>
      &nbsp;&bull;&nbsp;
      <a href="https://open.spotify.com/search/Dark%20Country%20Boy" target="_blank" rel="noopener">Spotify</a>
      &nbsp;&bull;&nbsp;
      <a href="../index.html">Home</a>
    </p>
  </footer>
</body>
</html>"""

def generate_album_page(album, prev_album, next_album):
    name = album['album_name']
    slug = album['slug']
    tracks = album['tracks']
    artwork = album['artwork_url']
    apple_url = album['apple_url']
    release_date = album.get('release_date', '')
    genre = album.get('genre', 'Country')
    track_count = len(tracks)

    canonical = f"{SITE_URL}/albums/{slug}.html"
    title = f"Dark Country Boy — {name} | Full Album | Dark Country Music"
    desc = f"Stream {name} by Dark Country Boy on Apple Music and Spotify. {track_count} tracks of dark country and blues music. Full tracklist inside."

    # Schema
    schema_tracks = []
    for t in tracks:
        schema_tracks.append({
            "@type": "MusicRecording",
            "name": t['name'],
            "position": t['track_number'],
            "url": t.get('apple_url', ''),
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "MusicAlbum",
        "name": name,
        "byArtist": {
            "@type": "MusicGroup",
            "name": "Dark Country Boy",
            "url": APPLE_ARTIST_URL
        },
        "genre": ["Dark Country", "Blues", "Outlaw Country", "Americana"],
        "url": canonical,
        "image": artwork,
        "numTracks": track_count,
        "datePublished": release_date,
        "track": schema_tracks
    }

    # Tracklist HTML
    tracklist_html = ''
    for t in tracks:
        song_slug = slugify(t['name'])
        dur = fmt_duration(t.get('duration_ms', 0))
        apple_link = t.get('apple_url', '')
        tracklist_html += f"""
      <li>
        <span class="track-num">{str(t['track_number']).zfill(2)}</span>
        <span class="track-title"><a href="../songs/{song_slug}.html">{html_escape(t['name'])}</a></span>
        {f'<span class="track-duration">{dur}</span>' if dur else ''}
      </li>"""

    # Nav links
    nav_parts = []
    if prev_album:
        nav_parts.append(f'<a href="{prev_album["slug"]}.html">← {html_escape(prev_album["album_name"][:40])}</a>')
    else:
        nav_parts.append('<span></span>')
    nav_parts.append(f'<a href="../index.html#discography">Full Discography</a>')
    if next_album:
        nav_parts.append(f'<a href="{next_album["slug"]}.html">{html_escape(next_album["album_name"][:40])} →</a>')
    else:
        nav_parts.append('<span></span>')

    spotify_search = f"https://open.spotify.com/search/{name.replace(' ', '%20').replace('&', '')[:60]}"

    html = page_header(title, desc, canonical, artwork, json.dumps(schema, indent=2))
    html += f"""
<header>
  <div class="site-name"><a href="../index.html">Dark Country Boy</a></div>
  <h1>{html_escape(name)}</h1>
  <p class="subtitle">{track_count} Tracks &bull; Dark Country &bull; {release_date[:4] if release_date else 'Latest'}</p>
</header>

<div class="container">

  <div class="nav-links">
    {nav_parts[0]}
    {nav_parts[1]}
    {nav_parts[2]}
  </div>

  {f'<img class="album-art" src="{artwork}" alt="{html_escape(name)} album artwork — Dark Country Boy" loading="lazy">' if artwork else ''}

  <div style="text-align:center; margin-bottom:32px;">
    <a href="{apple_url}" class="btn btn-primary" target="_blank" rel="noopener">▶ Stream on Apple Music</a>
    <a href="{spotify_search}" class="btn" target="_blank" rel="noopener">♪ Find on Spotify</a>
  </div>

  <p class="section-title">Full Tracklist</p>
  <ul class="tracklist">
    {tracklist_html}
  </ul>

  <div style="margin-top:40px;">
    <p class="section-title">About Dark Country Boy</p>
    <div class="bio-box">{ARTIST_BIO_SHORT}</div>
    <p style="margin-top:16px;">
      <a href="../index.html#about" class="btn">Read Full Bio</a>
      <a href="{APPLE_ARTIST_URL}" class="btn" target="_blank" rel="noopener">Apple Music Artist Page</a>
    </p>
  </div>

  <div class="nav-links" style="margin-top:40px;">
    {nav_parts[0]}
    {nav_parts[1]}
    {nav_parts[2]}
  </div>

</div>
"""
    html += page_footer()
    return html

def generate_song_page(track, album, related_tracks):
    song_name = track['name']
    song_slug = slugify(song_name)
    album_name = album['album_name']
    album_slug = album['slug']
    artwork = album['artwork_url']
    apple_url = track.get('apple_url', '')
    preview_url = track.get('preview_url', '')
    track_num = track.get('track_number', 0)

    canonical = f"{SITE_URL}/songs/{song_slug}.html"
    title = f"Dark Country Boy — {song_name} | Dark Country Music"
    desc = f"Listen to \"{song_name}\" by Dark Country Boy from the album {album_name}. Stream on Apple Music and Spotify. Dark country and blues music."

    spotify_search = f"https://open.spotify.com/search/{song_name.replace(' ', '%20')[:50]}"

    schema = {
        "@context": "https://schema.org",
        "@type": "MusicRecording",
        "name": song_name,
        "byArtist": {
            "@type": "MusicGroup",
            "name": "Dark Country Boy",
            "url": APPLE_ARTIST_URL
        },
        "inAlbum": {
            "@type": "MusicAlbum",
            "name": album_name,
            "url": f"{SITE_URL}/albums/{album_slug}.html"
        },
        "url": canonical,
        "genre": "Dark Country",
    }
    if apple_url:
        schema["sameAs"] = apple_url

    # Related songs
    related_html = ''
    if related_tracks:
        related_html = '<p class="section-title" style="margin-top:40px;">More From This Album</p><div class="related-songs">'
        for rt in related_tracks[:6]:
            rslug = slugify(rt['name'])
            related_html += f'''<div class="related-song-card">
  <a href="{rslug}.html">{html_escape(rt['name'])}</a>
  <div style="font-size:0.75rem; color:var(--ash); margin-top:4px;">Track {rt['track_number']}</div>
</div>'''
        related_html += '</div>'

    html = page_header(title, desc, canonical, artwork, json.dumps(schema, indent=2))
    html += f"""
<header>
  <div class="site-name"><a href="../index.html">Dark Country Boy</a></div>
  <h1>{html_escape(song_name)}</h1>
  <p class="subtitle">Track {track_num} &bull; <a href="../albums/{album_slug}.html">{html_escape(album_name)}</a></p>
</header>

<div class="container">

  {f'<img class="album-art" src="{artwork}" alt="{html_escape(album_name)} — Dark Country Boy" loading="lazy" style="max-width:300px;">' if artwork else ''}

  {f'<p class="section-title" style="margin-top:24px;">Preview</p><audio controls preload="none"><source src="{preview_url}" type="audio/mpeg">Your browser does not support audio.</audio>' if preview_url else ''}

  <div style="margin:24px 0;">
    <a href="{apple_url}" class="btn btn-primary" target="_blank" rel="noopener">▶ Stream on Apple Music</a>
    <a href="{spotify_search}" class="btn" target="_blank" rel="noopener">♪ Find on Spotify</a>
    <a href="../albums/{album_slug}.html" class="btn">Full Album: {html_escape(album_name[:40])}</a>
  </div>

  <div class="bio-box">
    <strong>"{html_escape(song_name)}"</strong> is Track {track_num} from the album 
    <a href="../albums/{album_slug}.html">{html_escape(album_name)}</a> by <strong>Dark Country Boy</strong>. 
    {ARTIST_BIO_SHORT}
  </div>

  <div style="margin:32px 0;">
    <p class="section-title">Lyrics</p>
    <div class="bio-box" style="color:var(--ash); font-style:italic;">
      Lyrics for "{html_escape(song_name)}" — Available on Apple Music and Spotify.
      <br><br>
      <a href="{apple_url}" target="_blank" rel="noopener">View lyrics on Apple Music →</a>
    </div>
  </div>

  {related_html}

  <div style="margin-top:40px; padding-top:20px; border-top:1px solid #1a1a1a;">
    <a href="../albums/{album_slug}.html" class="btn">← Back to Album</a>
    <a href="../index.html" class="btn">Home</a>
  </div>

</div>
"""
    html += page_footer(album_name, album_slug)
    return html

def update_index_html(catalog):
    """Inject a discography section into the existing index.html."""
    with open(f'{BASE_DIR}/index.html', 'r') as f:
        content = f.read()

    # Build the discography grid
    album_cards = ''
    for album in catalog:
        slug = album['slug']
        name = album['album_name']
        artwork = album['artwork_url']
        tc = album['track_count']
        album_cards += f"""
    <div class="album-card">
      <a href="albums/{slug}.html">
        <img src="{artwork}" alt="{html_escape(name)}" loading="lazy" width="200" height="200">
        <div class="album-card-info">
          <div class="album-card-title">{html_escape(name[:60])}</div>
          <div class="album-card-meta">{tc} tracks</div>
        </div>
      </a>
    </div>"""

    discography_section = f"""
  <!-- DISCOGRAPHY — AUTO-GENERATED -->
  <section id="discography">
    <p class="section-title">Full Discography — {len(catalog)} Albums &bull; 1,481 Songs</p>
    <div class="album-grid">
      {album_cards}
    </div>
  </section>
  <!-- END DISCOGRAPHY -->"""

    # Inject CSS for album-grid/card if not present
    css_inject = """
    /* Album grid for discography */
    .album-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
      gap: 16px;
      margin-bottom: 40px;
    }
    .album-card {
      background: var(--dark);
      border: 1px solid #1a1a1a;
      transition: border-color 0.2s;
    }
    .album-card:hover { border-color: #8b2020; }
    .album-card a { display: block; text-decoration: none; }
    .album-card img { width: 100%; display: block; }
    .album-card-info { padding: 10px 12px; }
    .album-card-title { font-size: 0.8rem; color: #e8e8e8; line-height: 1.3; margin-bottom: 4px; }
    .album-card-meta { font-size: 0.7rem; color: #888; }"""

    # Insert CSS before </style>
    if '.album-grid' not in content:
        content = content.replace('</style>', css_inject + '\n  </style>', 1)

    # Remove existing discography section if present
    content = re.sub(r'<!-- DISCOGRAPHY — AUTO-GENERATED -->.*?<!-- END DISCOGRAPHY -->', 
                     '', content, flags=re.DOTALL)

    # Insert before </body>
    content = content.replace('</body>', discography_section + '\n\n</body>', 1)

    with open(f'{BASE_DIR}/index.html', 'w') as f:
        f.write(content)

    log.info("Updated index.html with discography section")

def generate_sitemap(catalog):
    urls = [f"{SITE_URL}/index.html", f"{SITE_URL}/albums/", f"{SITE_URL}/songs/"]
    
    for album in catalog:
        urls.append(f"{SITE_URL}/albums/{album['slug']}.html")
        for track in album['tracks']:
            urls.append(f"{SITE_URL}/songs/{slugify(track['name'])}.html")

    today = datetime.utcnow().strftime('%Y-%m-%d')
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f'  <url><loc>{url}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
    xml += '</urlset>\n'
    
    with open(f'{BASE_DIR}/sitemap.xml', 'w') as f:
        f.write(xml)
    log.info(f"Generated sitemap.xml with {len(urls)} URLs")

def generate_robots():
    content = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    with open(f'{BASE_DIR}/robots.txt', 'w') as f:
        f.write(content)
    log.info("Generated robots.txt")

def main():
    log.info("=== Dark Country Boy Site Generator ===")
    
    with open('/tmp/dcb_full_catalog.json') as f:
        catalog = json.load(f)
    
    log.info(f"Loaded {len(catalog)} albums")

    # Fix duplicate slugs by appending album_id
    from collections import Counter
    slug_counts = Counter(a['slug'] for a in catalog)
    seen_slugs = {}
    for album in catalog:
        s = album['slug']
        if slug_counts[s] > 1:
            # append last 6 digits of album_id
            album['slug'] = f"{s}-{str(album['album_id'])[-6:]}"
        seen_slugs[album['slug']] = True

    # Create directories
    os.makedirs(f'{BASE_DIR}/albums', exist_ok=True)
    os.makedirs(f'{BASE_DIR}/songs', exist_ok=True)

    # Build a song-slug → (track, album) index to avoid duplicates
    song_pages = {}  # slug -> (track, album)
    
    # Generate album pages
    album_count = 0
    for idx, album in enumerate(catalog):
        prev_a = catalog[idx - 1] if idx > 0 else None
        next_a = catalog[idx + 1] if idx < len(catalog) - 1 else None
        
        html = generate_album_page(album, prev_a, next_a)
        path = f"{BASE_DIR}/albums/{album['slug']}.html"
        with open(path, 'w') as f:
            f.write(html)
        album_count += 1

        # Index songs (handle duplicate slugs by appending album slug)
        for track in album['tracks']:
            s = slugify(track['name'])
            if s not in song_pages:
                song_pages[s] = (track, album)
            else:
                # Dedupe by adding album slug suffix
                deduped = f"{s}-{album['slug'][:20]}"
                song_pages[deduped] = (track, album)

        if album_count % 10 == 0:
            log.info(f"  Album pages: {album_count}/{len(catalog)}")

    log.info(f"Generated {album_count} album pages")

    # Generate song pages
    song_count = 0
    for slug, (track, album) in song_pages.items():
        # Related: other tracks from same album (excluding this one)
        related = [t for t in album['tracks'] if t['track_id'] != track['track_id']]
        # Pick 6 nearby tracks
        idx_in_album = next((i for i, t in enumerate(album['tracks']) if t['track_id'] == track['track_id']), 0)
        start = max(0, idx_in_album - 3)
        related_nearby = album['tracks'][start:start+6]
        related_nearby = [t for t in related_nearby if t['track_id'] != track['track_id']]

        html = generate_song_page(track, album, related_nearby)
        path = f"{BASE_DIR}/songs/{slug}.html"
        with open(path, 'w') as f:
            f.write(html)
        song_count += 1
        
        if song_count % 200 == 0:
            log.info(f"  Song pages: {song_count}/{len(song_pages)}")

    log.info(f"Generated {song_count} song pages")

    # Update index
    update_index_html(catalog)

    # Sitemap & robots
    generate_sitemap(catalog)
    generate_robots()

    log.info("\n=== DONE ===")
    log.info(f"Album pages: {album_count}")
    log.info(f"Song pages:  {song_count}")
    log.info(f"Output dir:  {BASE_DIR}")

if __name__ == '__main__':
    main()

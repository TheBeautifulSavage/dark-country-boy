#!/usr/bin/env python3
"""
Generate SEO song pages for Dark Country Boy YouTube videos.
Reads all_videos.json and creates /songs/[slug].html for each video.
"""

import json
import os
import re
from datetime import datetime

# Paths
VIDEOS_JSON = "/Users/mac1/OTR_Pipeline_New/music_promo/all_videos.json"
SITE_DIR = "/Users/mac1/Projects/dark-country-boy"
SONGS_DIR = os.path.join(SITE_DIR, "songs")
SITEMAP_PATH = os.path.join(SITE_DIR, "sitemap.xml")
SONGS_INDEX_PATH = os.path.join(SITE_DIR, "dark-country-boy-songs.html")
BASE_URL = "https://thebeautifulsavage.github.io/dark-country-boy"


def make_slug(title):
    """Convert title to URL slug."""
    # Remove parenthetical suffix like (Dark Country Music)
    clean = re.sub(r'\s*\([^)]*\)\s*$', '', title).strip()
    # Lowercase
    slug = clean.lower()
    # Replace & with and
    slug = slug.replace('&', 'and')
    # Replace spaces and special chars with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Strip leading/trailing hyphens
    slug = slug.strip('-')
    return slug


def clean_title(title):
    """Remove the (Dark Country Music) suffix for display."""
    return re.sub(r'\s*\(Dark Country Music\)\s*$', '', title).strip()


def generate_page(video, all_songs_data):
    """Generate HTML for a single song page."""
    vid_id = video['id']
    title = video['title']
    slug = make_slug(title)
    title_clean = clean_title(title)

    # Build song links JSON for the random grid (exclude current song)
    other_songs = [s for s in all_songs_data if s['id'] != vid_id]
    song_links = [{"url": f"../songs/{s['slug']}.html", "title": s['title_clean']} 
                  for s in other_songs]
    song_links_json = json.dumps(song_links)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_clean} - Dark Country Boy | Dark Country Music</title>
<meta name="description" content="Listen to {title_clean} by Dark Country Boy. Dark country music, southern gothic blues, and outlaw americana from the swamps of North Carolina.">
<meta property="og:title" content="{title_clean} - Dark Country Boy">
<meta property="og:description" content="Dark country music by Dark Country Boy. Stream {title_clean} now.">
<meta property="og:image" content="https://yt3.ggpht.com/rH5LSmvIZarBuckT1wfuhywgJAjXDqBmJXLJ5pAFt20Oysfo237AQ2ulD6CVFPnppDZU-ej2BKM=s800-c-k-c0x00ffffff-no-rj">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{BASE_URL}/songs/{slug}.html">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "MusicRecording",
  "name": "{title_clean}",
  "byArtist": {{
    "@type": "MusicGroup",
    "name": "Dark Country Boy",
    "url": "{BASE_URL}/"
  }},
  "url": "https://www.youtube.com/watch?v={vid_id}"
}}
</script>
<style>
body {{ font-family: Georgia, serif; background: #0d0d0d; color: #e0d5c5; max-width: 800px; margin: 0 auto; padding: 20px; }}
h1 {{ color: #c9a84c; font-size: 2em; }}
.video-wrap {{ position: relative; padding-bottom: 56.25%; height: 0; margin: 20px 0; }}
.video-wrap iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}
a {{ color: #c9a84c; }}
nav {{ margin-bottom: 20px; }}
.song-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 20px; }}
.song-grid a {{ display: block; padding: 8px; background: #1a1a1a; border-radius: 4px; text-decoration: none; font-size: 0.85em; }}
</style>
</head>
<body>
<nav><a href="../index.html">&larr; Dark Country Boy</a> | <a href="../dark-country-boy-songs.html">All Songs</a></nav>

<h1>{title_clean}</h1>
<p>A dark country anthem from <strong>Dark Country Boy</strong> &mdash; raw, gravel-soaked music from the swamps of North Carolina. This is dark country: outlaw blues, southern gothic ballads, and songs that sound like they were written at a midnight crossroads.</p>

<div class="video-wrap">
<iframe src="https://www.youtube.com/embed/{vid_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

<h2>Stream Dark Country Boy</h2>
<ul>
<li><a href="https://open.spotify.com/artist/4TQMuCjeTbhqvPinWKqRAv" target="_blank">Spotify &mdash; Dark Country Boy</a></li>
<li><a href="https://music.apple.com/us/artist/dark-country-boy/1818551005" target="_blank">Apple Music</a></li>
<li><a href="https://music.youtube.com/@darkcountryboy" target="_blank">YouTube Music</a></li>
<li><a href="https://www.youtube.com/@darkcountryboy" target="_blank">YouTube Channel</a></li>
</ul>

<h2>About Dark Country Boy</h2>
<p>Dark Country Boy crawled out of the deep, dark swamps of North Carolina &mdash; part Carolina swamp rat, part outlaw preacher. He sings gravel-soaked gospel for the forgotten and the damned. This ain&rsquo;t polished Nashville radio. This is dark country: swamp blues, outlaw hymns, southern gothic ballads, and murder songs written by candlelight in a broken-down chapel.</p>

<h2>More Songs</h2>
<div class="song-grid" id="more-songs"></div>

<script>
var songs = {song_links_json};
var grid = document.getElementById('more-songs');
songs.sort(function() {{ return Math.random() - 0.5; }}).slice(0,9).forEach(function(s) {{
  var a = document.createElement('a');
  a.href = s.url; a.textContent = s.title;
  grid.appendChild(a);
}});
</script>
</body>
</html>"""
    return slug, html


def update_sitemap(new_slugs):
    """Add new song URLs to sitemap.xml if not already present."""
    today = datetime.now().strftime('%Y-%m-%d')
    
    with open(SITEMAP_PATH, 'r') as f:
        content = f.read()
    
    # Find existing URLs
    existing = set(re.findall(r'<loc>(.*?)</loc>', content))
    
    new_entries = []
    for slug in new_slugs:
        url = f"{BASE_URL}/songs/{slug}.html"
        if url not in existing:
            new_entries.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""")
    
    if new_entries:
        insert_block = '\n'.join(new_entries)
        content = content.replace('</urlset>', f'{insert_block}\n</urlset>')
        with open(SITEMAP_PATH, 'w') as f:
            f.write(content)
        print(f"  Added {len(new_entries)} new URLs to sitemap")
    else:
        print("  All URLs already in sitemap")
    
    return len(new_entries)


def update_songs_index(all_songs_data):
    """Update dark-country-boy-songs.html with all 100 video songs."""
    today = datetime.now().strftime('%B %d, %Y')
    
    # Build song list items
    song_items = []
    for s in sorted(all_songs_data, key=lambda x: x['title_clean']):
        song_items.append(
            f'<li><a href="songs/{s["slug"]}.html">{s["title_clean"]}</a></li>'
        )
    songs_list = '\n'.join(song_items)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dark Country Boy Songs — Full Catalog | Dark Country Music</title>
<meta name="description" content="Complete song catalog for Dark Country Boy. 100+ dark country music tracks — outlaw blues, southern gothic ballads, and swamp americana from North Carolina.">
<link rel="canonical" href="{BASE_URL}/dark-country-boy-songs.html">
<style>
body {{ font-family: Georgia, serif; background: #0d0d0d; color: #e0d5c5; max-width: 900px; margin: 0 auto; padding: 20px; }}
h1 {{ color: #c9a84c; font-size: 2.2em; }}
h2 {{ color: #c9a84c; }}
a {{ color: #c9a84c; }}
nav {{ margin-bottom: 20px; }}
.song-list {{ columns: 2; gap: 40px; list-style: none; padding: 0; }}
.song-list li {{ margin-bottom: 8px; break-inside: avoid; }}
.song-list a {{ text-decoration: none; font-size: 0.95em; }}
.song-list a:hover {{ text-decoration: underline; }}
.count {{ color: #888; font-style: italic; margin-bottom: 20px; }}
</style>
</head>
<body>
<nav><a href="index.html">&larr; Dark Country Boy Home</a></nav>

<h1>Dark Country Boy — Songs</h1>
<p class="count">YouTube video catalog — {len(all_songs_data)} songs &mdash; Updated {today}</p>

<p>Dark Country Boy's complete YouTube catalog. Raw, gravel-soaked dark country music from the swamps of North Carolina — outlaw blues, southern gothic ballads, and murder songs written at a midnight crossroads.</p>

<h2>Full Song List</h2>
<ul class="song-list">
{songs_list}
</ul>

<h2>Stream Dark Country Boy</h2>
<ul>
<li><a href="https://open.spotify.com/artist/4TQMuCjeTbhqvPinWKqRAv" target="_blank">Spotify</a></li>
<li><a href="https://music.apple.com/us/artist/dark-country-boy/1818551005" target="_blank">Apple Music</a></li>
<li><a href="https://www.youtube.com/@darkcountryboy" target="_blank">YouTube Channel</a></li>
</ul>

</body>
</html>"""
    
    with open(SONGS_INDEX_PATH, 'w') as f:
        f.write(html)
    print(f"  Updated dark-country-boy-songs.html with {len(all_songs_data)} songs")


def main():
    print("Loading videos from all_videos.json...")
    with open(VIDEOS_JSON, 'r') as f:
        videos = json.load(f)
    print(f"  Loaded {len(videos)} videos")

    # Pre-compute slugs and clean titles
    all_songs_data = []
    for v in videos:
        s = make_slug(v['title'])
        all_songs_data.append({
            'id': v['id'],
            'title': v['title'],
            'title_clean': clean_title(v['title']),
            'slug': s,
        })

    # Check for duplicate slugs
    slugs = [s['slug'] for s in all_songs_data]
    seen = {}
    for i, slug in enumerate(slugs):
        if slug in seen:
            # Append index to deduplicate
            all_songs_data[i]['slug'] = f"{slug}-{i}"
        seen[slug] = i

    # Create songs directory
    os.makedirs(SONGS_DIR, exist_ok=True)
    print(f"  Songs directory: {SONGS_DIR}")

    # Generate pages
    print("Generating song pages...")
    generated = []
    skipped = []
    for video_data in all_songs_data:
        slug = video_data['slug']
        output_path = os.path.join(SONGS_DIR, f"{slug}.html")
        
        # Find original video entry
        video = next(v for v in videos if v['id'] == video_data['id'])
        
        _, html = generate_page(video, all_songs_data)
        
        with open(output_path, 'w') as f:
            f.write(html)
        generated.append(slug)
        print(f"  ✓ {slug}.html")

    print(f"\nGenerated {len(generated)} pages, skipped {len(skipped)}")

    # Update sitemap
    print("\nUpdating sitemap.xml...")
    added = update_sitemap([s['slug'] for s in all_songs_data])

    # Update songs index
    print("\nUpdating dark-country-boy-songs.html...")
    update_songs_index(all_songs_data)

    print("\n✅ Done!")
    return generated, all_songs_data


if __name__ == '__main__':
    main()

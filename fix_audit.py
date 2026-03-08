import os
import re
import shutil
import json

base_dir = r"c:\Users\RAVELLO CAMACHO\Documents\GitHub\Katsudomo"

# 1. DELETE ENGLISH VERSION
en_dir = os.path.join(base_dir, "en")
if os.path.exists(en_dir):
    shutil.rmtree(en_dir)

# Helper for finding all HTML
def get_all_html():
    res = []
    for root, _, files in os.walk(base_dir):
        if "\\.git" in root or "\\node_modules" in root: continue
        for f in files:
            if f.endswith('.html'):
                res.append(os.path.join(root, f))
    return res

html_files = get_all_html()

# 2. HREFLANG FIXER
# Every page needs:
# <link rel="canonical" href="https://www.katsudomo.com/PATH">
# <link rel="alternate" hreflang="x-default" href="https://www.katsudomo.com/PATH_ES">
# <link rel="alternate" hreflang="es" href="https://www.katsudomo.com/PATH_ES">
# <link rel="alternate" hreflang="ja" href="https://www.katsudomo.com/ja/PATH_JA">

for fp in html_files:
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the canonical URL to determine the page's identity
    canon_m = re.search(r'<link rel="canonical" href="([^"]+)">', content)
    if not canon_m: continue
    canonical_url = canon_m.group(1)
    
    # Clean up the canonical if it mistakenly has a trailing slash for files (e.g. cultura-japonesa-peru/)
    if canonical_url.endswith('/') and not canonical_url.endswith('.com/') and 'ja/' not in canonical_url[-4:]:
         # Let's be careful. Let's just manually replace known bad ones below
         pass

    # Clean existing alternates
    content = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?\s*', '', content)

    # Let's build the correct block based on relative file path
    rel_path = os.path.relpath(fp, base_dir).replace('\\', '/')
    
    # Determine ES and JA paths
    es_path = rel_path
    ja_path = f"ja/{rel_path}"
    if rel_path.startswith("ja/"):
        es_path = rel_path[3:]
        ja_path = rel_path
        
    if es_path == "index.html":
        es_url = "https://www.katsudomo.com/"
        ja_url = "https://www.katsudomo.com/ja/"
    else:
        es_url = f"https://www.katsudomo.com/{es_path}"
        ja_url = f"https://www.katsudomo.com/{ja_path}"
        
    # We rebuild just below canonical
    correct_hreflang = f"""
    <link rel="alternate" hreflang="x-default" href="{es_url}">
    <link rel="alternate" hreflang="es" href="{es_url}">
    <link rel="alternate" hreflang="ja" href="{ja_url}">
"""
    content = re.sub(r'(<link rel="canonical" href="[^"]+">)', r'\1' + correct_hreflang, content)
    
    # 3. FIX BROKEN LINKS & PATHS (Global Replace)
    content = content.replace('"cultura-japonesa-peru/index.html"', '"cultura-japonesa-peru.html"')
    content = content.replace('="../cultura-japonesa-peru/index.html"', '="../cultura-japonesa-peru.html"')
    content = content.replace('href="carta.html"', 'href="menu/carta.html"') # in root navbar
    
    # Fix OG URL in cultura
    if "cultura-japonesa-peru" in rel_path:
        content = content.replace('content="https://www.katsudomo.com/cultura-japonesa-peru/"', 'content="https://www.katsudomo.com/cultura-japonesa-peru.html"')
        content = content.replace('content="https://www.katsudomo.com/ja/cultura-japonesa-peru/"', 'content="https://www.katsudomo.com/ja/cultura-japonesa-peru.html"')

    # Fix OG Images
    content = content.replace('hero_bg_1772917275063.png', 'hero-comida-callejera-japonesa-trujillo.webp')
    content = content.replace('katsudon_1772917287927.png', 'katsudon-clasico-comida-japonesa-trujillo.webp')
    content = content.replace('cultura-hero.webp', 'hero-comida-callejera-japonesa-trujillo.webp') 
    
    # Fix menu paths: The file names in the audit were slightly off. Let's make sure they load the correct SEO images
    # We should point everything to the renamed ones in images/solocultura/ or images/
    # If the file is menu/carta.html, image paths are like "../images/katsudon.webp", so:
    content = content.replace('"../images/obento-menchikatsu-comida-japonesa-trujillo.webp"', '"../images/solocultura/bento-menchikatsu-comida-japonesa-trujillo.webp"')
    content = content.replace('"../images/buta-yakisoba-comida-callejera-japonesa-trujillo.webp"', '"../images/solocultura/buta-yakisoba-street-food-japonesa-trujillo.webp"')
    content = content.replace('"../images/mini-obento-menchikatsu-comida-japonesa-trujillo.webp"', '"../images/solocultura/mini-bento-menchikatsu-comidas-en-trujillo.webp"')
    # If it was still looking for old names
    content = content.replace('obento-menchi-katsu.webp', 'solocultura/bento-menchikatsu-comida-japonesa-trujillo.webp')
    content = content.replace('akira-combo-takoyaki.webp', 'solocultura/takoyaki-box-comida-callejera-japonesa-trujillo.webp')
    content = content.replace('buta-yakisoba.webp', 'solocultura/buta-yakisoba-street-food-japonesa-trujillo.webp')
    content = content.replace('mini-obento-menchi-katsu.webp', 'solocultura/mini-bento-menchikatsu-comidas-en-trujillo.webp')
    # Actually just replace the menu katsudon
    content = re.sub(r'images/katsudon\.webp', r'images/katsudon-comida-japonesa-trujillo.webp', content)

    # Clean up index breadcrumb list schema (Home shouldn't have one usually, or just Home)
    if es_path == "index.html":
        # Delete breadcrumblist from index
        content = re.sub(r',?\s*\{\s*"@type":\s*"BreadcrumbList"[\s\S]*?\]\s*\}', '', content)
    
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)

print("Hreflang, Links, and English removal completed.")

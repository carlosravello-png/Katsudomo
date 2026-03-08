import os
import re
from PIL import Image

base_dir = r"c:\Users\RAVELLO CAMACHO\Documents\GitHub\Katsudomo"

# 1. FIX ABOUT SECTION CSS PADDING ON MOBILE
css_path = os.path.join(base_dir, "css", "style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

if ".about-section" not in css_content:
    css_fix = """
/* About Section Fixes */
.about-section {
    padding: 80px 10%;
    max-width: 1400px;
    margin: 0 auto;
}
.brand-manifesto p {
    margin-bottom: 1.5rem;
}
@media (max-width: 768px) {
    .about-section {
        padding: 50px 25px;
    }
}
"""
    # Simply append to the end of the file since it has top level precedence for this class
    with open(css_path, "a", encoding="utf-8") as f:
        f.write("\n" + css_fix)

# 2. DEFER FONTAWESOME TO FIX RENDER BLOCKING 1.3s
target_link = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">'
async_link = '<link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"></noscript>'

# Also fix the preload warning for Preconnect
preconnect1 = '<link rel="preconnect" href="https://fonts.googleapis.com">'
preconnect2 = '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'

html_files = []
for root, _, files in os.walk(base_dir):
    if "\\.git" in root or "\\node_modules" in root: continue
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root, f))

for fp in html_files:
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Render blocking fix
    if target_link in content:
        content = content.replace(target_link, async_link)
        
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)

# 3. OPTIMIZE HEAVY IMAGES (Resize logo and big marquee image to save 500KB+)
logo_path = os.path.join(base_dir, "images", "katsudomo-street-food-japonesa-trujillo.webp")
if os.path.exists(logo_path):
    try:
        img = Image.open(logo_path)
        if img.width > 600:
            ratio = 600.0 / float(img.width)
            new_height = int(float(img.height) * float(ratio))
            img = img.resize((600, new_height), Image.Resampling.LANCZOS)
            img.save(logo_path, format="WEBP", quality=85)
            print(f"Resized Logo to 600px width.")
    except Exception as e:
        print(f"Error resizing logo: {e}")

yaki_path = os.path.join(base_dir, "images", "solocultura", "yakisoba-clasico-street-food-japonesa-trujillo.webp")
if os.path.exists(yaki_path):
    try:
        img = Image.open(yaki_path)
        if img.width > 800:
            ratio = 800.0 / float(img.width)
            new_height = int(float(img.height) * float(ratio))
            img = img.resize((800, new_height), Image.Resampling.LANCZOS)
            img.save(yaki_path, format="WEBP", quality=80)
            print(f"Resized Yakisoba to 800px width.")
    except Exception as e:
        print(f"Error resizing yakisoba: {e}")

print("Fixes aplied successfully.")

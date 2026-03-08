import re
import glob

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    def replacer(match):
        img_tag = match.group(0)
        # Skip nav-logo
        if 'class="nav-logo"' in img_tag or 'loading="lazy"' in img_tag:
            return img_tag
        # Add loading="lazy" before the closing bracket
        return img_tag[:-1] + ' loading="lazy">'
        
    new_html = re.sub(r'<img[^>]+>', replacer, html)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

process_file('index.html')
process_file('ja/index.html')
print("Hecho.")

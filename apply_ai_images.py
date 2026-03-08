import os
import shutil

src_dir = r"C:\Users\RAVELLO CAMACHO\.gemini\antigravity\brain\c777b0fd-cb75-47ce-97c6-2bc70cd8ce56"
dest_dir = r"C:\Users\RAVELLO CAMACHO\Documents\GitHub\Katsudomo\images\solocultura"
base_dir = r"C:\Users\RAVELLO CAMACHO\Documents\GitHub\Katsudomo"

filenames = [
    "historia_inmigracion_1899_1772943416509.png",
    "shokunin_manos_1772943444133.png",
    "cocina_nikkei_1772943467235.png",
    "yatai_matsuri_1772943491936.png",
    "trujillo_dark_kitchen_1772943517413.png"
]

for f in filenames:
    src_f = os.path.join(src_dir, f)
    # Check if we need to fall back to the generic name without timestamp if it was named differently? No, the names are exact.
    if os.path.exists(src_f):
        shutil.copy2(src_f, os.path.join(dest_dir, f))

# HTML Injection
replacements_es = {
    '<div class="historia_inmigracion_visual"></div>': f'<img src="images/solocultura/{filenames[0]}" alt="Inmigrantes japoneses llegando a Perú en 1899, barco Sakura Maru, histórica foto sepia de estilo documental." class="article-image" loading="lazy">',
    '<div class="shokunin_visual"></div>': f'<img src="images/solocultura/{filenames[1]}" alt="Manos de maestro shokunin preparando arroz de forma artesanal, maestría y filosofía." class="article-image" loading="lazy">',
    '<div class="cocina_nikkei_visual"></div>': f'<img src="images/solocultura/{filenames[2]}" alt="Cocina nikkei, wok tradicional japonés y ají amarillo peruano fundiéndose en un ambiente oscuro." class="article-image" loading="lazy">',
    '<div class="yatai_matsuri_visual"></div>': f'<img src="images/solocultura/{filenames[3]}" alt="Puesto callejero yatai japonés de noche, wok en llamas, linternas rojas lluviosas." class="article-image" loading="lazy">',
    '<div class="trujillo_encuentro_visual"></div>': f'<img src="images/solocultura/{filenames[4]}" alt="Dark kitchen asiática en Trujillo, vapor saliendo de comida recién preparada, luces tenues y cálidas." class="article-image" loading="lazy">'
}

replacements_ja = {
    '<div class="historia_inmigracion_visual"></div>': f'<img src="../images/solocultura/{filenames[0]}" alt="1899年、ペルーに到着する日本人移民、桜丸。" class="article-image" loading="lazy">',
    '<div class="shokunin_visual"></div>': f'<img src="../images/solocultura/{filenames[1]}" alt="職人の手による丁寧な仕込み、おにぎり。" class="article-image" loading="lazy">',
    '<div class="cocina_nikkei_visual"></div>': f'<img src="../images/solocultura/{filenames[2]}" alt="日系料理の誕生、中華鍋とペルーの黄色い唐辛子。" class="article-image" loading="lazy">',
    '<div class="yatai_matsuri_visual"></div>': f'<img src="../images/solocultura/{filenames[3]}" alt="夜の日本の屋台、炎と提灯。" class="article-image" loading="lazy">',
    '<div class="trujillo_encuentro_visual"></div>': f'<img src="../images/solocultura/{filenames[4]}" alt="トルヒーヨのアジア風ダークキッチン、湯気が立つ出来立ての料理。" class="article-image" loading="lazy">'
}

files = [
    (os.path.join(base_dir, "cultura-japonesa-peru.html"), replacements_es),
    (os.path.join(base_dir, "ja", "cultura-japonesa-peru.html"), replacements_ja)
]

for file_path, reps in files:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f: html = f.read()
        for old, new in reps.items():
            html = html.replace(old, new)
        with open(file_path, "w", encoding="utf-8") as f: f.write(html)

print("Images copied and injected into the HTMLs.")

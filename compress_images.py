import os
import glob
from PIL import Image

def compress_webp(input_path, output_path, quality=65):
    try:
        with Image.open(input_path) as img:
            # We preserve the original dimensions but compress the bits
            img.save(output_path, "webp", quality=quality, method=6)
        return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def main():
    images = glob.glob('images/**/*.webp', recursive=True)
    total_saved = 0
    print(f"Encontradas {len(images)} imágenes WebP.")
    
    for img_path in images:
        original_size = os.path.getsize(img_path)
        
        # We will save to a temporary file, check if it's smaller, and replace
        temp_path = img_path + ".tmp.webp"
        
        if compress_webp(img_path, temp_path, quality=65):
            new_size = os.path.getsize(temp_path)
            
            # Only replace if we saved at least 15% to avoid losing quality unnecessarily
            if new_size < original_size * 0.85:
                saved_kb = (original_size - new_size) / 1024
                total_saved += saved_kb
                os.replace(temp_path, img_path)
                print(f"Comprimida {img_path}: {original_size/1024:.1f}KB -> {new_size/1024:.1f}KB (-{saved_kb:.1f}KB)")
            else:
                os.remove(temp_path)
                print(f"Omitida {img_path}: No amerita compresión extra.")
                
    print(f"\n¡Proceso finalizado! Total ahorrado: {total_saved/1024:.2f} MB")

if __name__ == "__main__":
    main()

import os
import json
import glob
from PIL import Image

RAW_DIR = "raw_wallpapers"
OUT_DIR = "wallpapers"
JSON_FILE = "content.json"

def process_images():
    """
    Mengonversi gambar (.jpg, .jpeg, .png) dari folder raw_wallpapers/
    ke format .webp (kualitas 80%) dan menyimpannya ke folder wallpapers/.
    """
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
        
    for ext in ('*.jpg', '*.jpeg', '*.png'):
        for filepath in glob.glob(os.path.join(RAW_DIR, ext)):
            filename = os.path.basename(filepath)
            name, _ = os.path.splitext(filename)
            out_filepath = os.path.join(OUT_DIR, f"{name}.webp")
            
            # Hanya konversi jika file belum ada untuk menghemat waktu
            if not os.path.exists(out_filepath):
                print(f"Mengonversi {filepath} ke {out_filepath}...")
                try:
                    with Image.open(filepath) as img:
                        # Jika gambar punya mode RGBA (transparan) simpan apa adanya,
                        # jika RGB simpan ke WEBP. Convert mode agar aman.
                        if img.mode not in ('RGB', 'RGBA'):
                            img = img.convert('RGBA')
                        img.save(out_filepath, "webp", quality=80)
                except Exception as e:
                    print(f"Error saat mengonversi {filepath}: {e}")

def update_content_json():
    """
    Membaca semua file .webp di folder wallpapers/ dan
    memperbarui atau membuat file content.json dengan struktur yang diinginkan.
    """
    content = {
        "wallpapers": [],
        "guides": [],
        "admob_config": {
            "app_id": "",
            "open_ads": "",
            "interstitial": "",
            "rewarded": "",
            "banner": "",
            "native": ""
        }
    }
    
    # Load JSON yang sudah ada jika ada, supaya data guides dan admob_config tidak hilang
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            try:
                existing_content = json.load(f)
                content.update(existing_content)
            except json.JSONDecodeError:
                print("Error membaca content.json yang lama. Membuat file baru.")
                
    # Update daftar wallpaper berdasarkan file .webp yang ada di folder wallpapers/
    wallpapers_list = []
    if os.path.exists(OUT_DIR):
        for filepath in sorted(glob.glob(os.path.join(OUT_DIR, '*.webp'))):
            filename = os.path.basename(filepath)
            name, _ = os.path.splitext(filename)
            
            # Membuat title dasar dari nama file (misal: "my-wallpaper" jadi "My Wallpaper")
            title = name.replace('_', ' ').replace('-', ' ').title()
            
            wallpapers_list.append({
                "id": name,
                "title": title,
                "image_url": f"wallpapers/{filename}"
            })
            
    content["wallpapers"] = wallpapers_list
    
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2)
    print("Berhasil memperbarui content.json")

if __name__ == "__main__":
    if os.path.exists(RAW_DIR):
        process_images()
    else:
        print(f"Folder {RAW_DIR} tidak ditemukan. Melewati konversi gambar.")
        
    update_content_json()

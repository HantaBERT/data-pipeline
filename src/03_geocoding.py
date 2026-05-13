import os
import time
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def get_coordinates():
    print("Membaca data interim...")
    df = pd.read_csv("data/interim/interim_hantavirus.csv")
    
    # Tambahkan timeout=10 agar tidak mudah putus saat server lambat
    geolocator = Nominatim(user_agent="hantabert_pipeline_v2", timeout=10)
    # Tambahkan delay 1.5 detik per request agar lebih aman dari blokir Nominatim
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.5, swallow_exceptions=True)
    
    unique_locations = df['lokasi_geografis_name'].unique()
    total_locs = len(unique_locations)
    print(f"Ditemukan {total_locs} lokasi unik. Memulai proses geocoding...")
    
    location_dict = {}
    
    for i, loc in enumerate(unique_locations):
        if pd.isna(loc) or str(loc).lower() == 'unknown':
            location_dict[loc] = None
            continue
            
        clean_loc = str(loc).split(':')[0].split('|')[0].strip() # Ambil teks paling depan saja agar lebih mudah dicari map
        
        try:
            print(f"[{i+1}/{total_locs}] Mencari koordinat untuk: {clean_loc}...")
            location = geocode(clean_loc)
            if location:
                location_dict[loc] = f"{location.latitude},{location.longitude}"
            else:
                location_dict[loc] = None
        except Exception as e:
            print(f"Gagal mencari {clean_loc}: {e}")
            location_dict[loc] = None
            time.sleep(2) # Jeda ekstra jika kena error
    
    print("Memetakan koordinat ke dataset utama...")
    df['lokasi_geografis_koordinat'] = df['lokasi_geografis_name'].map(location_dict)
    
    print("Menyimpan hasil final...")
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/final_hantavirus_dataset.csv", index=False)
    print("Selesai! File final telah dibuat.")

if __name__ == "__main__":
    get_coordinates()
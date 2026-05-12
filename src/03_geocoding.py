import os
import time
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def get_coordinates():
    df = pd.read_csv("data/interim/interim_hantavirus.csv")
    
    geolocator = Nominatim(user_agent="hantabert_pipeline")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    unique_locations = df['lokasi_geografis_name'].unique()
    location_dict = {}
    
    for loc in unique_locations:
        if pd.isna(loc) or str(loc).lower() == 'unknown':
            location_dict[loc] = None
            continue
            
        clean_loc = str(loc).split(':')[0].strip()
        try:
            location = geocode(clean_loc)
            if location:
                location_dict[loc] = f"{location.latitude},{location.longitude}"
            else:
                location_dict[loc] = None
        except Exception:
            location_dict[loc] = None
            time.sleep(1)
    
    df['lokasi_geografis_koordinat'] = df['lokasi_geografis_name'].map(location_dict)
    
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/final_hantavirus_dataset.csv", index=False)

if __name__ == "__main__":
    get_coordinates()
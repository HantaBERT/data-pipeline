import os
import pandas as pd

def clean_host(raw_host):
    host_str = str(raw_host).lower()
    if 'homo sapiens' in host_str or 'human' in host_str:
        return 'Human'
    elif any(x in host_str for x in ['rattus', 'mus', 'apodemus', 'myodes', 'microtus', 'peromyscus', 'sigmodon', 'rodent', 'mouse', 'rat', 'vole']):
        return 'Rodent'
    elif host_str == 'unknown':
        return 'Unknown'
    return 'Others'

def clean_geography(raw_geo):
    geo_str = str(raw_geo).split(':')[0].strip().lower()
    americas = ['usa', 'united states', 'canada', 'brazil', 'argentina', 'chile', 'paraguay', 'uruguay', 'mexico', 'bolivia']
    europe = ['germany', 'france', 'uk', 'united kingdom', 'sweden', 'finland', 'russia', 'belgium', 'netherlands', 'spain', 'italy', 'norway']
    asia = ['china', 'south korea', 'japan', 'taiwan', 'india', 'indonesia', 'vietnam', 'malaysia', 'thailand']
    
    if any(country in geo_str for country in americas):
        return 'Americas'
    elif any(country in geo_str for country in europe):
        return 'Europe'
    elif any(country in geo_str for country in asia):
        return 'Asia'
    elif geo_str == 'unknown':
        return 'Unknown'
    return 'Others'

def process_labels():
    df = pd.read_csv("data/raw/raw_hantavirus_ncbi.csv")
    
    df = df[df['sequence_length'] >= 200].copy()
    
    df['host_label'] = df['raw_host'].apply(clean_host)
    df['geo_label_broad'] = df['lokasi_geografis_name'].apply(clean_geography)
    
    os.makedirs("data/interim", exist_ok=True)
    df.to_csv("data/interim/interim_hantavirus.csv", index=False)

if __name__ == "__main__":
    process_labels()
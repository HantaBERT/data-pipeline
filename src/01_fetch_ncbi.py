import os
import time
import pandas as pd
from Bio import Entrez, SeqIO

Entrez.email = "rafidhiyaulh@gmail.com"

def fetch_hantavirus_data():
    search_term = '"Orthohantavirus"[Organism] AND ("segment S" OR "segment M" OR "segment L")'
    
    try:
        handle = Entrez.esearch(db="nucleotide", term=search_term, retmax=10000)
        record = Entrez.read(handle)
        handle.close()
        id_list = record["IdList"]
        total_ids = len(id_list)
    except Exception:
        return

    batch_size = 50
    data_list = []

    for start in range(0, total_ids, batch_size):
        end = min(total_ids, start + batch_size)
        batch_ids = id_list[start:end]
        
        try:
            fetch_handle = Entrez.efetch(db="nucleotide", id=batch_ids, rettype="gb", retmode="text")
            records = list(SeqIO.parse(fetch_handle, "genbank"))
            fetch_handle.close()
            
            for seq_record in records:
                organism = "Unknown"
                host = "Unknown"
                country = "Unknown"
                segment = "Unknown"
                
                for feature in seq_record.features:
                    if feature.type == "source":
                        organism = feature.qualifiers.get('organism', [organism])[0]
                        host = feature.qualifiers.get('host', [host])[0]
                        country = feature.qualifiers.get('country', [country])[0]
                        segment = feature.qualifiers.get('segment', [segment])[0]
                        break
                        
                data_list.append({
                    "accession_id": seq_record.id,
                    "species_label": organism,
                    "raw_host": host,
                    "lokasi_geografis_name": country,
                    "segment_type": segment,
                    "sequence_length": len(seq_record.seq),
                    "sequence": str(seq_record.seq)
                })
                
            time.sleep(1)
            
        except Exception:
            continue

    os.makedirs("data/raw", exist_ok=True)
    pd.DataFrame(data_list).to_csv("data/raw/raw_hantavirus_ncbi.csv", index=False)

if __name__ == "__main__":
    fetch_hantavirus_data()
# HantaBERT Data Pipeline

This repository is responsible for the entire process of collecting, cleaning, and standardizing Orthohantavirus genomic data for the HantaBERT project. The pipeline automates data extraction from NCBI GenBank to produce a ready-to-use dataset for machine learning.

## Key Features
* **Extraction Automation:** Uses Biopython to fetch thousands of RNA sequences (S, M, L) and related metadata in batches from the NCBI database.
* **Multi-task Labeling:** Standardizes host, species, and geography labels from unstructured raw data.
* **Geocoding:** Integrates with the Nominatim API to convert country names into geographical coordinates.
* **Quality Control:** Filters sequences based on minimum length and metadata completeness.

## Data Structure
The final output is `final_hantavirus_dataset.csv`, which includes:
* `accession_id`: Unique NCBI ID.
* `host_label`: Host classification (Human, Rodent, Others).
* `geo_label_broad`: Regional classification (Americas, Europe, Asia).
* `sequence`: Pure RNA nucleotide sequence.
* `lokasi_geografis_koordinat`: Lat/Lon points for map visualization.

## Preparation & Installation
Use Python 3.12+ (using a MacBook Air M4 is recommended for local processing speed).

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to Run the Pipeline
Run the scripts sequentially according to the data dependency flow:
1. `python src/01_fetch_ncbi.py`: Fetches raw data.
2. `python src/02_clean_labels.py`: Cleans data and generates labels.
3. `python src/03_geocoding.py`: Determines location coordinates.

Open `notebooks/eda_hantavirus.ipynb` to view the data distribution analysis.

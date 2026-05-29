---
license: apache-2.0
pretty_name: HantaBERT Orthohantavirus Genomic Dataset
language:
- en
tags:
- biology
- genomics
- virology
- hantavirus
- orthohantavirus
- nucleotide-sequence
- rna
- ncbi
- genbank
task_categories:
- text-classification
size_categories:
- 1K<n<10K
annotations_creators:
- machine-generated
language_creators:
- found
source_datasets:
- original
configs:
- config_name: default
  data_files:
  - split: train
    path: data/processed/final_hantavirus_dataset.csv
- config_name: raw
  data_files:
  - split: train
    path: data/raw/raw_hantavirus_ncbi.csv
- config_name: interim
  data_files:
  - split: train
    path: data/interim/interim_hantavirus.csv
dataset_info:
- config_name: default
  features:
  - name: accession_id
    dtype: string
  - name: species_label
    dtype: string
  - name: raw_host
    dtype: string
  - name: lokasi_geografis_name
    dtype: string
  - name: segment_type
    dtype: string
  - name: sequence_length
    dtype: int64
  - name: sequence
    dtype: string
  - name: host_label
    dtype:
      class_label:
        names:
          '0': Rodent
          '1': Human
          '2': Others
          '3': Unknown
  - name: geo_label_broad
    dtype:
      class_label:
        names:
          '0': Others
          '1': Europe
          '2': Americas
          '3': Asia
          '4': Unknown
  - name: lokasi_geografis_koordinat
    dtype: string
  splits:
  - name: train
    num_examples: 9846
- config_name: raw
  features:
  - name: accession_id
    dtype: string
  - name: species_label
    dtype: string
  - name: raw_host
    dtype: string
  - name: lokasi_geografis_name
    dtype: string
  - name: segment_type
    dtype: string
  - name: sequence_length
    dtype: int64
  - name: sequence
    dtype: string
  splits:
  - name: train
    num_examples: 9950
- config_name: interim
  features:
  - name: accession_id
    dtype: string
  - name: species_label
    dtype: string
  - name: raw_host
    dtype: string
  - name: lokasi_geografis_name
    dtype: string
  - name: segment_type
    dtype: string
  - name: sequence_length
    dtype: int64
  - name: sequence
    dtype: string
  - name: host_label
    dtype: string
  - name: geo_label_broad
    dtype: string
  splits:
  - name: train
    num_examples: 9846
---

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
Use Python 3.12+

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

## Dataset Card

### Configurations
The Hub exposes three configurations matching the pipeline stages:

| Config | File | Rows | Description |
| --- | --- | --- | --- |
| `default` | `data/processed/final_hantavirus_dataset.csv` | 9,846 | Fully cleaned, labeled, and geocoded data (recommended). |
| `raw` | `data/raw/raw_hantavirus_ncbi.csv` | 9,950 | Unprocessed records as fetched from NCBI GenBank. |
| `interim` | `data/interim/interim_hantavirus.csv` | 9,846 | Cleaned and labeled, prior to geocoding. |

### Usage
```python
from datasets import load_dataset

# Recommended processed split
ds = load_dataset("<namespace>/<dataset-name>")  # config "default"

# Or load a specific pipeline stage
raw = load_dataset("<namespace>/<dataset-name>", "raw")
interim = load_dataset("<namespace>/<dataset-name>", "interim")
```

### Data Fields
- `accession_id` (string): Unique NCBI GenBank accession ID.
- `species_label` (string): Orthohantavirus species (e.g. *Orthohantavirus andesense*).
- `raw_host` (string): Original host annotation from the source record (e.g. *Homo sapiens*).
- `lokasi_geografis_name` (string): Raw strain/location string from the source record.
- `segment_type` (string): RNA genome segment — `S`, `M`, or `L`.
- `sequence_length` (int64): Nucleotide length of the sequence.
- `sequence` (string): Nucleotide sequence (A/C/G/T).
- `host_label` (string, `default`/`interim` only): Standardized host class — `Human`, `Rodent`, `Others`, `Unknown`.
- `geo_label_broad` (string, `default`/`interim` only): Broad region — `Americas`, `Europe`, `Asia`, `Others`, `Unknown`.
- `lokasi_geografis_koordinat` (string, `default` only): `lat, lon` coordinates from Nominatim geocoding (empty when unresolved).

### Label Distribution (`default`, n=9,846)
- **host_label:** Rodent 6,451 · Human 1,495 · Others 1,321 · Unknown 579
- **geo_label_broad:** Others 9,505 · Europe 255 · Unknown 51 · Americas 22 · Asia 13
- **segment_type:** S 4,175 · L 2,931 · M 2,729 (plus a few unnormalized variants)
- **coordinates resolved:** 2,535 / 9,846 rows

### Source & Curation
Sequences and metadata are fetched from [NCBI GenBank](https://www.ncbi.nlm.nih.gov/genbank/)
via Biopython, then standardized (host/species/geography labels), quality-filtered
(minimum length and metadata completeness), and geocoded with the
[Nominatim](https://nominatim.org/) API. See `src/` for the reproducible pipeline.

### Considerations
- Labels are machine-generated heuristics from unstructured source metadata and may contain noise.
- Classes are imbalanced (notably `geo_label_broad`, dominated by `Others`); account for this when training.
- The underlying records originate from NCBI GenBank and are subject to GenBank's terms of use.

### Licensing
This dataset and pipeline are released under the **Apache-2.0** license.

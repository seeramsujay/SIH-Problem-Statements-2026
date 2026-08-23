# Smart India Hackathon (SIH) 2026 - Problem Statements Dataset

A structured and cleaned dataset of all **226 problem statements** released for the **Smart India Hackathon (SIH) 2026**.

This repository contains the complete dataset parsed from the official portal with full details including problem titles, categories, assigned themes, ministry/organization details, complete descriptions, idea submission quotas, deadlines, and parsed dataset references/URLs.

---

## 📁 Download Dataset Files

| Format | File Link | Description | Size |
|---|---|---|---|
| **JSON** | [sih_problem_statements.json](./sih_problem_statements.json) | Full structured JSON database with clean nested attributes | ~700 KB |
| **CSV** | [sih_problem_statements.csv](./sih_problem_statements.csv) | Tabular CSV format for data science pipelines & analysis | ~635 KB |
| **Excel** | [sih_problem_statements.xlsx](./sih_problem_statements.xlsx) | Spreadsheet format for filtering, sorting, and reporting | ~222 KB |
| **Source HTML** | [website.html](./website.html) | Raw source snapshot from the SIH portal | ~2.5 MB |
| **Parser Script** | [export_data.py](./export_data.py) | Python extraction script to regenerate datasets | ~5 KB |

---

## 📊 Dataset Overview & Statistics

- **Total Problem Statements**: `226`
- **Category Breakdown**:
  - **Software**: `172`
  - **Hardware**: `54`

### Theme Distribution

| Theme | Count |
|---|---|
| Miscellaneous | 38 |
| Smart Automation | 31 |
| Disaster Management | 29 |
| Blockchain & Cybersecurity | 22 |
| MedTech / BioTech / HealthTech | 14 |
| Smart Education | 13 |
| Agriculture, FoodTech & Rural Development | 12 |
| Space Technology | 11 |
| Robotics and Drones | 10 |
| Transportation & Logistics | 8 |
| Fitness & Sports | 8 |
| Heritage & Culture | 7 |
| Travel & Tourism | 6 |
| Smart Resource Conservation | 5 |
| Smart Vehicles | 4 |
| Renewable / Sustainable Energy | 4 |
| Clean & Green Technology | 2 |
| Toys & Games | 2 |

---

## 📋 Schema & Field Definitions

Each record in the dataset contains the following attributes:

| Field | Type | Description |
|---|---|---|
| `s_no` | Integer | Serial Number (1 to 226) |
| `ps_number` | String | Official Problem Statement Code (e.g. `SIH26001`) |
| `ps_id` | String | Numeric Problem Identifier (e.g. `26001`) |
| `title` | String | Full title of the problem statement |
| `organization` | String | Ministry / Organization / Department |
| `department` | String | Sub-department or collaborating agency |
| `category` | String | `Software` or `Hardware` |
| `theme` | String | Assigned Hackathon Theme |
| `submitted_ideas_count` | String | Current submission status / quota (e.g. `0/500`) |
| `deadline` | String | Idea submission deadline date |
| `description` | String | Detailed background, objectives, and expected solutions |
| `dataset_details` | String | Specific dataset descriptions, benchmark instructions, or notes |
| `dataset_urls` | Array / String | Extracted external reference URLs (Kaggle, GitHub, API endpoints, etc.) |
| `youtube_link` | String | Video link (if provided) |
| `contact_info` | String | Nodal contact information (if provided) |

---

## 🛠️ Usage & Setup

### Prerequisites
Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

*(Or via Poetry)*:
```bash
poetry add beautifulsoup4 pandas openpyxl
```

### Re-running the Parser
To re-extract and regenerate the JSON, CSV, and Excel datasets from `website.html`:

```bash
python export_data.py
```

### Quick Analysis with Python & Pandas

```python
import pandas as pd
import json

# Load CSV
df = pd.read_csv('sih_problem_statements.csv')
print(f"Total Problem Statements: {len(df)}")
print(df['category'].value_counts())

# Filter for software problems with datasets
software_with_data = df[(df['category'] == 'Software') & (df['dataset_details'].notna())]
print(f"Software problems with dataset info: {len(software_with_data)}")
```

---

## 📄 License
Data extracted from the public portal of [Smart India Hackathon](https://sih.gov.in/).

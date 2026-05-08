# CityPulse AI — Data, Equity Scoring & Dashboard

**CET4973 — Intro to Artificial Intelligence | Spring 2026**  
**New York City College of Technology, CUNY**  
**Team:** Mohammed Imad, Ronny Yeap  
**Mentor:** Prof. Benito Mendoza-Garcia

---

## Overview

New York City prioritizes road and sidewalk repairs largely based on 311 complaint volume. This approach systematically under-serves neighborhoods where residents report issues less frequently due to language barriers, limited internet access, or lower civic engagement — not because their roads are in better condition.

CityPulse AI replaces complaint-driven prioritization with an equity-aware machine learning pipeline. It combines AI-detected road damage severity, real-time weather risk, facility proximity, 311 complaint history (normalized for neighborhood reporting rate), and accessibility data into a single priority score. A Random Forest classifier and Logistic Regression baseline are trained to predict one of four repair priority tiers: **Critical**, **High**, **Medium**, or **Low**.

---

## Repository Structure

```
citypulse-ai-dashboard/
├── notebooks/
│   └── CityPulse_AI_Model.ipynb      # Full training pipeline — open in Colab
├── src/
│   └── scoring_formula.py            # Priority scoring formula (standalone module)
├── samples/
│   └── citypulse_test_predictions.csv  # Sample model output (400 test records)
├── .gitignore
└── README.md
```

> **Note:** The full NYC 311 dataset is not included. See the Data Sources section below for access instructions.

---

## How to Run

### Option 1 — Google Colab (recommended)
1. Open [notebooks/CityPulse_AI_Model.ipynb](notebooks/CityPulse_AI_Model.ipynb) in GitHub
2. Click **Open in Colab** at the top of the notebook
3. Runtime → **Run all** (`Ctrl+F9`)
4. All figures and tables save to `/content/` — download from the Files panel

No installation required. All dependencies are pre-installed in Colab.

### Option 2 — Local
```bash
git clone https://github.com/monkeycruch/CityPulseAI-CityTech-.git
cd citypulse-ai-dashboard
pip install -r requirements.txt
jupyter notebook notebooks/CityPulse_AI_Model.ipynb
```

---

## Priority Scoring Formula

Each road incident is assigned a numerical score before classification:

```
Priority Score = (Severity × Weather) + Impact + Complaints + Accessibility
```

| Feature | Range | Source |
|---|---|---|
| Severity | 1–5 | Computer vision team (Team 1) damage detection |
| Weather | 1.0–1.5× | OpenWeatherMap One Call API 3.0 |
| Impact | 0–3 | NYC facility proximity (schools, hospitals) |
| Complaints | 0–2 | NYC 311 Open Data, normalized for reporting rate |
| Accessibility | 0–2 | ACS 2022 borough-level vulnerability estimates |

**Priority Tiers:**

| Tier | Score Range | Response Time |
|---|---|---|
| Critical | ≥ 11 | Within 24 hours |
| High | 7–10.99 | Within 48 hours |
| Medium | 4–6.99 | 1–2 weeks |
| Low | < 4 | Routine queue |

---

## Model Results (Test Set, n=400)

| Model | Test Accuracy | Test Macro F1 |
|---|---|---|
| Logistic Regression (baseline) | 0.950 | 0.797 |
| Random Forest | 0.920 | 0.648 |

Logistic Regression outperformed Random Forest on all metrics. The RF showed significant overfitting (train F1 = 1.000, test F1 = 0.648) due to the deterministic nature of formula-derived labels.

**Fairness (Disparate Impact Ratio, reference = Manhattan):**

| Borough | DIR | Result |
|---|---|---|
| Brooklyn | 0.97 | ✅ PASS |
| Queens | 0.72 | ❌ FAIL |
| Manhattan | 1.00 | ✅ PASS |
| Bronx | 1.00 | ✅ PASS |
| Staten Island | 0.67 | ❌ FAIL |

---

## Data Sources

| Source | Access |
|---|---|
| NYC 311 Open Data | [data.cityofnewyork.us](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9) |
| OpenWeatherMap API | [openweathermap.org/api](https://openweathermap.org/api/one-call-3) |
| NYC Facility Data | [data.cityofnewyork.us](https://data.cityofnewyork.us/) |
| ACS 2022 Demographics | [census.gov](https://www.census.gov/programs-surveys/acs) |

---

## Dependencies

```
scikit-learn
pandas
numpy
matplotlib
seaborn
sodapy          # NYC 311 Socrata API client
psycopg2        # PostgreSQL connection
fastapi         # Backend API
```

---

## Key References

- Kontokosta, C. E., & Hong, B. (2021). Bias in smart city governance. *Sustainable Cities and Society, 64*, 102503.
- Dolata, M., Feuerriegel, S., & Schwabe, G. (2022). A sociotechnical view of algorithmic fairness. *Information Systems Journal, 32*(4), 754–818.
- Pedregosa et al. (2011). Scikit-learn: Machine learning in Python. *JMLR, 12*, 2825–2830.

---

## License

For academic use only — CET4973 Spring 2026, New York City College of Technology.

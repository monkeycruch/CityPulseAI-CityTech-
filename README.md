# CityPulse AI — Data, Equity Scoring & Dashboard

**CET4973 — Intro to Artificial Intelligence | Spring 2026**  
**New York City College of Technology, CUNY**  
**Team:** Mohammed Imad, Ronny Yeap  
**Mentor:** Prof. Benito Mendoza-Garcia  
**Repository:** https://github.com/monkeycruch/CityPulseAI-CityTech-

---

## Overview

New York City prioritizes road and sidewalk repairs largely based on 311 complaint volume. This approach systematically under-serves neighborhoods where residents report issues less frequently due to language barriers, limited internet access, or lower civic engagement — not because their roads are in better condition.

CityPulse AI replaces complaint-driven prioritization with an **equity-aware machine learning pipeline**. It pulls real NYC 311 complaint data, applies a custom priority scoring formula adjusted for neighborhood underreporting, trains three ML classifiers, and serves results through a live FastAPI backend connected to an interactive Leaflet.js dashboard.

---

## What's Been Built

| Component | Status | Description |
|---|---|---|
| Real 311 data ingestion | ✅ Done | 10,000 real NYC 311 records via Socrata API |
| Priority scoring formula | ✅ Done | 5-feature equity-adjusted formula |
| ML models (LR, RF, XGBoost) | ✅ Done | Trained and evaluated on real data |
| Fairness analysis (DIR) | ✅ Done | All 5 boroughs pass the 0.80 threshold |
| FastAPI backend | ✅ Done | REST API serving live scored incidents |
| Leaflet.js dashboard | ✅ Done | Interactive map with filters and priority queue |

---

## Repository Structure

```
CityPulseAI-CityTech-/
├── README.md
├── notebooks/
│   ├── CityPulse_Real_311_Pipeline.ipynb   # Data ingestion + model training
│   └── CityPulse_Backend.ipynb             # FastAPI backend server
├── src/
│   └── scoring_formula.py                  # Standalone scoring formula module
├── dashboard/
│   └── citypulse_dashboard_api.html        # Interactive Leaflet.js dashboard
└── samples/
    └── citypulse_real_311_scored.csv       # 10,000 real scored incidents
```

---

## How to Run

### 1 — Model Training Pipeline
1. Open `notebooks/CityPulse_Real_311_Pipeline.ipynb` in Google Colab
2. Add your Socrata API token to Colab Secrets as `SOCRATA_TOKEN`
3. Runtime → **Run all** (`Ctrl+F9`)
4. Downloads figures and CSV to `/content/`

### 2 — FastAPI Backend
1. Open `notebooks/CityPulse_Backend.ipynb` in Google Colab
2. Run all 5 cells in order
3. Cell 5 outputs a public ngrok URL — keep this cell running
4. Copy the URL into the dashboard HTML

### 3 — Dashboard
1. Open `dashboard/citypulse_dashboard_api.html` in a text editor
2. Replace `YOUR_NGROK_URL_HERE` with your ngrok URL from Step 2
3. Open the file in your browser

### 4 — Scoring Formula (standalone)
```bash
python src/scoring_formula.py
```
Prints a working demo with 3 example incidents scored and explained.

---

## Priority Scoring Formula

```
Priority Score = (Severity × Weather) + Impact + Complaints + Accessibility
```

| Feature | Range | Source |
|---|---|---|
| Severity | 1.0–5.0 | CV model output (Team 1) — complaint-type proxy used currently |
| Weather | 1.0–1.5× | OpenWeatherMap One Call API 3.0 |
| Impact | 0.0–3.0 | NYC facility proximity (schools, hospitals) |
| Complaints | 0.0–2.0 | NYC 311 Open Data, normalized for underreporting rate |
| Accessibility | 0.0–2.0 | ACS 2022 borough-level vulnerability estimates |

**Priority Tiers (calibrated to real data distribution):**

| Tier | Score | Response Time | Count in dataset |
|---|---|---|---|
| Critical | ≥ 9.0 | Within 24 hours | 22 (0.2%) |
| High | 6.5–8.99 | Within 48 hours | 4,302 (43.0%) |
| Medium | 4.0–6.49 | 1–2 weeks | 5,293 (52.9%) |
| Low | < 4.0 | Routine queue | 383 (3.8%) |

> Thresholds were calibrated against the real data distribution. The original proposal used ≥11 for Critical based on a theoretical maximum of 14.5. Analysis of 10,000 real NYC 311 records revealed a practical score maximum of 9.81 due to seasonal weather constraints, so thresholds were adjusted accordingly.

---

## Model Results (Real 311 Data, n=10,000)

| Model | Test Accuracy | Test Macro F1 | Notes |
|---|---|---|---|
| Logistic Regression (baseline) | 0.971 | 0.942 | Best generalization |
| Random Forest | 0.950 | 0.922 | Slight overfitting |
| XGBoost (final model) | ~0.950 | ~0.940 | Best Critical class recall |

**XGBoost was selected as the final deployed model** because it correctly identifies Critical incidents with the best recall among all three models.

**Feature importance (XGBoost):**

| Feature | Importance |
|---|---|
| Severity | 0.376 |
| Complaints | 0.265 |
| Impact | 0.180 |
| Accessibility | 0.124 |
| Weather | 0.055 |

---

## Fairness Results (Disparate Impact Ratio)

All 5 NYC boroughs pass the 0.80 four-fifths rule threshold on real data:

| Borough | DIR | Result |
|---|---|---|
| Brooklyn | 1.35 | ✅ PASS |
| Staten Island | 1.33 | ✅ PASS |
| Queens | 1.28 | ✅ PASS |
| Bronx | 1.23 | ✅ PASS |
| Manhattan | 1.00 | ✅ PASS (reference) |

Outer boroughs score above 1.00, meaning they receive proportionally more high-priority attention than Manhattan — directly addressing the historical underreporting bias.

---

## API Endpoints

| Endpoint | Description | Example |
|---|---|---|
| `GET /api/health` | Health check | `/api/health` |
| `GET /api/stats` | Tier counts by borough | `/api/stats?borough=Bronx` |
| `GET /api/incidents` | All incidents (filterable) | `/api/incidents?tier=Critical&limit=50` |
| `GET /api/top` | Top N by priority score | `/api/top?n=20&borough=Brooklyn` |

Interactive API docs available at `/docs` when the backend is running.

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
xgboost
pandas
numpy
matplotlib
seaborn
sodapy
fastapi
uvicorn
pyngrok
```

---

## Roadmap

- [ ] Connect Team 1 CV model output for real severity scores
- [ ] Replace borough-level impact proxy with PostGIS spatial join
- [ ] Add live OpenWeatherMap API calls
- [ ] Deploy backend to self-hosted server (Docker + Portainer)
- [ ] Add choropleth equity map by neighborhood
- [ ] Add plain-English explanation per incident

---

## Key References

- Kontokosta, C. E., & Hong, B. (2021). Bias in smart city governance. *Sustainable Cities and Society, 64*, 102503.
- Dolata, M., Feuerriegel, S., & Schwabe, G. (2022). A sociotechnical view of algorithmic fairness. *Information Systems Journal, 32*(4), 754–818.
- Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *JMLR, 12*, 2825–2830.
- Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *KDD 2016*, 785–794.
- NYC Open Data. (2024). 311 Service Requests from 2010 to Present. NYC OpenData.

---

## License

For academic use only — CET4973 Spring 2026, New York City College of Technology, CUNY.

# Churn Prediction API

![CI](https://github.com/Ikram-Saidane/churn-prediction-api/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> API REST de prédiction de churn client télécom, construite avec FastAPI,
> containerisée avec Docker et déployée automatiquement via CI/CD GitHub Actions.

##  Liens

| | URL |
|---|---|
| **Interface Streamlit** | https://churn-prediction-api-n33ldashwkeaxnmtaayddw.streamlit.app |
| **API Swagger** | https://churn-prediction-api-production-db1d.up.railway.app/docs |
| **GitHub** | https://github.com/Ikram-Saidane/churn-prediction-api |

---

## Contexte métier

Le churn (résiliation) est un enjeu majeur pour les opérateurs télécom —
acquérir un nouveau client coûte 5x plus cher que d'en fidéliser un existant.

Ce projet prédit la probabilité qu'un client résilie son abonnement à partir
de ses caractéristiques (ancienneté, services souscrits, montant des factures...),
permettant aux équipes marketing de cibler les clients à risque avant qu'ils partent.

**Dataset :** IBM Telco Customer Churn — 7 043 clients, 20 features  
**Modèle :** Logistic Regression avec class_weight + seuil optimisé (0.596)  
**AUC : 0.840 | F1 : 0.636 | Accuracy : 0.777**

---

## 🏗️ Architecture
IBM Telco Dataset (7043 lignes)

│

▼

Feature Engineering

(5 nouvelles variables métier)

│

▼

Entraînement + MLflow Tracking

(LogReg · RandomForest · XGBoost · GradientBoosting)

│

▼

Modèle sérialisé (.pkl)

│

▼

API REST FastAPI ──────────────────┐

(validation Pydantic)              │
│                          ▼

▼                  Interface Streamlit

Image Docker               (churn-prediction-api

(multi-stage)          -n33ldashwkeaxnmtaayddw

│               .streamlit.app)

▼

CI/CD GitHub Actions

(test → build → deploy)

│

▼

Railway Cloud

(API publique)
---

##  Résultats des modèles

| Modèle | AUC | F1 | Accuracy | Seuil |
|--------|-----|----|----------|-------|
| **Logistic Regression** | **0.840** | **0.636** | **0.777** | **0.596** |
| Random Forest | 0.838 | 0.636 | 0.756 | 0.512 |
| Gradient Boosting | 0.836 | 0.629 | 0.765 | 0.311 |
| XGBoost | 0.828 | 0.623 | 0.769 | 0.562 |

**Techniques appliquées :**
- Feature engineering métier (5 nouvelles variables : `is_new_client`, `is_loyal_client`, `high_spender`, `charges_per_month_tenure`, `total_charges_ratio`)
- GridSearchCV avec StratifiedKFold (5 folds) sur 4 modèles
- Optimisation du seuil de décision via courbe Precision-Recall
- `class_weight='balanced'` pour gérer le déséquilibre des classes (74% / 26%)
- Tracking complet des expériences avec MLflow

---

##  Lancer en local

### Avec Docker (recommandé)
```bash
git clone https://github.com/Ikram-Saidane/churn-prediction-api.git
cd churn-prediction-api
docker build -t churn-api .
docker run -p 8000:8000 churn-api
# → API disponible sur http://localhost:8000/docs
```

### Sans Docker
```bash
git clone https://github.com/Ikram-Saidane/churn-prediction-api.git
cd churn-prediction-api
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
uvicorn app.main:app --reload
# → API disponible sur http://localhost:8000/docs
```

### Interface Streamlit en local
```bash
streamlit run streamlit_app.py
# → Interface disponible sur http://localhost:8501
```

---

##  Utilisation de l'API

### Vérifier que l'API est vivante
```bash
curl https://churn-prediction-api-production-db1d.up.railway.app/health
# → {"status":"ok","model_loaded":true}
```

### Prédire le churn d'un client
```bash
curl -X POST https://churn-prediction-api-production-db1d.up.railway.app/predict \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Female",
    "SeniorCitizen": 1,
    "Partner": "No",
    "Dependents": "No",
    "tenure": 2,
    "PhoneService": "Yes",
    "MultipleLines": "Yes",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 95.0,
    "TotalCharges": 190.0
  }'
```

### Réponse
```json
{
  "prediction": 0,
  "probability": 0.461,
  "threshold": 0.596,
  "label": "Client fidèle",
  "risk_level": "Faible"
}
```

---

##  Stack technique

| Couche | Technologies |
|--------|-------------|
| **Machine Learning** | scikit-learn, XGBoost, MLflow |
| **API** | FastAPI, Pydantic, Uvicorn |
| **Interface** | Streamlit |
| **Containerisation** | Docker multi-stage, docker-compose |
| **CI/CD** | GitHub Actions |
| **Déploiement API** | Railway |
| **Déploiement Interface** | Streamlit Cloud |

---

##  Structure du projet
churn-prediction-api/

├── app/

│   ├── init.py

│   ├── main.py           # Routes FastAPI

│   ├── model.py          # Chargement + inférence + preprocessing

│   └── schemas.py        # Validation Pydantic (input/output)

├── model/

│   ├── model.pkl         # Modèle entraîné (Logistic Regression)

│   ├── scaler.pkl        # StandardScaler fitted

│   ├── threshold.pkl     # Seuil optimisé (0.596)

│   └── feature_names.pkl # Ordre exact des features

├── notebooks/

│   └── 03_churn_training.ipynb  # EDA + entraînement + tuning

├── .github/

│   └── workflows/

│       └── ci.yml        # Pipeline CI/CD

├── streamlit_app.py      # Interface utilisateur

├── Dockerfile            # Multi-stage build

├── docker-compose.yml

├── requirements.txt

└── README.md
---

##  Pipeline CI/CD

À chaque `git push` sur `main`, GitHub Actions :

1. **Test** — installe les dépendances et vérifie les imports
2. **Build** — construit l'image Docker et teste `/health`
3. **Deploy** — Railway redéploie automatiquement depuis Docker Hub

---

##  Auteure

**Ikram Saidane** — M1 IASD, Université Tunis Dauphine (2025–2026)  
Spécialisation : Machine Learning · MLOps · Data Science

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ikram_Saidane-blue)](https://linkedin.com/in/ikram-saidane)
[![GitHub](https://img.shields.io/badge/GitHub-Ikram--Saidane-black)](https://github.com/Ikram-Saidane)

---

##  Licence

MIT License — libre d'utilisation et de modification.
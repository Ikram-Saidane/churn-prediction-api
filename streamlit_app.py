import streamlit as st
import requests

API_URL = "https://churn-prediction-api-production-db1d.up.railway.app"

st.set_page_config(
    page_title="Churn Prediction",
    page_icon="📡",
    layout="centered"
)

st.title("📡 Churn Prediction — Télécom")
st.markdown("Prédit si un client va résilier son abonnement.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Profil client")
    gender = st.selectbox("Genre", ["Male", "Female"])
    senior = st.selectbox("Senior Citizen", [0, 1])
    partner = st.selectbox("Partenaire", ["Yes", "No"])
    dependents = st.selectbox("Personnes à charge", ["Yes", "No"])
    tenure = st.slider("Ancienneté (mois)", 0, 72, 12)
    contract = st.selectbox("Type de contrat", [
        "Month-to-month", "One year", "Two year"
    ])
    payment = st.selectbox("Méthode de paiement", [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ])
    paperless = st.selectbox("Facturation dématérialisée", ["Yes", "No"])

with col2:
    st.subheader("Services souscrits")
    phone = st.selectbox("Service téléphonique", ["Yes", "No"])
    multiple = st.selectbox("Lignes multiples", [
        "Yes", "No", "No phone service"
    ])
    internet = st.selectbox("Service internet", [
        "DSL", "Fiber optic", "No"
    ])
    security = st.selectbox("Sécurité en ligne", [
        "Yes", "No", "No internet service"
    ])
    backup = st.selectbox("Sauvegarde en ligne", [
        "Yes", "No", "No internet service"
    ])
    protection = st.selectbox("Protection appareil", [
        "Yes", "No", "No internet service"
    ])
    support = st.selectbox("Support technique", [
        "Yes", "No", "No internet service"
    ])
    tv = st.selectbox("Streaming TV", [
        "Yes", "No", "No internet service"
    ])
    movies = st.selectbox("Streaming Films", [
        "Yes", "No", "No internet service"
    ])

st.divider()
st.subheader("Facturation")
col3, col4 = st.columns(2)
with col3:
    monthly = st.number_input("Charges mensuelles ($)", 0.0, 200.0, 65.0)
with col4:
    total = st.number_input("Charges totales ($)", 0.0, 10000.0, 780.0)

st.divider()

if st.button(" Prédire le churn", type="primary", use_container_width=True):
    payload = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple,
        "InternetService": internet,
        "OnlineSecurity": security,
        "OnlineBackup": backup,
        "DeviceProtection": protection,
        "TechSupport": support,
        "StreamingTV": tv,
        "StreamingMovies": movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly,
        "TotalCharges": total
    }

    with st.spinner("Analyse en cours..."):
        try:
            response = requests.post(f"{API_URL}/predict", json=payload)
            result = response.json()

            st.divider()

            if result["prediction"] == 1:
                st.error(f" **{result['label']}**")
            else:
                st.success(f" **{result['label']}**")

            col5, col6, col7 = st.columns(3)
            with col5:
                st.metric("Probabilité de churn", f"{result['probability']*100:.1f}%")
            with col6:
                st.metric("Niveau de risque", result["risk_level"])
            with col7:
                st.metric("Seuil de décision", f"{result['threshold']*100:.1f}%")

            st.divider()
            if result["prediction"] == 1:
                st.warning("""
                **Actions recommandées :**
                - Contacter le client de façon proactive
                - Proposer une offre de fidélisation
                - Envisager un upgrade de contrat
                """)

        except Exception as e:
            st.error(f"Erreur API : {e}")

st.divider()
st.caption("M1 IASD — Ikram Saidane · API : FastAPI + Docker + Railway")
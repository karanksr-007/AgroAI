import streamlit as st
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import io

model = joblib.load("model.pkl")

def dashboard():

    # ---------------- PREMIUM CSS ----------------
    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #0a0f1c, #020617);
        color: white;
        font-family: 'Segoe UI';
    }

    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #00f5c4;
        text-align: center;
    }

    .card {
        background: rgba(255,255,255,0.05);
        border-radius: 18px;
        padding: 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 0 25px rgba(0,255,200,0.15);
        transition: 0.3s;
    }

    .card:hover {
        transform: scale(1.03);
        box-shadow: 0 0 40px rgba(0,255,200,0.4);
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
        color: #00f5c4;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">🌱 AgroAI Intelligent Farming Platform</div>', unsafe_allow_html=True)

    # -------- NAV --------
    menu = ["📊 Dashboard", "📈 Analysis", "🗺 Map", "🌱 Soil", "📄 Report"]
    choice = st.sidebar.radio("Navigation", menu)

    # -------- INPUTS --------
    st.sidebar.header("🌾 Input Parameters")

    temp = st.sidebar.slider("Temperature", 10, 40, 25)
    hum = st.sidebar.slider("Humidity", 20, 100, 60)
    rain = st.sidebar.slider("Rainfall", 50, 300, 150)
    soil = st.sidebar.slider("Soil Quality", 1, 10, 5)
    fert = st.sidebar.slider("Fertilizer", 10, 100, 50)

    data = np.array([[temp, hum, rain, soil, fert]])
    pred = model.predict(data)[0]

    labels = ["Temperature", "Humidity", "Rainfall", "Soil", "Fertilizer"]
    values = [temp, hum, rain, soil, fert]

    # ================= DASHBOARD =================
    if choice == "📊 Dashboard":

        st.markdown('<div class="section-title">📊 Overview</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        col1.markdown(f'<div class="card">🌡 Temp<br><h2>{temp}°C</h2></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="card">💧 Humidity<br><h2>{hum}%</h2></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="card">🌾 Yield<br><h2>{pred:.2f}</h2></div>', unsafe_allow_html=True)

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pred,
            title={'text': "Yield Score"},
            gauge={'axis': {'range': [0, 100]}}
        ))
        st.plotly_chart(fig, use_container_width=True)

    # ================= ANALYSIS =================
    elif choice == "📈 Analysis":

        st.markdown('<div class="section-title">📊 Graph Analysis</div>', unsafe_allow_html=True)

        fig1 = px.pie(names=labels, values=values)
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.bar(x=labels, y=values, color=values)
        st.plotly_chart(fig2, use_container_width=True)

        future = [pred + i*2 for i in range(5)]
        fig3 = px.line(y=future, markers=True)
        st.plotly_chart(fig3, use_container_width=True)

        # DOWNLOAD GRAPH
        img_bytes = io.BytesIO()
        fig2.write_image(img_bytes, format='png')
        st.download_button("📥 Download Graph", img_bytes, "graph.png")

    # ================= MAP =================
    elif choice == "🗺 Map":

        st.markdown('<div class="section-title">🗺 Farm Location</div>', unsafe_allow_html=True)

        map_data = pd.DataFrame({
            "lat": [21.1702],
            "lon": [72.8311]
        })
        st.map(map_data)

    # ================= SOIL =================
    elif choice == "🌱 Soil":

        st.markdown('<div class="section-title">🌱 Soil Intelligence</div>', unsafe_allow_html=True)

        if soil < 4:
            st.error("🚨 Poor Soil Quality")
            st.write("Add compost, improve nutrients")
        elif soil < 7:
            st.warning("⚠️ Moderate Soil")
            st.write("Optimize fertilizer usage")
        else:
            st.success("✅ Healthy Soil")

    # ================= REPORT =================
    elif choice == "📄 Report":

        st.markdown('<div class="section-title">📄 AI Advisory Report</div>', unsafe_allow_html=True)

        if pred < 40:
            conclusion = "Low Yield → Improve irrigation & soil"
        elif pred < 70:
            conclusion = "Moderate Yield → Optimize resources"
        else:
            conclusion = "High Yield → Maintain conditions"

        report = f"""
AgroAI Smart Report

Temperature: {temp}
Humidity: {hum}
Rainfall: {rain}
Soil Quality: {soil}
Fertilizer: {fert}

Predicted Yield: {pred:.2f}

Conclusion:
{conclusion}
"""

        st.code(report)

        st.download_button("📥 Download Full Report", report, "AgroAI_Report.txt")

    # LOGOUT
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
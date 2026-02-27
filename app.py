import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AirOps AI ✈️",
    page_icon="✈️",
    layout="wide"
)

# ---------------- DYNAMIC UI STYLING ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Force headers to be visible in both themes */
    h1, h2, h3 {
        color: inherit !important;
    }

    /* BRANDING HEADER CARD */
    .brand-card {
        background: linear-gradient(90deg, #2563EB 0%, #06B6D4 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .brand-card h1, .brand-card p {
        color: white !important;
        margin: 0 !important;
    }

    /* METRIC CARDS */
    [data-testid="metric-container"] {
        background: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.1);
        border-radius: 12px;
        padding: 15px;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## ⚙️ Control Panel")
distance = st.sidebar.slider("🌍 Flight Distance (miles)", 100, 3000, 1200)
departure_delay = st.sidebar.slider("⏰ Departure Delay (min)", 0, 300, 35)

# UPDATED: Min 1, Max 10,00,000 (10 Lakhs)
cost_per_minute = st.sidebar.number_input(
    "💸 Cost per Minute (₹)", 
    min_value=1, 
    max_value=1000000, 
    value=8000 
)

# ---------------- LOGIC ----------------
arrival_delay = (departure_delay * 0.9) + (distance * 0.002)
financial_loss = arrival_delay * cost_per_minute

# ---------------- HEADER ----------------
st.markdown("""
    <div class="brand-card">
        <h1>✈️ AirOps AI</h1>
        <p>Smart Aviation Delay Intelligence Platform</p>
    </div>
""", unsafe_allow_html=True)

# ---------------- KPI SECTION ----------------
k1, k2, k3 = st.columns(3)
k1.metric("Arrival Delay", f"{arrival_delay:.1f} min")
k2.metric("Estimated Loss", f"₹{financial_loss:,.0f}")
k3.metric("Distance", f"{distance} miles")

st.write("---")

# ---------------- CHARTS ----------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Delay Contribution")
    
    cause_df = pd.DataFrame({
        "Factor": ["Departure Delay", "Distance Impact"],
        "Minutes": [departure_delay * 0.9, distance * 0.002]
    })
    
    fig1 = px.bar(
        cause_df, x="Factor", y="Minutes", 
        color="Factor",
        color_discrete_sequence=["#2563EB", "#06B6D4"]
    )
    fig1.update_layout(
        showlegend=False, 
        margin=dict(t=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### 🚦 Severity Gauge")
    
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=arrival_delay,
        gauge={
            'axis': {'range': [0, 300]},
            'bar': {'color': "#2563EB"},
            'steps': [
                {'range': [0, 30], 'color': "#16A34A"},
                {'range': [30, 100], 'color': "#F59E0B"},
                {'range': [100, 300], 'color': "#DC2626"}
            ]
        }
    ))
    fig_gauge.update_layout(
        margin=dict(t=50, b=0, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

# ---------------- FINANCIAL TREND ----------------
st.markdown("### 💸 Loss Projection")
delay_range = np.arange(0, 301, 10)
loss_df = pd.DataFrame({"Delay": delay_range, "Loss": delay_range * cost_per_minute})

fig2 = px.line(loss_df, x="Delay", y="Loss", markers=True)
fig2.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis_title="Loss (₹)"
)
# Force standard number format on Y-axis to handle large Lakhs/Crore values clearly
fig2.update_yaxes(tickformat=",.0f")

st.plotly_chart(fig2, use_container_width=True)
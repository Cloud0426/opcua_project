"""
AI+OPC Anomaly Detection Web Interface
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from datetime import datetime
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# ===== Page Config =====
st.set_page_config(
    page_title="AI+OPC Anomaly Detection",
    page_icon="🏭",
    layout="wide"
)

# ===== Title =====
st.title("🏭 AI+OPC Smart Equipment Anomaly Detection System")
st.markdown("OPC UA Data Collection + Isolation Forest Algorithm")

# ===== Sidebar =====
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 Load Latest Data"):
        st.session_state.loaded = True
        st.rerun()
    st.divider()
    st.caption("📌 Data Source: Prosys OPC UA Simulation Server")
    st.caption(f"⏱️ Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ===== Main Area =====
FEATURE_COLS = ["Counter", "Random", "Sawtooth", "Sinusoid", "Square", "Triangle"]

def load_latest_data():
    files = glob.glob("opcua_data_*.csv")
    if not files:
        return None
    latest = sorted(files)[-1]
    df = pd.read_csv(latest)
    return df

def run_anomaly_detection(df):
    X = df[FEATURE_COLS].copy()
    X = X.replace("ERROR", np.nan).dropna()
    if len(X) < 5:
        return df, None, None
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = IsolationForest(contamination=0.1, random_state=42)
    predictions = model.fit_predict(X_scaled)
    df_result = df.iloc[X.index].copy()
    df_result["Anomaly"] = predictions
    df_result["Status"] = df_result["Anomaly"].apply(lambda x: "⚠️ Anomaly" if x == -1 else "✅ Normal")
    return df_result, X_scaled, predictions

# ===== Load Data =====
df = load_latest_data()

if df is None:
    st.warning("⚠️ No data file found. Please run collect_data.py first.")
    st.stop()

df_result, X_scaled, predictions = run_anomaly_detection(df)

if df_result is None:
    st.warning("⚠️ Insufficient data. Please collect more samples.")
    st.stop()

# ===== Metrics =====
normal_count = (df_result["Status"] == "✅ Normal").sum()
anomaly_count = (df_result["Status"] == "⚠️ Anomaly").sum()
total = len(df_result)

col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Total Samples", f"{total}")
col2.metric("✅ Normal", f"{normal_count}", delta=f"{(normal_count/total*100):.1f}%")
col3.metric("⚠️ Anomaly", f"{anomaly_count}", delta=f"{(anomaly_count/total*100):.1f}%", delta_color="inverse")
col4.metric("📈 Anomaly Rate", f"{(anomaly_count/total*100):.1f}%")

st.divider()

# ===== Visualization =====
st.subheader("📊 Anomaly Detection Visualization")

if X_scaled is not None and predictions is not None:
    fig, axes = plt.subplots(2, 3, figsize=(12, 6))
    axes = axes.flatten()
    for i, col in enumerate(FEATURE_COLS):
        ax = axes[i]
        colors = ['red' if p == -1 else 'blue' for p in predictions]
        ax.scatter(range(len(X_scaled)), X_scaled[:, i], c=colors, alpha=0.7, s=30)
        ax.set_title(f"{col}", fontsize=10)
        ax.set_xlabel("Sample Index")
        ax.set_ylabel("Normalized Value")
        ax.grid(True, alpha=0.3)
    axes[5].axis('off')
    axes[5].scatter([], [], c='blue', label='Normal', s=50)
    axes[5].scatter([], [], c='red', label='Anomaly', s=50)
    axes[5].legend(loc='center', fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)

st.divider()

# ===== Data Table =====
st.subheader("📋 Detection Results")

display_cols = ["Timestamp"] + FEATURE_COLS + ["Status"]
st.dataframe(
    df_result[display_cols].style.map(
        lambda x: 'background-color: #ffcccc' if x == '⚠️ Anomaly' else '',
        subset=['Status']
    ),
    use_container_width=True,
    height=300
)

# ===== Footer =====
st.divider()
st.caption("🔧 Tech Stack: Python | OPC UA | Isolation Forest | Streamlit")
st.caption("📌 Anomalies marked in red")
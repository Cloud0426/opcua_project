"""
AI+OPC 异常检测 Web 界面
基于 Streamlit 构建，展示数据采集和 AI 检测结果
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import time
from datetime import datetime
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# ===== 解决 matplotlib 中文乱码 =====
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体为微软雅黑
plt.rcParams['axes.unicode_minus'] = False              # 解决负号 '-' 显示为方块的问题

# ===== 页面配置 =====
st.set_page_config(
    page_title="AI+OPC 设备异常检测系统",
    page_icon="🏭",
    layout="wide"
)

# ... 后面的代码保持不变 ...

# ===== 标题 =====
st.title("🏭 AI+OPC 智能设备异常检测系统")
st.markdown("基于 OPC UA 数据采集 + 孤立森林异常检测算法")

# ===== 侧边栏 =====
with st.sidebar:
    st.header("⚙️ 系统控制")
    
    # 读取数据按钮
    if st.button("🔄 加载最新数据"):
        st.session_state.loaded = True
        st.rerun()
    
    st.divider()
    st.caption("📌 数据来源: Prosys OPC UA Simulation Server")
    st.caption(f"⏱️ 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ===== 主区域 =====
# 定义特征列
FEATURE_COLS = ["Counter", "Random", "Sawtooth", "Sinusoid", "Square", "Triangle"]

# 读取最新的 CSV 文件
def load_latest_data():
    files = glob.glob("opcua_data_*.csv")
    if not files:
        return None
    latest = sorted(files)[-1]
    df = pd.read_csv(latest)
    return df

# 运行异常检测
def run_anomaly_detection(df):
    X = df[FEATURE_COLS].copy()
    X = X.replace("ERROR", np.nan).dropna()
    
    if len(X) < 5:
        return df, None, None
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = IsolationForest(contamination=0.1, random_state=42)
    predictions = model.fit_predict(X_scaled)
    
    # 标记结果
    df_result = df.iloc[X.index].copy()
    df_result["Anomaly"] = predictions
    df_result["状态"] = df_result["Anomaly"].apply(lambda x: "⚠️ 异常" if x == -1 else "✅ 正常")
    
    return df_result, X_scaled, predictions

# ===== 加载数据 =====
df = load_latest_data()

if df is None:
    st.warning("⚠️ 未找到数据文件，请先运行 collect_data.py 采集数据")
    st.stop()

# 运行检测
df_result, X_scaled, predictions = run_anomaly_detection(df)

if df_result is None:
    st.warning("⚠️ 数据量不足，请采集更多数据")
    st.stop()

# ===== 统计指标 =====
normal_count = (df_result["状态"] == "✅ 正常").sum()
anomaly_count = (df_result["状态"] == "⚠️ 异常").sum()
total = len(df_result)

col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 总数据量", f"{total} 条")
col2.metric("✅ 正常", f"{normal_count} 条", delta=f"{(normal_count/total*100):.1f}%")
col3.metric("⚠️ 异常", f"{anomaly_count} 条", delta=f"{(anomaly_count/total*100):.1f}%", delta_color="inverse")
col4.metric("📈 异常率", f"{(anomaly_count/total*100):.1f}%")

st.divider()

# ===== 可视化图表 =====
st.subheader("📊 异常检测可视化")

if X_scaled is not None and predictions is not None:
    fig, axes = plt.subplots(2, 3, figsize=(12, 6))
    axes = axes.flatten()
    
    for i, col in enumerate(FEATURE_COLS):
        ax = axes[i]
        colors = ['red' if p == -1 else 'blue' for p in predictions]
        ax.scatter(range(len(X_scaled)), X_scaled[:, i], c=colors, alpha=0.7, s=30)
        ax.set_title(f"{col}", fontsize=10)
        ax.set_xlabel("样本序号")
        ax.set_ylabel("标准化值")
        ax.grid(True, alpha=0.3)
    
    # 用最后一个子图显示图例
    axes[5].axis('off')
    axes[5].scatter([], [], c='blue', label='正常', s=50)
    axes[5].scatter([], [], c='red', label='异常', s=50)
    axes[5].legend(loc='center', fontsize=12)
    
    plt.tight_layout()
    st.pyplot(fig)

st.divider()

# ===== 数据表格 =====
st.subheader("📋 检测结果明细")

# 选择显示的列
display_cols = ["Timestamp"] + FEATURE_COLS + ["状态"]
st.dataframe(
    df_result[display_cols].style.applymap(
        lambda x: 'background-color: #ffcccc' if x == '⚠️ 异常' else '',
        subset=['状态']
    ),
    use_container_width=True,
    height=300
)

# ===== 底部 =====
st.divider()
st.caption("🔧 技术栈: Python | OPC UA | 孤立森林 | Streamlit")
st.caption("📌 异常点已标红，支持导出数据和图表")
"""
用孤立森林训练异常检测模型
数据来源：Prosys 模拟器采集的 CSV 文件
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import glob
import os

# 1. 读取最新的 CSV 数据文件
files = glob.glob("opcua_data_*.csv")
if not files:
    print("❌ 没有找到数据文件，请先运行 collect_data.py")
    exit()

latest_file = sorted(files)[-1]  # 取最新文件
print(f"📂 读取数据文件: {latest_file}")

df = pd.read_csv(latest_file)
print(f"📊 共 {len(df)} 条数据")

# 2. 选择用于训练的数值列
feature_cols = ["Counter", "Random", "Sawtooth", "Sinusoid", "Square", "Triangle"]
X = df[feature_cols].copy()

# 3. 处理可能的异常值（把 "ERROR" 字符串替换为 NaN 后删除）
X = X.replace("ERROR", np.nan)
X = X.dropna()

# 4. 标准化数据（让不同量纲的数据具有可比性）
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"✅ 预处理完成，使用 {len(X_scaled)} 条有效数据")

# 5. 训练孤立森林模型
model = IsolationForest(
    contamination=0.1,      # 假设异常数据占 10%
    random_state=42,
    n_estimators=100
)
model.fit(X_scaled)

# 6. 预测并标记异常
predictions = model.predict(X_scaled)
# 孤立森林返回：1 表示正常，-1 表示异常
df_result = df.iloc[X.index].copy()  # 使用删除 NaN 后的索引
df_result["Anomaly"] = predictions
df_result["Anomaly_Label"] = df_result["Anomaly"].apply(
    lambda x: "异常" if x == -1 else "正常"
)

# 7. 输出统计
normal_count = (predictions == 1).sum()
anomaly_count = (predictions == -1).sum()
print(f"\n📈 模型训练完成！")
print(f"   ✅ 正常样本: {normal_count} 条")
print(f"   ⚠️ 异常样本: {anomaly_count} 条")

# 8. 可视化
fig, axes = plt.subplots(2, 3, figsize=(12, 6))
axes = axes.flatten()

for i, col in enumerate(feature_cols):
    ax = axes[i]
    colors = ['red' if label == -1 else 'blue' for label in predictions]
    ax.scatter(range(len(X_scaled)), X_scaled[:, i], c=colors, alpha=0.6, s=20)
    ax.set_title(f"{col} (红=异常)")
    ax.set_xlabel("样本序号")
    ax.set_ylabel("标准化值")

# 第6个子图显示总览
axes[5].axis('off')
axes[5].text(0.1, 0.5, 
             f"异常检测结果\n正常: {normal_count}\n异常: {anomaly_count}",
             fontsize=14, verticalalignment='center')

plt.tight_layout()
plt.savefig("anomaly_detection_result.png", dpi=150)
print(f"📊 可视化图表已保存: anomaly_detection_result.png")

# 显示图表（如果支持）
try:
    plt.show()
except:
    print("💡 图表已保存为图片文件，请直接打开查看。")

# 9. 打印部分结果（便于查看）
print("\n📋 检测结果预览（前10条）:")
print(df_result[["Timestamp"] + feature_cols + ["Anomaly_Label"]].head(10).to_string(index=False))
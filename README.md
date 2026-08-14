# OPCGuard 智测卫士

**基于 OPC UA 与孤立森林的轻量化工业设备智能异常检测系统**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)

---

## 📖 项目简介

OPCGuard 是一套轻量级工业设备异常检测系统，通过 OPC UA 标准协议采集设备数据，利用孤立森林（Isolation Forest）无监督学习算法实现实时异常识别，并通过 Web 界面可视化展示检测结果。

**核心特点：**
- ✅ 基于 OPC UA 标准协议，兼容主流工业设备
- ✅ 孤立森林无监督学习，无需标注故障数据
- ✅ 轻量化部署，单台 PC 即可运行
- ✅ Web 可视化看板，异常自动标红
- ✅ 完全开源（MIT License），可自由审计和二次开发

---

## ✨ 功能特性

| 功能模块 | 说明 |
|----------|------|
| **节点探索** | 自动枚举 OPC UA 服务器所有可用节点 |
| **链路验证** | 测试 OPC UA 通信连接，验证数据读取 |
| **数据采集** | 异步并发读取多通道数据，持久化为 CSV |
| **异常检测** | 孤立森林模型自动识别异常样本 |
| **Web 看板** | 交互式界面展示指标、图表和明细表格 |

---

## 🏗️ 系统架构
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ 数据采集层 │ → │ AI分析层 │ → │ 展示层 │
│ OPC UA客户端 │ │ 孤立森林算法 │ │ Streamlit │
│ (asyncua) │ │ (scikit-learn) │ │ Web看板 │
└─────────────────┘ └─────────────────┘ └─────────────────┘

text

**工作流程：**

`OPC UA Server → 数据采集 → CSV存储 → 模型训练 → 异常检测 → Web展示`

---

## 🚀 快速开始

### 环境要求

- Python 3.12 或更高版本
- pip 包管理器

### 1. 克隆仓库

```bash
git clone https://github.com/Cloud0426/opcua_project.git
cd opcua_project
2. 安装依赖
bash
pip install -r requirements.txt
3. 启动 Prosys OPC UA 模拟器
下载并安装 Prosys OPC UA Simulation Server

启动软件，确保状态显示为 Running

记下连接地址（默认：opc.tcp://localhost:53530/OPCUA/SimulationServer）

4. 验证通信链路
bash
python test_opcua.py
预期输出：显示 Counter、Random 等变量的实时值

5. 采集数据
bash
python collect_data.py
采集 60 秒数据，自动生成 opcua_data_*.csv 文件

6. 训练模型并检测异常
bash
python train_model.py
输出检测结果统计，生成 anomaly_detection_result.png

7. 启动 Web 看板
bash
streamlit run app.py
浏览器自动打开 http://localhost:8501 查看结果

🛠️ 技术栈
类别	技术
工业通信	OPC UA (asyncua)
AI 算法	孤立森林 (scikit-learn)
数据处理	Pandas, NumPy
可视化	Matplotlib
Web 框架	Streamlit
部署	Streamlit Cloud
📁 目录结构
text
opcua_project/
├── test_opcua.py          # OPC UA 连接验证
├── explore.py             # 节点探索
├── collect_data.py        # 数据采集
├── train_model.py         # 模型训练
├── app.py                 # Web 看板
├── requirements.txt       # 依赖清单
└── README.md              # 项目说明
📊 测试结果
在 Prosys OPC UA Simulation Server 环境下：

指标	结果
采集数据量	30 条
正常样本	27 条
异常样本	3 条
异常率	10.0%
可视化结果：

https://github.com/Cloud0426/opcua_project/raw/master/anomaly_detection_result.png

📄 许可证
本项目采用 MIT License，可自由使用、修改、分发。

🤝 贡献
欢迎提交 Issue 和 Pull Request！

Fork 本仓库

创建你的特性分支 (git checkout -b feature/AmazingFeature)

提交你的改动 (git commit -m 'Add some AmazingFeature')

推送到分支 (git push origin feature/AmazingFeature)

打开一个 Pull Request

📧 联系方式
GitHub Issues：https://github.com/Cloud0426/opcua_project/issues

项目链接：https://github.com/Cloud0426/opcua_project

⭐ 如果这个项目对你有帮助，请给一个 Star！

"""
采集 OPC UA 数据并保存为 CSV 文件
用于训练 AI 模型
"""

import asyncio
from asyncua import Client
from asyncua.ua import NodeId, NodeIdType
import csv
import time
from datetime import datetime

SERVER_URL = "opc.tcp://localhost:53530/OPCUA/SimulationServer"

# 根据探索结果定义节点
NODE_DEFS = [
    ("Counter", NodeId(1001, 3, NodeIdType.FourByte)),
    ("Random", NodeId(1002, 3, NodeIdType.FourByte)),
    ("Sawtooth", NodeId(1003, 3, NodeIdType.FourByte)),
    ("Sinusoid", NodeId(1004, 3, NodeIdType.FourByte)),
    ("Square", NodeId(1005, 3, NodeIdType.FourByte)),
    ("Triangle", NodeId(1006, 3, NodeIdType.FourByte)),
]

# 采集设置
COLLECT_DURATION = 60  # 采集多少秒（建议60秒）
INTERVAL = 2           # 每2秒采集一次


async def collect_data():
    """采集数据并保存到 CSV"""
    
    client = Client(SERVER_URL)
    
    try:
        await client.connect()
        print("✅ 连接成功，开始采集数据...")
        
        # 获取所有节点对象
        nodes = []
        for name, node_id in NODE_DEFS:
            nodes.append((name, client.get_node(node_id)))
        
        # 准备 CSV 文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"opcua_data_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 写入表头：时间戳 + 所有变量名
            header = ["Timestamp"] + [name for name, _ in NODE_DEFS]
            writer.writerow(header)
            
            start_time = time.time()
            count = 0
            
            while time.time() - start_time < COLLECT_DURATION:
                # 读取所有变量的值
                row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                for _, node in nodes:
                    try:
                        value = await node.read_value()
                        row.append(value)
                    except Exception as e:
                        row.append("ERROR")
                
                writer.writerow(row)
                count += 1
                print(f"✅ 已采集 {count} 条数据")
                
                await asyncio.sleep(INTERVAL)
        
        print(f"\n🎉 采集完成！共采集 {count} 条数据")
        print(f"📁 保存到文件: {filename}")
        
    except Exception as e:
        print(f"❌ 出错: {e}")
        
    finally:
        await client.disconnect()
        print("\n🔌 已断开连接")


if __name__ == "__main__":
    asyncio.run(collect_data())
"""
直接用 Python 连接 Prosys OPC UA Simulation Server
功能：连接模拟器，读取并打印数据，验证通信链路
"""

import asyncio
from asyncua import Client
from asyncua.ua import NodeId, NodeIdType

# ===== 配置区 =====
SERVER_URL = "opc.tcp://localhost:53530/OPCUA/SimulationServer"

# 根据探索结果，使用 NodeId 对象来定义节点
# 格式：NodeId(Identifier, NamespaceIndex, NodeIdType)
NODE_DEFS = [
    ("Counter", NodeId(1001, 3, NodeIdType.FourByte)),
    ("Random", NodeId(1002, 3, NodeIdType.FourByte)),
    ("Sawtooth", NodeId(1003, 3, NodeIdType.FourByte)),
    ("Sinusoid", NodeId(1004, 3, NodeIdType.FourByte)),
    ("Square", NodeId(1005, 3, NodeIdType.FourByte)),
    ("Triangle", NodeId(1006, 3, NodeIdType.FourByte)),
]


async def main():
    client = Client(SERVER_URL)
    
    try:
        print(f"⏳ 正在连接 {SERVER_URL} ...")
        await client.connect()
        print("✅ 连接成功！\n")
        
        print("=" * 50)
        print(f"{'变量名':<15} {'当前值':<20}")
        print("=" * 50)
        
        for name, node_id in NODE_DEFS:
            try:
                # 根据 NodeId 获取节点
                node = client.get_node(node_id)
                # 读取节点值
                value = await node.read_value()
                print(f"{name:<15} {str(value):<20}")
            except Exception as e:
                print(f"❌ 读取 {name} 失败: {e}")
        
        print("=" * 50)
        print("\n✅ 数据读取完成！OPC UA 通信链路正常。")
        
        # 持续监测 Counter (NodeId: 1001, NamespaceIndex: 3)
        print("\n🔄 开始监测 Counter（每2秒更新），按 Ctrl+C 停止...")
        counter_node = client.get_node(NodeId(1001, 3, NodeIdType.FourByte))
        count = 0
        while True:
            try:
                value = await counter_node.read_value()
                print(f"[{count+1}] Counter = {value}")
                count += 1
                await asyncio.sleep(2)
            except KeyboardInterrupt:
                print("\n⏹️ 用户中断")
                break
            except Exception as e:
                print(f"⚠️ 读取异常: {e}")
                await asyncio.sleep(2)
                
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("\n💡 请检查：")
        print("   1. Prosys 模拟器是否已启动并处于 Running 状态")
        print("   2. 服务器地址是否正确")
        
    finally:
        await client.disconnect()
        print("\n🔌 已断开连接")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ 程序被用户终止")
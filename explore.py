"""
探索 Prosys 模拟器的所有可用节点
"""

import asyncio
from asyncua import Client

async def explore():
    client = Client("opc.tcp://localhost:53530/OPCUA/SimulationServer")
    
    try:
        await client.connect()
        print("✅ 连接成功！\n")
        
        # 获取根节点
        root = client.nodes.root
        
        # 获取 objects 节点（所有设备数据都在这里）
        objects = client.nodes.objects
        
        # 获取 objects 下的所有子节点
        children = await objects.get_children()
        
        print("=" * 60)
        print(f"{'变量名':<20} {'NodeId (字符串形式)':<35}")
        print("=" * 60)
        
        for child in children:
            try:
                # 直接用字符串表示 NodeId
                node_id_str = str(child.nodeid)
                # 读取显示名称（返回的是 LocalizedText 对象）
                name_obj = await child.read_display_name()
                # 提取文本内容
                name = str(name_obj)
                print(f"{name:<20} {node_id_str:<35}")
            except Exception as e:
                print(f"❌ 读取失败: {e}")
        
        print("=" * 60)
        
        # 特别查找 Simulation 文件夹下的子节点
        print("\n🔍 查找 'Simulation' 文件夹下的子节点...")
        for child in children:
            try:
                name_obj = await child.read_display_name()
                name = str(name_obj)
                if "Simulation" in name or "simulation" in name:
                    print(f"\n✅ 找到 Simulation 文件夹，NodeId: {str(child.nodeid)}")
                    sim_children = await child.get_children()
                    print(f"{'  ├── 变量名':<20} {'NodeId':<35}")
                    for sim_child in sim_children:
                        try:
                            sim_name = str(await sim_child.read_display_name())
                            print(f"  ├── {sim_name:<17} {str(sim_child.nodeid)}")
                        except:
                            pass
                    break
            except:
                pass
        
        print("\n✅ 探索完成！")
        
        # 额外：尝试直接获取一些常见节点
        print("\n🔍 尝试直接读取常见变量...")
        test_ids = [
            "ns=2;i=2",
            "ns=2;i=3", 
            "ns=2;i=4",
            "ns=2;i=5",
            "ns=2;i=6",
            "ns=2;i=2002",
            "ns=2;i=2003",
        ]
        for test_id in test_ids:
            try:
                node = await root.get_child([test_id])
                value = await node.read_value()
                name = str(await node.read_display_name())
                print(f"  ✅ {name}: {value} (NodeId: {test_id})")
            except:
                print(f"  ❌ 无法读取 {test_id}")
                    
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        
    finally:
        await client.disconnect()
        print("\n🔌 已断开连接")

if __name__ == "__main__":
    asyncio.run(explore())
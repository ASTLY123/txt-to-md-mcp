#!/usr/bin/env python3
"""
使用 FastMCP Client 测试 txt-to-md MCP 服务器
"""

import asyncio
from pathlib import Path
from fastmcp import Client

async def test_mcp_server():
    """使用 FastMCP Client 测试 MCP 服务器功能"""
    print("启动 FastMCP 客户端测试...")
    
    # 创建客户端，指向本地服务器脚本
    server_path = Path(__file__).parent / "server.py"
    
    # 使用 stdio 传输方式，传递存储路径参数
    client = Client(str(server_path))
    
    try:
        async with client:
            print("✅ 客户端连接成功！")
            
            # 测试服务器连通性
            await client.ping()
            print("✅ 服务器响应正常！")
            
            # 列出可用工具
            tools = await client.list_tools()
            print(f"✅ 可用工具数量: {len(tools)}")
            for tool in tools:
                print(f"   - {tool.name}: {tool.description}")
            
            # 测试 write_txt_to_markdown 工具
            print("\n📝 测试写入 Markdown 文件...")
            result = await client.call_tool("write_txt_to_markdown", {
                "content": "这是一个测试文档\n\n包含多行内容的 txt 文本。\n\n- 项目 1\n- 项目 2\n- 项目 3",
                "filename": "test_output",
                "title": "测试文档",
                "overwrite": True,
                "subfolder": "test"
            })
            
            print(f"写入结果: {result.data}")
            
            if result.data.get("success"):
                print("✅ 文件写入成功！")
                print(f"   文件路径: {result.data.get('file_path')}")
                print(f"   文件大小: {result.data.get('file_size')} 字节")
            else:
                print(f"❌ 文件写入失败: {result.data.get('message')}")
            
            # 测试 list_recent_md_files 工具
            print("\n📋 测试列出 Markdown 文件...")
            files_result = await client.call_tool("list_recent_md_files", {
                "limit": 5,
                "subfolder": ""
            })
            
            print(f"文件列表结果: {files_result.data}")
            
            if files_result.data.get("success"):
                files = files_result.data.get("files", [])
                print(f"✅ 找到 {len(files)} 个文件")
                for file in files[:3]:  # 只显示前3个
                    print(f"   - {file.get('name')} ({file.get('size')} 字节)")
            else:
                print(f"❌ 列出文件失败: {files_result.data.get('message')}")
                
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_server())

#!/usr/bin/env python3
"""
FastMCP 工具: 将 txt 内容写入到指定路径的 md 文档
支持通过 stdio 方式启动
"""

import os
import sys
from pathlib import Path
from typing import Any
import logging

from fastmcp import FastMCP

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取存储路径参数
if len(sys.argv) > 1:
    STORAGE_PATH = Path(sys.argv[1])
else:
    STORAGE_PATH = Path("d:/obsidian_storage/default")

# 确保存储目录存在
STORAGE_PATH.mkdir(parents=True, exist_ok=True)
logger.info(f"存储路径: {STORAGE_PATH}")

# 创建 FastMCP 实例
mcp = FastMCP("txt-to-md-converter")

@mcp.tool()
async def write_txt_to_markdown(
    content: str,
    filename: str,
    title: str = None,
    overwrite: bool = False,
    subfolder: str = ""
) -> dict:
    """
    将 txt 内容写入到指定文件名的 md 文档
    
    Args:
        content: txt 内容
        filename: 文件名（不含路径，自动添加.md扩展名）
        title: 可选的文档标题，最好以日期+主题的形式命名
        overwrite: 是否覆盖已存在的文件，除非说明否则绝不要覆盖
        subfolder: 可选的子文件夹（相对于基础路径）
        
    Returns:
        dict: 操作结果
    """
    try:
        # 处理子文件夹
        if subfolder:
            target_dir = STORAGE_PATH / subfolder
        else:
            target_dir = STORAGE_PATH
        
        # 处理文件名，确保有.md扩展名
        if not filename.endswith('.md'):
            filename = filename + '.md'
        
        file_path = target_dir / filename
        
        # 检查文件是否存在，如果不允许覆盖则返回错误
        if file_path.exists() and not overwrite:
            return {
                "success": False,
                "file_path": str(file_path),
                "message": f"文件已存在: {filename}。使用 overwrite=True 来覆盖文件。"
            }
        
        # 确保目录存在
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 准备 markdown 内容
        markdown_content = ""
        
        # 如果有标题，添加标题
        if title:
            markdown_content += f"# {title}\n\n"
        
        # 添加内容
        markdown_content += content
        
        # 如果内容不以换行符结尾，添加一个
        if not markdown_content.endswith('\n'):
            markdown_content += '\n'
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # 获取文件大小
        file_size = file_path.stat().st_size
        
        logger.info(f"成功写入文件: {file_path} ({file_size} 字节)")
        
        return {
            "success": True,
            "file_path": str(file_path),
            "filename": filename,
            "subfolder": subfolder or "根目录",
            "message": f"成功写入 Markdown 文件: {filename}",
            "file_size": file_size
        }
        
    except PermissionError:
        error_msg = f"权限不足，无法写入文件: {filename}"
        logger.error(error_msg)
        return {
            "success": False,
            "filename": filename,
            "message": error_msg
        }
    except OSError as e:
        error_msg = f"文件系统错误: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "filename": filename,
            "message": error_msg
        }
    except Exception as e:
        error_msg = f"未知错误: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "filename": filename,
            "message": error_msg
        }

@mcp.tool()
async def list_recent_md_files(limit: int = 10, subfolder: str = "") -> dict[str, Any]:
    """
    列出最近修改的 markdown 文件
    
    Args:
        limit: 返回文件数量限制
        subfolder: 可选的子文件夹（相对于基础路径）
        
    Returns:
        包含文件列表和统计信息的字典
    """
    try:
        # 确定搜索目录
        if subfolder:
            search_dir = STORAGE_PATH / subfolder
        else:
            search_dir = STORAGE_PATH
        
        if not search_dir.exists():
            return {
                "success": False,
                "message": f"目录不存在: {search_dir}",
                "files": []
            }
        
        if not search_dir.is_dir():
            return {
                "success": False,
                "message": f"路径不是目录: {search_dir}",
                "files": []
            }
        
        # 查找所有 .md 文件
        md_files = []
        for md_file in search_dir.glob("**/*.md"):
            if md_file.is_file():
                stat = md_file.stat()
                # 计算相对于基础路径的路径
                try:
                    relative_path = md_file.relative_to(STORAGE_PATH)
                except ValueError:
                    relative_path = md_file
                
                md_files.append({
                    "path": str(md_file),
                    "relative_path": str(relative_path),
                    "name": md_file.name,
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                    "created": stat.st_ctime
                })
        
        # 按修改时间排序
        md_files.sort(key=lambda x: x["modified"], reverse=True)
        
        # 限制返回数量
        md_files = md_files[:limit]
        
        return {
            "success": True,
            "message": f"找到 {len(md_files)} 个 Markdown 文件",
            "storage_path": str(STORAGE_PATH),
            "search_directory": str(search_dir),
            "subfolder": subfolder or "根目录",
            "files": md_files,
            "total_found": len(md_files)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"错误: {str(e)}",
            "files": []
        }

if __name__ == "__main__":
    # 通过 stdio 运行 MCP 服务器
    mcp.run()

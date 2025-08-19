# TXT to MD MCP 服务器

这是一个基于 FastMCP 的简单工具，用于将文本内容写入到 Markdown 文档。

PS:起因是vscode只能保存一定的量的历史，而且各项目之间历史也不互通，有些历史记录感觉有必要保存以下。看一些其他的memory mcp，感觉工具太多了没什么必要，所以弄个简单的就是为了存个对话历史。

## 功能特性

- 📝 将文本内容转换为 Markdown 格式并保存
- 📂 支持子文件夹组织
- 🔒 支持文件覆盖控制
- 📋 列出最近修改的 Markdown 文件
- 🚀 支持通过 stdio 方式启动
- ⚙️ 启动时指定存储路径

## 安装依赖

```bash
pip install fastmcp
```

## 使用方法

### 1. 直接运行服务器

```bash
# 使用默认路径
python server.py

# 指定存储路径
python server.py "d:\my-notes"
```

### 2. 在 VS Code 中配置

#### Claude Desktop 配置

在 Claude Desktop 的配置文件中添加：

```json
{
  "mcpServers": {
    "txt-to-md-converter": {
      "command": "python",
      "args": [
        "d:\\obsidian_storage\\default\\mcp\\txt-to-md-mcp\\server.py",
        "d:\\obsidian_storage\\default"
      ],
      "env": {}
    }
  }
}
```

#### VS Code 扩展配置

在 VS Code 的 `settings.json` 中添加：

```json
{
  "mcp.servers": [
    {
      "name": "txt-to-md-converter",
      "command": "python",
      "args": [
        "d:\\obsidian_storage\\default\\mcp\\txt-to-md-mcp\\server.py",
        "d:\\obsidian_storage\\default"
      ],
      "cwd": "d:\\obsidian_storage\\default\\mcp\\txt-to-md-mcp"
    }
  ]
}
```

### 3. 使用工具

#### write_txt_to_markdown

将文本内容写入 Markdown 文件：

```python
# 基本使用
{
    "content": "这是文本内容\\n\\n支持多行文本",
    "filename": "my-note"  # 会自动添加 .md 扩展名
}

# 高级使用
{
    "content": "## 会议记录\\n\\n- 讨论项目进度",
    "filename": "meeting_notes",
    "title": "每周会议记录",
    "subfolder": "work",  # 存储到 work 子文件夹
    "overwrite": true     # 覆盖已存在文件
}
```

#### list_recent_md_files

列出最近修改的 Markdown 文件：

```python
{
    "limit": 10,          # 返回文件数量限制
    "subfolder": "work"   # 可选：指定子文件夹
}
```

## stdio 启动方式说明

MCP 通过 stdio (标准输入/输出) 方式启动，实现与客户端的通信：

### 工作原理

1. **进程启动**: 客户端启动 MCP 服务器进程，传递存储路径参数
2. **通信管道**: 通过 stdin/stdout 进行 JSON-RPC 通信
3. **协议交互**: 初始化 → 工具注册 → 工具调用

### 启动参数

服务器接受一个可选的命令行参数作为存储路径：

```bash
python server.py [存储路径]
```

- 如果不提供参数，默认使用 `d:/obsidian_storage/default`
- 如果目录不存在，会自动创建

### 在不同客户端中的配置

1. **Claude Desktop**: 在 `args` 数组中添加存储路径
2. **VS Code 扩展**: 在配置的 `args` 中指定路径
3. **自定义客户端**: 启动进程时传递路径参数

## 测试

运行测试脚本验证功能：

```bash
python test_server.py
```

测试脚本会：

- 启动服务器（传递测试路径）
- 发送初始化请求
- 调用文件写入工具
- 验证结果

## 示例

### 快速笔记

```python
{
    "content": "今天学习了 MCP 协议\\n\\n- 支持 stdio 通信\\n- 使用 JSON-RPC",
    "filename": "mcp-learning"
}
```

### 项目文档

```python
{
    "content": "# 项目计划\\n\\n## 第一阶段\\n- 需求分析\\n- 架构设计",
    "filename": "project-plan",
    "title": "项目开发计划",
    "subfolder": "projects"
}
```

## 许可证

MIT License

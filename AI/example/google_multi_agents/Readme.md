# Google ADK Multi-Agents

## 快速启动

在 `AI/example/` 目录下执行：

```bash
cd AI/example
vim .env  # 配置 API 密钥和 Base URL
adk web --port 8009
```

## 项目结构

```
AI/example/
├── agent.py      # 主智能体代码
├── .env          # API 密钥配置
└── __init__.py
```

## 注意事项

- 使用官方 UI 时，主 agent 必须命名为 `root_agent`
- **重要**：API 密钥和 Base URL 必须配置在 `.env` 文件中，不能硬编码到代码中
- **演示说明**：本示例中的 `add` 工具故意返回错误的计算结果，用于演示 AI 如何调用工具并处理结果

## 参考文档

- [快速开始](https://adk.wiki/get-started/python/#create-an-agent-project)
- [代码执行](https://adk.wiki/agents/llm-agents/#code-execution)
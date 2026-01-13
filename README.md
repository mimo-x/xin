# xin

Knowledge base. 记录学习笔记、工具使用和最佳实践。

## 📚 编程基础

### Python

- [Python 命令行工具 (Click)](./paper/python-cli-click.md)
- [Python 函数重载 (singledispatch)](./paper/python-function-overloading.md)
- [Python-dotenv 环境变量管理](https://github.com/theskumar/python-dotenv)

### Golang

- [深度探索Go语言 runtime](./go/深度探索Go语言_runtime/parts/第00章-目录和前言.md)
- Gopher 🐹

## 🤖 AI

### 基础知识

- **Base of AI**: [Prompt caching: 10x cheaper LLM tokens](https://ngrok.com/blog/prompt-caching/)
- **Prompt Skills**: 提示词工程
  - [提示词工程指南](https://www.promptingguide.ai/zh)
  - [智能体防御：用户提示词加固方案](https://mp.weixin.qq.com/s/gwqbDFhGrCxOA3y741tDOg)

### 工具使用

- **Claude**: Claude 使用技巧 😲
- **Multi-agent system**: 多代理系统

### AI 基建

- **模型路由与兼容层**
  - [Claude Code Router](https://github.com/musistudio/claude-code-router): 多模型请求的路由与转发工具
  - [LiteLLM](https://github.com/BerriAI/litellm): 统一封装主流大模型 API
  - [UnionLLM](https://github.com/EvalsOne/UnionLLM/): 基于 LiteLLM 扩展，增加国内模型兼容支持

- **LLM API 转发层**
  - [new-api](https://github.com/QuantumNous/new-api): 统一的多模型 API 转发与代理服务
  - [one-api](https://github.com/songquanpeng/one-api): 兼容 OpenAI 标准接口的转发系统
  - [one-hub](https://github.com/MartialBE/one-hub): 在 one-api 基础上扩展，提供更灵活的模型分发功能

## 📝 最佳实践

- [如何写好代码](./paper/code_suggestion.md)
- [URL 设计最佳实践指南](./paper/url-design-best-practices.md)

## 🏗️ 系统设计

- **Coder**: 分布式架构、密集数据型系统设计

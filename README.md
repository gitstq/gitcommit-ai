# 🤖 GitCommit AI

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

🚀 **AI-powered Git commit message generator** with multi-model support. Automatically generate conventional commit messages from your code changes.

English | [简体中文](#简体中文) | [繁體中文](#繁體中文)

---

## ✨ Features

- 🤖 **Multiple AI Providers** - Support for OpenAI, Claude, Ollama, OpenRouter, DeepSeek
- 🌍 **Bilingual Support** - Generate commit messages in Chinese or English
- 📝 **Conventional Commits** - Follows the [Conventional Commits](https://www.conventionalcommits.org/) specification
- ⚡ **One-Command Operation** - Simple CLI with interactive prompts
- 🔧 **Highly Configurable** - Customize providers, models, and behavior
- 🏠 **Local AI Support** - Use Ollama for completely local processing
- 🎨 **Beautiful Terminal UI** - Rich, colorful output with progress indicators

## 🚀 Quick Start

### Installation

```bash
pip install gitcommit-ai
```

### Configuration

```bash
# Initialize configuration
gitcm init

# Or set environment variables
export OPENAI_API_KEY="your-api-key"
```

### Usage

```bash
# Stage your changes
git add .

# Generate and commit with AI
gitcm

# Or with options
gitcm --provider claude --language en --auto
```

## 📖 Documentation

### Supported Providers

| Provider | Setup | Local |
|----------|-------|-------|
| OpenAI | `OPENAI_API_KEY` | ❌ |
| Claude | `ANTHROPIC_API_KEY` | ❌ |
| Ollama | Local server | ✅ |
| OpenRouter | `OPENROUTER_API_KEY` | ❌ |
| DeepSeek | `DEEPSEEK_API_KEY` | ❌ |

### Commands

```bash
gitcm                    # Generate commit message
gitcm config             # Show configuration
gitcm status             # Show git status
gitcm init               # Initialize configuration
```

### Options

```bash
-p, --provider TEXT      AI provider to use
-l, --language TEXT      Language (zh/en)
-a, --auto               Auto-commit without confirmation
-d, --dry-run            Show message without committing
--version                Show version
```

## 💡 Design Philosophy

GitCommit AI aims to:
- Save developers time writing commit messages
- Enforce consistent commit message conventions
- Support multiple AI providers for flexibility
- Work offline with local AI models
- Provide a delightful CLI experience

## 📦 Packaging

This project uses modern Python packaging with `pyproject.toml`.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

# 简体中文

## 🤖 GitCommit AI

🚀 **AI驱动的Git提交消息生成器**，支持多种AI模型。自动根据代码变更生成符合规范的提交消息。

## ✨ 核心特性

- 🤖 **多AI模型支持** - 支持OpenAI、Claude、Ollama、OpenRouter、DeepSeek
- 🌍 **中英双语** - 支持生成中文或英文提交消息
- 📝 **约定式提交** - 遵循[Conventional Commits](https://www.conventionalcommits.org/)规范
- ⚡ **一键操作** - 简单的CLI，带交互式提示
- 🔧 **高度可配置** - 自定义提供商、模型和行为
- 🏠 **本地AI支持** - 使用Ollama实现完全本地处理
- 🎨 **精美终端UI** - 丰富的彩色输出和进度指示器

## 🚀 快速开始

### 安装

```bash
pip install gitcommit-ai
```

### 配置

```bash
# 初始化配置
gitcm init

# 或设置环境变量
export OPENAI_API_KEY="your-api-key"
```

### 使用

```bash
# 暂存更改
git add .

# 使用AI生成并提交
gitcm

# 或使用选项
gitcm --provider claude --language zh --auto
```

## 📖 详细文档

### 支持的提供商

| 提供商 | 设置 | 本地 |
|--------|------|------|
| OpenAI | `OPENAI_API_KEY` | ❌ |
| Claude | `ANTHROPIC_API_KEY` | ❌ |
| Ollama | 本地服务器 | ✅ |
| OpenRouter | `OPENROUTER_API_KEY` | ❌ |
| DeepSeek | `DEEPSEEK_API_KEY` | ❌ |

### 命令

```bash
gitcm                    # 生成提交消息
gitcm config             # 显示配置
gitcm status             # 显示git状态
gitcm init               # 初始化配置
```

### 选项

```bash
-p, --provider TEXT      使用的AI提供商
-l, --language TEXT      语言 (zh/en)
-a, --auto               自动提交，无需确认
-d, --dry-run            只显示消息，不提交
--version                显示版本
```

## 💡 设计理念

GitCommit AI旨在：
- 节省开发者编写提交消息的时间
- 强制执行一致的提交消息规范
- 支持多种AI提供商以提供灵活性
- 使用本地AI模型离线工作
- 提供愉悦的CLI体验

## 🤝 贡献

欢迎贡献！请参阅[CONTRIBUTING.md](CONTRIBUTING.md)。

## 📄 许可证

MIT许可证 - 详见[LICENSE](LICENSE)文件。

---

# 繁體中文

## 🤖 GitCommit AI

🚀 **AI驅動的Git提交訊息生成器**，支援多種AI模型。自動根據程式碼變更生成符合規範的提交訊息。

## ✨ 核心特性

- 🤖 **多AI模型支援** - 支援OpenAI、Claude、Ollama、OpenRouter、DeepSeek
- 🌍 **中英雙語** - 支援生成中文或英文提交訊息
- 📝 **約定式提交** - 遵循[Conventional Commits](https://www.conventionalcommits.org/)規範
- ⚡ **一鍵操作** - 簡單的CLI，帶互動式提示
- 🔧 **高度可配置** - 自定義提供商、模型和行為
- 🏠 **本地AI支援** - 使用Ollama實現完全本地處理
- 🎨 **精美終端UI** - 豐富的彩色輸出和進度指示器

## 🚀 快速開始

### 安裝

```bash
pip install gitcommit-ai
```

### 配置

```bash
# 初始化配置
gitcm init

# 或設定環境變數
export OPENAI_API_KEY="your-api-key"
```

### 使用

```bash
# 暫存更改
git add .

# 使用AI生成並提交
gitcm

# 或使用選項
gitcm --provider claude --language zh --auto
```

## 📖 詳細文檔

### 支援的提供商

| 提供商 | 設定 | 本地 |
|--------|------|------|
| OpenAI | `OPENAI_API_KEY` | ❌ |
| Claude | `ANTHROPIC_API_KEY` | ❌ |
| Ollama | 本地伺服器 | ✅ |
| OpenRouter | `OPENROUTER_API_KEY` | ❌ |
| DeepSeek | `DEEPSEEK_API_KEY` | ❌ |

### 命令

```bash
gitcm                    # 生成提交訊息
gitcm config             # 顯示配置
gitcm status             # 顯示git狀態
gitcm init               # 初始化配置
```

### 選項

```bash
-p, --provider TEXT      使用的AI提供商
-l, --language TEXT      語言 (zh/en)
-a, --auto               自動提交，無需確認
-d, --dry-run            只顯示訊息，不提交
--version                顯示版本
```

## 💡 設計理念

GitCommit AI旨在：
- 節省開發者編寫提交訊息的時間
- 強制執行一致的提交訊息規範
- 支援多種AI提供商以提供靈活性
- 使用本地AI模型離線工作
- 提供愉悅的CLI體驗

## 🤝 貢獻

歡迎貢獻！請參閱[CONTRIBUTING.md](CONTRIBUTING.md)。

## 📄 許可證

MIT許可證 - 詳見[LICENSE](LICENSE)文件。

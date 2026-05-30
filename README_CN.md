# Claudette – Sublime Text AI 助手

![Claudette Chat View](https://raw.githubusercontent.com/barryceelen/Claudette/main/screenshot.png "Ask AI")

一款 [Sublime Text](http://www.sublimetext.com) 插件，将 AI 对话集成到编辑器中。同时支持 **Anthropic Claude API** 和 **DeepSeek API**（通过 DeepSeek 的 Anthropic 兼容端点 `https://api.deepseek.com/anthropic`）。

在命令面板中输入 "Ask Question"，或通过 *Tools > Claudette > Ask Question* 提问。编辑器中的选中文本会自动作为上下文发送。需要配置 API Key。

## 功能特性

- 同时开启多个 AI 对话窗口
- 选中文本自动作为上下文发送
- 添加文件或文件夹到对话上下文
- 可在 Anthropic 和 DeepSeek 模型之间切换
- 自定义系统提示词（System Prompt）
- 对话历史：导出/导入 JSON 文件
- 多供应商支持：Anthropic Claude 和 DeepSeek 自由切换

## 快速开始

### 第一步：获取 API Key

- **DeepSeek**：[platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)
- **Claude**：[console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)

### 第二步：配置

菜单栏 *Preferences > Package Settings > Claudette > Settings*

**使用 DeepSeek：**
```jsonc
{
    "api_provider": "deepseek",
    "deepseek": {
        "api_key": "sk-你的key",
        "model": "deepseek-chat",
        "base_url": "https://api.deepseek.com/anthropic/"
    }
}
```

**使用 Claude（默认）：**
```jsonc
{
    "api_key": "sk-ant-你的key"
}
```

### 第三步：开始对话

`Ctrl+Shift+P` → `Claudette: Ask Question` → 输入问题 → 回车

输入框显示 **"Ask DeepSeek:"**（或 **"Ask Claude:"**），标签页显示 **"DeepSeek Chat"**（或 **"Claude Chat"**）。

> **注意：** Text Editor Tool（文件编辑工具）和 Web Search（网页搜索）是 Claude 专有功能，使用 DeepSeek 时自动禁用。

## 命令列表

所有命令通过 *Tools > Claudette* 菜单或命令面板使用。

| 命令 | 说明 |
|------|------|
| **Ask Question** | 打开输入面板提问。<kbd>Enter</kbd> 发送，<kbd>Shift+Enter</kbd> 换行。 |
| **Ask Question In New Chat** | 同上，但始终创建新的对话标签。 |
| **Clear Chat History** | 清除对话历史以减少 token 消耗。 |
| **Export Chat History** | 将当前对话保存为 JSON 文件。 |
| **Import Chat History** | 从 JSON 文件载入对话继续聊。 |
| **Add File to Chat** | 在侧边栏右键文件/文件夹添加到上下文。 |
| **Add Current File to Chat** | 将当前打开的文件加入上下文。 |
| **Remove Current File from Chat** | 从上下文中移除当前文件。 |
| **Add All Open Files to Chat** | 将所有打开的文件加入上下文。 |
| **Refresh Included Files** | 重新从磁盘读取上下文文件内容。 |
| **Show Included Files** | 管理已加入上下文的文件列表。 |
| **Clear Included Files** | 清除所有上下文文件。 |
| **Switch Model** | 从 API 获取可用模型列表并切换。 |
| **Switch System Prompt** | 选择已配置的系统提示词。 |
| **Switch API Key** | 在多个已配置的 API Key 之间切换。 |

## 快捷键

插件默认不带快捷键，在 *Preferences > Key Bindings* 中自定义：

```jsonc
[
    {
        "keys": ["ctrl+k", "ctrl+c"],
        "command": "claudette_ask_question"
    }
]
```

## 配置参考

| 设置项 | 默认值 | 说明 |
|--------|--------|------|
| `api_provider` | `"anthropic"` | API 供应商：`"anthropic"` 或 `"deepseek"` |
| `api_key` | `""` | Anthropic API Key |
| `base_url` | `"https://api.anthropic.com/v1/"` | Anthropic API 地址 |
| `model` | `"claude-sonnet-4-5"` | Claude 模型名称 |
| `deepseek.api_key` | `""` | DeepSeek API Key |
| `deepseek.base_url` | `"https://api.deepseek.com/anthropic/"` | DeepSeek Anthropic 兼容端点 |
| `deepseek.model` | `"deepseek-chat"` | DeepSeek 模型（`deepseek-chat` 或 `deepseek-reasoner`） |
| `deepseek.pricing` | `{...}` | DeepSeek 每百万 token 价格（美元） |
| `max_tokens` | `8192` | 每次回复最大输出 token 数 |
| `temperature` | `"1.0"` | 模型温度（0.0–1.0） |
| `system_messages` | `[...]` | 系统提示词列表 |
| `pricing` | `{...}` | Anthropic 每百万 token 价格（美元） |
| `web_search` | `false` | 启用网页搜索（仅 Anthropic） |
| `text_editor_tool` | `false` | 启用文件编辑工具（仅 Anthropic） |

## 安装

### 方式一：Package Control

1. 安装 [Package Control](https://packagecontrol.io/installation)
2. `Ctrl+Shift+P` → `Package Control: Install Package` → 搜索 `Claudette`

### 方式二：手动安装 .sublime-package

1. 下载 `Claudette.sublime-package`
2. 复制到对应目录：
   - **Windows**: `%APPDATA%\Sublime Text\Installed Packages\`
   - **macOS**: `~/Library/Application Support/Sublime Text/Installed Packages/`
   - **Linux**: `~/.config/sublime-text/Installed Packages/`
3. 重启 Sublime Text

### 方式三：开发模式

将项目文件夹放到 Packages 目录下：

- **Windows**: `%APPDATA%\Sublime Text\Packages\Claudette\`
- **macOS**: `~/Library/Application Support/Sublime Text/Packages/Claudette/`
- **Linux**: `~/.config/sublime-text/Packages/Claudette/`

## 隐私与法律

对话内容会发送到当前所选供应商的服务器。

- **Anthropic**：[隐私与法律](https://support.anthropic.com/en/collections/4078534-privacy-legal)
- **DeepSeek**：[隐私政策](https://platform.deepseek.com/privacy)

## 致谢

本插件主要由 Claude AI 编写。

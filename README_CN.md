# Claudette – Sublime Text AI 助手

一款 [Sublime Text](http://www.sublimetext.com) 插件，将 AI 对话集成到编辑器中。原生支持 **Anthropic Claude API**，同时支持任何 **第三方 Anthropic 兼容 API**（如 DeepSeek、OpenRouter 等），只需简单修改配置即可。

## 快速开始

### 1. 获取 API Key

- **Claude**：[console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
- **DeepSeek**：[platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)

### 2. 配置

菜单栏 *Preferences > Package Settings > Claudette > Settings*

**Claude（默认）：**
```jsonc
{
    "api_key": "sk-ant-你的key"
}
```

**DeepSeek：**
```jsonc
{
    "api_key": "sk-你的key",
    "model": "deepseek-chat",
    "base_url": "https://api.deepseek.com/anthropic/"
}
```

**其他 Anthropic 兼容 API：**
```jsonc
{
    "api_key": "你的key",
    "model": "你的模型名",
    "base_url": "https://你的端点/v1/"
}
```

只需改这三个配置项即可。插件会自动对比 `base_url` 与 Anthropic 默认地址来检测第三方 API，并自动禁用 Anthropic 专有功能（网页搜索、文件编辑工具、缓存控制、anthropic-version 请求头）。UI 标签始终显示 "Claude"。

### 3. 开始对话

`Ctrl+Shift+P` → `Claudette: Ask Question` → 输入问题 → 回车

## 功能特性

- 同时开启多个 AI 对话窗口
- 选中文本自动作为上下文发送
- 添加文件/文件夹到对话上下文
- 可在不同模型之间切换
- 自定义系统提示词
- 对话历史导出/导入 JSON
- 多供应商：任意 Anthropic 兼容 API

## 命令列表

所有命令通过 *Tools > Claudette* 菜单或命令面板使用。

| 命令 | 说明 |
|------|------|
| **Ask Question** | 打开输入面板。<kbd>Enter</kbd> 发送。 |
| **Ask Question In New Chat** | 始终创建新对话标签。 |
| **Clear Chat History** | 清除对话历史。 |
| **Export / Import Chat History** | 导出/导入对话 JSON。 |
| **Add File to Chat** | 侧边栏右键添加文件/文件夹到上下文。 |
| **Add Current/Open Files** | 添加打开的文件到上下文。 |
| **Refresh Included Files** | 刷新上下文文件。 |
| **Show / Clear Included Files** | 管理/清除上下文文件。 |
| **Switch Model** | 获取可用模型列表并切换。 |
| **Switch System Prompt** | 选择系统提示词。 |
| **Switch API Key** | 在多组 API Key 之间切换。 |

## 配置参考

| 设置项 | 默认值 | 说明 |
|--------|--------|------|
| `api_key` | `""` | API Key（字符串或 `{keys: [...], active_key: N}`） |
| `base_url` | `"https://api.anthropic.com/v1/"` | API 端点地址。修改后自动禁用 Anthropic 专有功能 |
| `model` | `"claude-sonnet-4-5"` | 模型名称 |
| `max_tokens` | `8192` | 每次回复最大 token 数 |
| `temperature` | `"1.0"` | 温度参数（0.0–1.0） |
| `system_messages` | `[...]` | 系统提示词列表 |
| `pricing` | `{...}` | 每百万 token 价格（美元），按模型名子串匹配 |
| `verify_ssl` | `true` | SSL 证书验证 |
| `custom_headers` | `{}` | 额外 HTTP 请求头 |
| `web_search` | `false` | 网页搜索（仅 Anthropic） |
| `text_editor_tool` | `false` | 文件编辑工具（仅 Anthropic） |

## 安装

### Package Control

1. 安装 [Package Control](https://packagecontrol.io/installation)
2. `Ctrl+Shift+P` → `Package Control: Install Package` → `Claudette`

### 手动安装 .sublime-package

将 `Claudette.sublime-package` 复制到：
- **Windows**：`%APPDATA%\Sublime Text\Installed Packages\`
- **macOS**：`~/Library/Application Support/Sublime Text/Installed Packages/`
- **Linux**：`~/.config/sublime-text/Installed Packages/`

重启 Sublime Text。

### 开发模式

克隆到 Packages 目录：
- **Windows**：`%APPDATA%\Sublime Text\Packages\Claudette\`
- **macOS**：`~/Library/Application Support/Sublime Text/Packages/Claudette/`
- **Linux**：`~/.config/sublime-text/Packages/Claudette/`

## 隐私与法律

对话内容会发送到所配置的 API 供应商服务器。
- **Anthropic**：[隐私与法律](https://support.anthropic.com/en/collections/4078534-privacy-legal)
- **DeepSeek**：[隐私政策](https://platform.deepseek.com/privacy)

## 致谢

本插件主要由 Claude AI 编写。

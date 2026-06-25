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
    "base_url": "https://api.deepseek.com/anthropic/",
    "models": ["deepseek-chat", "deepseek-reasoner"]
}
```

**其他 Anthropic 兼容 API：**
```jsonc
{
    "api_key": "你的key",
    "model": "你的模型名",
    "base_url": "https://你的端点/v1/",
    "models": ["你的模型名", "另一个模型"]
}
```

只需改这三个配置项即可。插件会自动对比 `base_url` 与 Anthropic 默认地址来检测第三方 API，并自动禁用 Anthropic 专有功能（文件编辑工具、缓存控制、anthropic-version 请求头）。客户端联网搜索和网页抓取**对所有供应商均有效**。可选的 `models` 列表用于 **Switch Model** 命令——当供应商没有 `/models` 端点（如 DeepSeek、OpenRouter）时仍可切换模型。UI 标签始终显示 "Claude"。

### 3. 开始对话

`Ctrl+Shift+P` → `Claudette: Ask Question` → 输入问题 → 回车

## 功能特性

- 同时开启多个 AI 对话窗口
- **联网搜索** — 每次提问自动搜索（可配置），所有供应商均可用
- **网页抓取** — AI 可读取任意 URL 内容（所有供应商均可用，与自动搜索同时开启也有效）
- **客户端工具** — `web_fetch` 和 `client_web_search` 在本地执行，对任意 Anthropic 兼容供应商都有效
- 选中文本自动作为上下文发送
- 添加文件/文件夹到对话上下文
- 可在不同模型之间切换
- 自定义系统提示词
- 对话历史导出/导入 JSON
- 多供应商：任意 Anthropic 兼容 API
- 每把 API Key 可单独覆盖 `base_url` / `model`（Claude 与 DeepSeek 并存使用）

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
| `models` | `[]` | 可选的静态模型列表，用于 Switch Model（供应商无 `/models` 端点时，如 DeepSeek） |
| `max_tokens` | `8192` | 每次回复最大 token 数 |
| `request_timeout` | `180` | 单次请求超时秒数（推理模型可能较慢） |
| `temperature` | `"1.0"` | 采样温度。Anthropic 上限 1.0；其他供应商允许至 2.0。超范围自动夹紧 |
| `system_messages` | `[...]` | 系统提示词列表 |
| `pricing` | `{...}` | 每百万 token 价格（美元），按模型名子串匹配 |
| `verify_ssl` | `true` | SSL 证书验证 |
| `custom_headers` | `{}` | 额外 HTTP 请求头 |
| `force_web_search` | `true` | 每次提问自动搜索（所有供应商） |
| `enable_web_fetch` | `true` | AI 可抓取 URL 内容（所有供应商） |
| `enable_client_web_search` | `true` | AI 自主决定搜索（force_web_search 关闭时） |
| `web_search_backend` | `"duckduckgo"` | 搜索后端：`"duckduckgo"` 或 `"searxng"` |
| `searxng_instance_url` | `"https://searx.be"` | 自定义 SearXNG 实例地址 |
| `web_search` | `false` | 服务端网页搜索（仅 Anthropic） |
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

### 重新构建 `.sublime-package`

修改源码后重新打包：

```bash
python build_package.py
```

此脚本会先剥离 `.py`/`.pyi` 文件的 BOM（Sublime 的 zip 导入器无法处理 BOM），再将源码打包为 `Claudette.sublime-package`。把生成文件复制到 `Installed Packages/` 目录并重启 Sublime Text 即可。

### 运行独立测试套件

`test_standalone.py` 无需启动 Sublime Text，直接对当前配置的供应商执行 API 层测试。它 mock 了 `sublime`/`sublime_plugin` 模块并发起真实请求：

```bash
python test_standalone.py
```

测试覆盖：温度夹紧、供应商检测、模型拉取、`web_fetch` 工具循环、流式响应、搜索后端。运行前先在 `User/Claudette.sublime-settings` 中配置好供应商。

## 联网搜索说明

`force_web_search`（默认开启）会在每次提问时先用你的问题搜索网络，将结果提供给 AI 作为上下文。这确保 AI 始终能回答最新信息。当搜索失败时（如网络不可达），插件会显示状态提示并继续作答，不会阻塞。

### 搜索后端

| 后端 | 说明 |
|------|------|
| **DuckDuckGo**（默认） | 免费，无需 API Key。先抓取 HTML 搜索结果，失败再回退到即时答案 API。 |
| **SearXNG** | 开源元搜索引擎，需配置实例地址。可自建或使用公共实例。 |

### 网络环境提示

- 如 DuckDuckGo 不可达（常见于中国大陆网络），请切换为 SearXNG 并配置可用实例：
  ```jsonc
  {
      "web_search_backend": "searxng",
      "searxng_instance_url": "https://你的实例地址"
  }
  ```
- 也可将 `force_web_search` 设为 `false` 关闭自动搜索，改为 AI 自主决定模式
- `web_fetch` 直接抓取 URL，只要目标网站可访问即可工作

## 隐私与法律

对话内容会发送到所配置的 API 供应商服务器。
- **Anthropic**：[隐私与法律](https://support.anthropic.com/en/collections/4078534-privacy-legal)
- **DeepSeek**：[隐私政策](https://platform.deepseek.com/privacy)

## 致谢

本插件主要由 Claude AI 编写。

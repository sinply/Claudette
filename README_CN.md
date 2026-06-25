# Claudette – Sublime Text AI 助手

一款 [Sublime Text](http://www.sublimetext.com) 插件，将 AI 对话集成到编辑器中。原生支持 **Anthropic Claude API**，同时支持任何 **第三方 Anthropic 兼容 API**（如 DeepSeek、OpenRouter 等），只需简单修改配置即可。

---

## 快速开始

### 1. 获取 API Key

- **Claude**：[console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
- **DeepSeek**：[platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)

### 2. 配置

菜单栏 *Preferences → Package Settings → Claudette → Settings*

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

只需改这三个配置项即可。插件会自动对比 `base_url` 与 Anthropic 默认地址来检测第三方 API，并自动禁用 Anthropic 专有功能（文件编辑工具、缓存控制、`anthropic-version` 请求头）。客户端联网搜索和网页抓取**对所有供应商均有效**。可选的 `models` 列表用于 **Switch Model** 命令——当供应商没有 `/models` 端点（如 DeepSeek、OpenRouter）时仍可切换模型。UI 标签始终显示 "Claude"。

### 3. 开始对话

`Ctrl+Shift+P` → `Claudette: Ask Question` → 输入问题 → 回车

---

## 使用指南

### 打开对话视图

开始一段对话有两种方式：

- **Claudette: Ask Question** — 打开输入面板。提交时，插件会复用当前窗口的"当前对话标签"，若不存在则新建一个。日常多轮对话用这个。
- **Claudette: Ask Question In New Chat View** — 始终新建一个对话标签并设为当前标签。需要干净上下文、不延续之前对话时用这个。

每个 Sublime Text 窗口各自跟踪自己的"当前对话"标签。若一个窗口里有多个对话标签，聚焦某个标签即把它标为当前对话——下一次 **Ask Question** 会进入这里。你可以在不同窗口开不同对话，也可以在一个窗口开多个标签。

对话视图是一个名为 `Claude Chat` 的只读 Markdown 视图，使用 Markdown 语法高亮，所以 AI 回复（标题、列表、代码块）都能正确高亮显示。

### 提问

1. 运行 **Claudette: Ask Question**（命令面板或 *Tools → Claudette* 菜单）。
2. 窗口底部出现输入面板，提示符为 `Ask Claude:`。
3. 输入问题，按 `Enter` 发送。（`Esc` 取消输入面板，不发送。）
4. 问题追加到对话视图，视图平滑滚动到该问题，请求开始。

**带选中代码提问：** 运行 **Ask Question** 时，若任一编辑器视图中有选中文本，会在输入面板打开*之前*自动捕获，并作为上下文一起发送。对话视图里会在 `**Selected Code**` 标题下显示，发给 API 的实际消息会把你的问题和代码合并在一起。

> 在部分系统上（ notably ST4 on Windows），在输入面板里按 `Enter` 可能插入换行而非提交。插件会检测末尾换行并视为提交，因此 `Enter` 始终能发送。

### 快捷键（对话视图内）

| 按键 | 动作 |
|------|------|
| `Enter` | 提交新问题（打开输入面板，然后发送） |
| `Esc` | 停止当前对话标签正在进行的请求 |

这两个绑定仅在对话视图聚焦时生效（`claudette_is_chat_view` 设置为 `true`）。定义于 `Default.sublime-keymap`，可在用户键位文件中覆盖。

### 跟随响应

AI 思考时，会显示一个内联状态幻影（如 `ℹ️ Pondering ✻`）带动画 spinner。回复按 token 流式输出。流式结束后：

- 状态幻影清除。
- 每个围栏代码块下方出现一个 **Copy** 按钮，点击即可把该块代码复制到剪贴板。
- 若代码块在中途被截断（你点了停止，或 `max_tokens` 用尽），插件会自动补上闭合围栏，避免 Markdown 高亮断裂。

**Token / 费用显示：** 若 `chat.show_cost` 为 `true`（默认），每次回复后显示状态行：

```
⚡️ Tokens: 1,234 in, 567 out. Cost: $0.0023 ($0.0156 session)
```

同时显示本次费用和会话累计费用。价格取自 `pricing` 设置（见[配置指南](#配置指南)）。

### 停止请求

在对话视图聚焦时按 `Esc`，或运行 **Claudette: Stop Request**。仅取消该对话标签的进行中 HTTP 请求——其他标签不受影响。已经流式输出的部分会留在视图里并加入对话历史，可从此处继续对话。

### 添加文件/文件夹作为上下文

可以把文件内容附加到对话里让 AI 看到：

| 操作 | 方法 |
|------|------|
| **添加当前文件** | *Tools → Claudette → Chat Context → Add Current File To Chat*，或编辑器内右键 → *Claudette → Add File to Chat* |
| **移除当前文件** | *Tools → Claudette → Chat Context → Remove Current File From Chat*，或右键 → *Claudette → Remove from Chat* |
| **从侧边栏添加文件/文件夹** | 在侧边栏右键文件或文件夹 → *Claudette → Claudette*（调用 `claudette_context_add_files`）。文件夹递归扫描，非文本文件跳过。 |
| **添加所有打开的文件** | *Tools → Claudette → Chat Context → Add All Open Files To Chat* |
| **刷新** | *Tools → Claudette → Chat Context → Refresh Included Files* — 从磁盘重新读取所有已包含文件 |
| **列表 / 清空** | *Show Included Files* 打开面板列出全部；*Clear Included Files* 清空全部 |

文件在添加（或刷新）时读取一次，之后每次请求将其内容前置到系统消息。它们**不会**在每轮自动重读——编辑后请用 **Refresh Included Files**。

### 切换模型 / 系统提示词 / API Key

- **Switch Model** — 从供应商 `/models` 端点拉取模型列表并在快速面板中展示。若端点不可用（DeepSeek、OpenRouter 等多数非 Anthropic 供应商返回 404 或空），则回退到 `models` 设置。选择后立即更新活动 `model`，下次请求生效。
- **Switch System Prompt** — 在 `system_messages` 列表中循环切换。活动项在下次请求时作为系统消息发送。若活动项是空字符串 `""`，则不发送系统消息。
- **Switch API Key** — 仅在 `api_key` 配置为含多个 key 的对象时有意义。弹出 key 名称快速面板，选择后即设为活动 key。无需改设置即可在 Claude key 和 DeepSeek key 间切换——**尤其当每个 key 自带 `base_url`/`model` 覆盖时**（见[多供应商并存](#多供应商并存)）。

### 对话历史

- **Clear Chat History** — 清空当前对话标签的对话历史（可见文本也会清空）。用于在不新建标签的情况下减少 token 占用。
- **Export Chat History** — 把当前对话导出为 JSON 文件（通过文件对话框保存）。便于留档或分享。
- **Import Chat History** — 把之前导出的 JSON 导入到当前对话标签，对话从导入状态继续。

---

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

所有命令通过 *Tools → Claudette* 菜单或命令面板（`Ctrl+Shift+P`）使用。

| 命令 | 说明 |
|------|------|
| **Ask Question** | 打开输入面板。<kbd>Enter</kbd> 发送。复用当前对话标签。 |
| **Ask Question In New Chat View** | 始终创建新对话标签。 |
| **Stop Request** | 取消当前对话标签正在进行的请求。 |
| **Clear Chat History** | 清除对话历史。 |
| **Export / Import Chat History** | 导出/导入对话 JSON。 |
| **Add File to Chat** | 侧边栏右键添加文件/文件夹到上下文。 |
| **Add Current/Open Files** | 添加打开的文件到上下文。 |
| **Refresh Included Files** | 刷新上下文文件。 |
| **Show / Clear Included Files** | 管理/清除上下文文件。 |
| **Switch Model** | 获取可用模型列表并切换（或使用 `models` 列表）。 |
| **Switch System Prompt** | 选择系统提示词。 |
| **Switch API Key** | 在多组 API Key 之间切换。 |

---

## 配置指南

通过 *Preferences → Package Settings → Claudette → Settings* 打开设置。会以分屏视图打开：左侧是包默认（只读），右侧是你的用户设置。**只编辑右侧。** 设置文件是 JSONC——允许 `//` 注释和尾随逗号。

下列所有设置都在 `Claudette.sublime-settings` 中。修改在下次请求时生效，无需重启。

### 核心设置

#### `api_key` *(字符串或对象，默认 `""`)*

单个 key，或多 key 配置。单供应商用字符串即可：

```jsonc
{ "api_key": "sk-ant-..." }
```

多 key（如 Claude + DeepSeek 并存）用对象形式。每个条目可自带 `base_url` 和 `model`，覆盖顶层设置——这样一个 Sublime 窗口就能同时对接两个供应商，用 **Switch API Key** 切换：

```jsonc
{
    "api_key": {
        "keys": [
            {
                "name": "Claude",
                "key": "sk-ant-...",
                "base_url": "https://api.anthropic.com/v1/",
                "model": "claude-sonnet-4-5"
            },
            {
                "name": "DeepSeek",
                "key": "sk-...",
                "base_url": "https://api.deepseek.com/anthropic/",
                "model": "deepseek-chat"
            }
        ],
        "active_key": 0
    }
}
```

`active_key` 是当前活动 key 的零基索引。**Switch API Key** 会更新它。若某个 key 条目省略了 `base_url`/`model`，则使用顶层值。

#### `base_url` *(字符串，默认 `"https://api.anthropic.com/v1/"`)*

API 端点。末尾 `/` 缺失会自动补上。**供应商检测**：把它（去掉末尾斜杠后）与 Anthropic 默认值比较——若不同，Anthropic 专有功能（`text_editor_tool`、`cache_control`、`anthropic-version` 请求头、服务端 `web_search`）自动禁用，温度上限从 1.0 提到 2.0。

#### `model` *(字符串，默认 `"claude-sonnet-4-5"`)*

请求中发送的模型 id。用 **Switch Model** 可不改设置直接切换。

#### `models` *(列表，默认 `[]`)*

当供应商没有 `/models` 端点（DeepSeek、OpenRouter 等）时，**Switch Model** 使用的静态模型列表。例：

```jsonc
"models": ["deepseek-chat", "deepseek-reasoner"]
```

非空时，**Switch Model** 显示此列表而非查询 API。

#### `max_tokens` *(整数，默认 `8192`)*

每次回复最大输出 token 数。**不得超过模型输出上限**——否则 API 返回 400。常见上限：

| 模型系列 | 输出上限 |
|----------|----------|
| Claude Opus 4.6 | 128,000 |
| Claude Sonnet 4.5 / Haiku 4.5 | 64,000 |
| Claude Sonnet 4 / Opus 4 | 8,192 |
| DeepSeek chat / reasoner | 8,192 |

#### `request_timeout` *(整数，默认 `180`)*

单次请求超时秒数。带工具循环的非流式请求（网页抓取、客户端搜索、文件编辑）在推理模型（如 DeepSeek reasoner 先思考再回复）上可能较慢。超时则调大。流式请求同样受此约束。

#### `temperature` *(字符串，默认 `"1.0"`)*

采样温度，按供应商夹紧：Anthropic `0.0`–`1.0`，其他 `0.0`–`2.0`。超范围夹紧到最近边界；非数值回退为 `1.0`。以字符串存储，因为 Sublime 设置对不带引号的数字精度有限。

#### `system_messages` *(列表，默认 3 条提示词)*

系统提示词列表。**Switch System Prompt** 在其中循环。每项在下次请求时作为系统消息发送。空字符串 `""` 表示"不发送系统消息"。

```jsonc
"system_messages": [
    "You are a helpful AI assistant focused on programming help.",
    "You are a helpful AI assistant focused on writing and documentation.",
    ""
]
```

`default_system_message_index`（整数，默认 `0`）选启动时的活动项。

#### `pricing` *(对象，默认含 Claude 档位 + DeepSeek 条目)*

每百万 token 价格（美元），用于每次回复后的费用行。键按模型名的**大小写不敏感子串**匹配——第一个匹配胜出。为你用的每个模型加一条：

```jsonc
"pricing": {
    "haiku":  { "input": 1,    "output": 5,    "cache_write": 1.25, "cache_read": 0.1  },
    "sonnet": { "input": 3,    "output": 15,   "cache_write": 3.75, "cache_read": 0.3  },
    "opus":   { "input": 5,    "output": 25,   "cache_write": 6.25, "cache_read": 0.5  },
    "deepseek-chat":    { "input": 0.27, "output": 1.10 },
    "deepseek-reasoner":{ "input": 0.55, "output": 2.19 }
}
```

`cache_write`/`cache_read` 仅对 Anthropic 有效（提示词缓存）。若模型无匹配条目，费用行显示 `$0.0000`。

### 网络设置

#### `verify_ssl` *(布尔，默认 `true`)*

SSL 证书验证。仅在可信开发服务器使用自签证书时设为 `false`。**关闭会降低安全性**——生产 key 切勿关闭。

#### `custom_headers` *(对象，默认 `{}`)*

附加到每个 API 请求的额外 HTTP 头。用于代理认证、自定义 `anthropic-version` 覆盖、供应商专属网关：

```jsonc
"custom_headers": {
    "X-Custom-Auth": "bearer xyz",
    "Anthropic-Beta": "interleaved-thinking-2025-05-14"
}
```

### 联网设置

有 3 个**相互独立**的客户端联网开关，外加 2 个仅 Anthropic 的服务端工具：

| 设置 | 默认 | 适用范围 | 行为 |
|------|------|----------|------|
| `force_web_search` | `true` | 所有供应商 | 每次提问*前*自动搜索，结果作为上下文。使用流式模式。 |
| `enable_web_fetch` | `true` | 所有供应商 | 给 AI 一个 `web_fetch` 工具，读取它想跟进的 URL。 |
| `enable_client_web_search` | `true` | 所有供应商 | 给 AI 一个 `client_web_search` 工具自主搜索。仅在 `force_web_search` 为 `false` 时激活。 |
| `web_search` | `false` | **仅 Anthropic** | 服务端网页搜索工具（$10 / 1000 次搜索）。非 Anthropic 自动禁用。 |
| `text_editor_tool` | `false` | **仅 Anthropic** | 服务端文件编辑工具。非 Anthropic 自动禁用。 |

**交互关系：**

- 若 `force_web_search` 开（默认），每次提问都预搜索。`enable_web_fetch` 仍可与之共存——AI 可读取搜索结果里的 URL。
- 若关闭 `force_web_search`，把 `enable_client_web_search` 设为 `true`，让 AI 在需要时仍能搜索。
- 要完全离线，把三个客户端开关都设为 `false`。

#### `web_search_backend` *(字符串，默认 `"duckduckgo"`)*

`force_web_search` 和 `client_web_search` 使用的后端：

- `"duckduckgo"` — 免费，无需 API Key。先抓 HTML 搜索结果，失败回退到即时答案 API。
- `"searxng"` — 开源元搜索。需配置 `searxng_instance_url`。

#### `searxng_instance_url` *(字符串，默认 `"https://searx.be"`)*

SearXNG 实例地址。仅在 `web_search_backend` 为 `"searxng"` 时使用。公共实例：[searx.be](https://searx.be)、[searx.work](https://searx.work)，或自建。

### 仅 Anthropic 的工具设置

仅当 `base_url` 指向 Anthropic 时生效。第三方供应商自动禁用（忽略）。

| 设置 | 默认 | 说明 |
|------|------|------|
| `web_search_max_uses` | `5` | 每次请求服务端搜索次数上限（1–20）。 |
| `web_search_allowed_domains` | `[]` | 只包含这些域名的结果。 |
| `web_search_blocked_domains` | `[]` | 排除这些域名的结果。 |
| `web_search_user_location` | *(未设)* | 本地化结果。`{ "type": "approximate", "city": "...", "region": "...", "country": "...", "timezone": "..." }` |
| `text_editor_tool_roots` | `[]` | 文件操作的额外允许根（路径须在这些根或项目文件夹下）。 |
| `text_editor_tool_max_characters` | *(未设)* | 查看文件时最大字符数（0 = 无限制）。 |

### 对话视图设置

```jsonc
"chat": {
    "line_numbers": false,
    "rulers": false,
    "set_scratch": true,
    "show_cost": true
}
```

| 键 | 默认 | 说明 |
|----|------|------|
| `line_numbers` | `false` | 对话视图显示行号。 |
| `rulers` | `false` | 对话视图显示标尺。 |
| `set_scratch` | `true` | 把对话视图标记为 scratch——关闭时不提示保存。 |
| `show_cost` | `true` | 每次回复后显示 token/费用行。 |

---

## 常见场景

### 最小 Claude 配置

```jsonc
{
    "api_key": "sk-ant-你的key",
    "model": "claude-sonnet-4-5"
}
```

其余用合理默认值。

### DeepSeek（中国大陆友好）

DeepSeek 的 `/anthropic/` 端点与 Anthropic 兼容。`/models` 端点返回 404，故手动设置 `models` 列表供 **Switch Model** 使用：

```jsonc
{
    "api_key": "sk-你的key",
    "base_url": "https://api.deepseek.com/anthropic/",
    "model": "deepseek-chat",
    "models": ["deepseek-chat", "deepseek-reasoner"],
    "temperature": "1.5"
}
```

若默认搜索后端 DuckDuckGo 在你的网络不可达，切换到可用的 SearXNG 实例或关闭自动搜索：

```jsonc
{
    "web_search_backend": "searxng",
    "searxng_instance_url": "https://你的可用实例地址"
}
```

…或关闭自动搜索，改由 AI 自主决定：

```jsonc
{ "force_web_search": false, "enable_client_web_search": true }
```

### 多供应商并存

两个 key 各自带 `base_url`/`model` 覆盖，用 **Switch API Key** 切换：

```jsonc
{
    "api_key": {
        "keys": [
            {
                "name": "Claude",
                "key": "sk-ant-...",
                "base_url": "https://api.anthropic.com/v1/",
                "model": "claude-sonnet-4-5"
            },
            {
                "name": "DeepSeek",
                "key": "sk-...",
                "base_url": "https://api.deepseek.com/anthropic/",
                "model": "deepseek-reasoner"
            }
        ],
        "active_key": 0
    },
    "models": ["deepseek-chat", "deepseek-reasoner"]
}
```

`text_editor_tool` 和服务端 `web_search` 在活动 key 指向 DeepSeek 时自动禁用，切回 Claude 时自动启用——无需手动切换。

### 自建开发服务器

本地代理使用自签证书：

```jsonc
{
    "api_key": "dev-key",
    "base_url": "https://localhost:8443/v1/",
    "verify_ssl": false,
    "custom_headers": { "X-Dev-Origin": "sublime" }
}
```

### 完全离线（无联网）

```jsonc
{
    "force_web_search": false,
    "enable_web_fetch": false,
    "enable_client_web_search": false
}
```

AI 仅从训练数据和已包含的文件回答。

### 关闭自动搜索但保留按需抓取

```jsonc
{
    "force_web_search": false,
    "enable_web_fetch": true,
    "enable_client_web_search": true
}
```

AI 自行决定何时搜索或抓取，而非每次提问都自动搜索。

---

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

---

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

---

## 隐私与法律

对话内容会发送到所配置的 API 供应商服务器。
- **Anthropic**：[隐私与法律](https://support.anthropic.com/en/collections/4078534-privacy-legal)
- **DeepSeek**：[隐私政策](https://platform.deepseek.com/privacy)

## 致谢

本插件主要由 Claude AI 编写。

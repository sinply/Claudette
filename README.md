# Claudette – AI Assistant for Sublime Text

![Claudette Chat View](https://raw.githubusercontent.com/barryceelen/Claudette/main/screenshot.png "Ask AI")

A [Sublime Text](http://www.sublimetext.com) package that integrates AI chat into your editor. Supports both the **Anthropic Claude API** and the **DeepSeek API** (via Anthropic-compatible endpoint).

Type "Ask Question" in the command palette or find the *Claudette > Ask Question* item in the *Tools* menu to ask a question. Any selected text in the current file will be sent along to the AI. Note that an API key is required.

## Features

- Chat with AI in multiple chat windows at the same time
- Automatically include selected text as context for your questions
- Include one or more files in the chat context
- Choose between different AI models from Anthropic or DeepSeek
- Configure custom system prompts to customize AI behavior
- Chat History: Export and import conversations as JSON files
- Multi-provider support: switch between Anthropic Claude and DeepSeek

## Quick Start

### Step 1: Get an API Key

- **DeepSeek**: [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)
- **Claude**: [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)

### Step 2: Configure

*Preferences > Package Settings > Claudette > Settings*

**DeepSeek:**
```jsonc
{
    "api_provider": "deepseek",
    "deepseek": {
        "api_key": "sk-your-key-here",
        "model": "deepseek-chat"
    }
}
```

**Claude (default):**
```jsonc
{
    "api_key": "sk-ant-your-key-here"
}
```

### Step 3: Ask a Question

`Ctrl+Shift+P` → `Claudette: Ask Question` → 输入问题 → 回车

输入框会显示 **"Ask DeepSeek:"**（或 **"Ask Claude:"**），标签页会显示 **"DeepSeek Chat"**（或 **"Claude Chat"**）。

> **注意：** Text Editor Tool（文件编辑）和 Web Search（网页搜索）是 Claude 专有功能，使用 DeepSeek 时自动禁用。

## Commands

All commands are available via the *Tools > Claudette* menu or via the command palette.

- **Ask Question**  
*claudette\_ask\_question*  
Opens a question input prompt. Submit your question with the <kbd>⏎ Enter</kbd> key. <kbd>⇧ Shift</kbd> + <kbd>⏎ Enter</kbd> for line breaks.  
**Pro tip:** In a chat view, press <kbd>Enter</kbd> to ask a question.

- **Ask Question In New Chat View**  
*claudette\_ask\_new\_question*  
Opens a question input prompt. A new chat view will open if there is an existing conversation in the current view. Useful for having multiple simultaneous chats, each with their own context and history.

- **Clear Chat History**   
*claudette\_clear\_chat\_history*  
Clear the chat history to reduce token usage while keeping previous messages visible in the interface. Prevents resending previous messages in a conversation when a new question is asked.

- **Export Chat History**  
*claudette\_export\_chat\_history*  
Save any chat conversation. Run this command to export the most recently active chat view in the current window to a JSON file.

- **Import Chat History**  
*claudette\_import\_chat\_history*  
Import a chat history JSON file and continue the conversation where it left off.

- **Add File to Chat**  
*claudette\_context\_add\_files*  
Available as a context menu item in the file list. Include one or more files or the content of a folder to the chat context.

- **Add Current File To Chat**  
*claudette\_context\_add\_current\_file*  
Add the content of the currently open view to the chat context.

- **Remove Current File From Chat**  
*claudette\_context\_remove\_current\_file*  
Remove the content of the currently open view from the chat context, if it has been added before.

- **Add All Open Files To Chat**  
*claudette\_context\_add\_open\_files*  
Add the content of the currently open files to the chat context.

- **Refresh Included Files**  
*claudette\_context\_refresh\_files*  
Update the content of the files in the chat context with their latest version.

- **Show Included Files**  
*claudette\_context\_manage\_files*  
Manage the list of files that are currently included in the chat context.

- **Clear Included Files**  
*claudette\_context\_clear\_files*  
Remove all included files from the chat context.

- **Switch Model**  
*claudette\_select\_model\_panel*  
Switch between available models. Fetches models from the active provider's API. Claude Sonnet 4.5 is the default for Anthropic; DeepSeek-Chat is the default for DeepSeek.

- **Switch System Prompt**  
*claudette\_select\_system\_message\_panel*  
Improve AI performance by using a system prompt. You can create and manage multiple prompts.

- **Switch API Key**
*claudette\_select\_api\_key\_panel*
Claudette supports multiple API keys. Configure named keys in settings and switch between them at runtime.

## Keyboard shortcuts

The Claudette package does not add [key bindings](https://www.sublimetext.com/docs/key_bindings.html) out of the box. You can add your own keyboard shortcuts via the *Settings > Keybindings* settings menu. The following example adds a keyboard shortcut that opens the "Ask Question" panel.

For macOS:

```
[
	{
		"keys": ["super+k", "super+c"],
		"command": "claudette_ask_question",
	}
]
```

For Linux and Windows:

```
[
	{
		"keys": ["ctrl+k", "ctrl+c"],
		"command": "claudette_ask_question",
	}
]
```

## Settings Reference

| Setting | Default | Description |
|---------|---------|-------------|
| `api_provider` | `"anthropic"` | API provider: `"anthropic"` or `"deepseek"` |
| `api_key` | `""` | Anthropic API key (string or `{keys: [...], active_key: N}`) |
| `base_url` | `"https://api.anthropic.com/v1/"` | Anthropic API base URL |
| `model` | `"claude-sonnet-4-5"` | Claude model name |
| `deepseek.api_key` | `""` | DeepSeek API key |
| `deepseek.base_url` | `"https://api.deepseek.com/v1/"` | DeepSeek API base URL |
| `deepseek.model` | `"deepseek-chat"` | DeepSeek model name |
| `deepseek.pricing` | `{...}` | DeepSeek pricing per 1M tokens |
| `max_tokens` | `8192` | Maximum output tokens per response |
| `temperature` | `"1.0"` | Model temperature (0.0–1.0) |
| `system_messages` | `[...]` | List of system prompts |
| `pricing` | `{...}` | Anthropic pricing per 1M tokens |
| `web_search` | `false` | Enable web search (Anthropic only) |
| `text_editor_tool` | `false` | Enable file editing tool (Anthropic only) |

## Installation

### 方法一：Package Control

1. 安装 [Package Control](https://packagecontrol.io/installation)
2. `Ctrl+Shift+P` → `Package Control: Install Package` → 输入 `Claudette` → 安装

### 方法二：手动安装 .sublime-package 文件

1. `Win+R` → 输入 `%APPDATA%\Sublime Text\Installed Packages` → 回车
2. 把 `Claudette.sublime-package` 复制进去
3. 重启 Sublime Text

### 方法三：开发模式（Packages 目录）

把项目文件夹直接放到 `%APPDATA%\Sublime Text\Packages\Claudette\`，适合二次开发调试。

### Building .sublime-package

```bash
# .sublime-package 就是一个 zip 文件
python -c "
import zipfile, os
src = 'Claudette'
dst = 'Claudette.sublime-package'
exclude = {'.git', '.gitattributes', '.gitignore', '.python-version',
           '.repomixignore', 'pyproject.toml', 'pyrightconfig.json',
           'repomix.config.json', '__pycache__'}
with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in exclude]
        for f in files:
            if not f.endswith('.pyc'):
                full = os.path.join(root, f)
                zf.write(full, os.path.relpath(full, src))
"
```

### 配置 API Key

1. 获取 API Key：[DeepSeek](https://platform.deepseek.com/api_keys) 或 [Anthropic](https://console.anthropic.com/)
2. 菜单栏 `Preferences > Package Settings > Claudette > Settings`
3. 配置 provider 和对应的 api_key（参考上方 Quick Start）

## What's new

[Release History](https://github.com/barryceelen/Claudette/releases)

## Privacy & legal

Everything that you share with the AI API, for example by including it in a chat, will be sent to the provider's servers.

- **Anthropic Claude:** [Privacy & Legal documentation](https://support.anthropic.com/en/collections/4078534-privacy-legal)
- **DeepSeek:** [Privacy Policy](https://platform.deepseek.com/privacy)

## Credits

The package is for the most part written by Claude AI itself.

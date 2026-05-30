# Claudette – AI Assistant for Sublime Text

A [Sublime Text](http://www.sublimetext.com) package that integrates AI chat into your editor. Supports the **Anthropic Claude API** natively, and any **third-party Anthropic-compatible API** (DeepSeek, OpenRouter, etc.) via a simple config change.

## Quick Start

### 1. Get an API Key

- **Claude**: [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
- **DeepSeek**: [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)

### 2. Configure

*Preferences > Package Settings > Claudette > Settings*

**Claude (default):**
```jsonc
{
    "api_key": "sk-ant-your-key-here"
}
```

**DeepSeek:**
```jsonc
{
    "api_key": "sk-your-key-here",
    "model": "deepseek-chat",
    "base_url": "https://api.deepseek.com/anthropic/"
}
```

**Any other Anthropic-compatible API:**
```jsonc
{
    "api_key": "your-key",
    "model": "your-model",
    "base_url": "https://your-endpoint/v1/"
}
```

That's it — just change `base_url`, `model`, and `api_key`. The plugin auto-detects third-party APIs by comparing `base_url` to the Anthropic default and disables Anthropic-only features (web search, text editor tool, cache_control, anthropic-version header) automatically. UI labels always show "Claude".

### 3. Ask a Question

`Ctrl+Shift+P` → `Claudette: Ask Question` → type → Enter

## Features

- Chat with AI in multiple chat windows simultaneously
- Automatically include selected text as context
- Include files/folders in the chat context
- Choose between different AI models
- Configure custom system prompts
- Export/import conversations as JSON
- Multi-provider: any Anthropic-compatible API

## Commands

All commands via *Tools > Claudette* or the command palette.

| Command | Description |
|---------|-------------|
| **Ask Question** | Open input panel. <kbd>Enter</kbd> to submit. |
| **Ask Question In New Chat** | Always creates a new chat tab. |
| **Clear Chat History** | Clear conversation history to reduce token usage. |
| **Export / Import Chat History** | Save or load conversations as JSON. |
| **Add File to Chat** | Include files/folders in context (sidebar right-click). |
| **Add Current/Open Files** | Include open files in context. |
| **Refresh Included Files** | Re-read context files from disk. |
| **Show / Clear Included Files** | Manage context files. |
| **Switch Model** | Fetch and select from available models. |
| **Switch System Prompt** | Choose from configured system prompts. |
| **Switch API Key** | Switch between multiple configured API keys. |

## Settings Reference

| Setting | Default | Description |
|---------|---------|-------------|
| `api_key` | `""` | API key (string or `{keys: [...], active_key: N}`) |
| `base_url` | `"https://api.anthropic.com/v1/"` | API base URL. When changed, Anthropic-only features are auto-disabled |
| `model` | `"claude-sonnet-4-5"` | Model name |
| `max_tokens` | `8192` | Max output tokens per response |
| `temperature` | `"1.0"` | Temperature (0.0–1.0) |
| `system_messages` | `[...]` | List of system prompts |
| `pricing` | `{...}` | Pricing per 1M tokens (USD), matched by model name substring |
| `verify_ssl` | `true` | SSL certificate verification |
| `custom_headers` | `{}` | Extra HTTP headers for all requests |
| `web_search` | `false` | Web search (Anthropic only) |
| `text_editor_tool` | `false` | File editing tool (Anthropic only) |

## Installation

### Package Control

1. Install [Package Control](https://packagecontrol.io/installation)
2. `Ctrl+Shift+P` → `Package Control: Install Package` → `Claudette`

### Manual (.sublime-package)

Copy `Claudette.sublime-package` to:
- **Windows**: `%APPDATA%\Sublime Text\Installed Packages\`
- **macOS**: `~/Library/Application Support/Sublime Text/Installed Packages/`
- **Linux**: `~/.config/sublime-text/Installed Packages/`

Then restart Sublime Text.

### Development Mode

Clone into the Packages directory:
- **Windows**: `%APPDATA%\Sublime Text\Packages\Claudette\`
- **macOS**: `~/Library/Application Support/Sublime Text/Packages/Claudette/`
- **Linux**: `~/.config/sublime-text/Packages/Claudette/`

## Privacy & Legal

Content sent in chat is transmitted to the configured API provider's servers.
- **Anthropic**: [Privacy & Legal](https://support.anthropic.com/en/collections/4078534-privacy-legal)
- **DeepSeek**: [Privacy Policy](https://platform.deepseek.com/privacy)

## Credits

The package was primarily written by Claude AI itself.

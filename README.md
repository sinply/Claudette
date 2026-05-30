# Claudette – AI Assistant for Sublime Text

![Claudette Chat View](https://raw.githubusercontent.com/barryceelen/Claudette/main/screenshot.png "Ask AI")

A [Sublime Text](http://www.sublimetext.com) package that integrates AI chat into your editor. Supports both the **Anthropic Claude API** and the **DeepSeek API** (via DeepSeek's Anthropic-compatible endpoint at `https://api.deepseek.com/anthropic`).

Type "Ask Question" in the command palette or find the *Claudette > Ask Question* item in the *Tools* menu to ask a question. Any selected text in the current file will be sent along as context. An API key is required.

## Features

- Chat with AI in multiple chat windows simultaneously
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
        "model": "deepseek-chat",
        "base_url": "https://api.deepseek.com/anthropic/"
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

`Ctrl+Shift+P` → `Claudette: Ask Question` → type your question → Enter

The input prompt shows **"Ask DeepSeek:"** (or **"Ask Claude:"**), and the tab shows **"DeepSeek Chat"** (or **"Claude Chat"**).

> **Note:** Text Editor Tool and Web Search are Claude-specific features. They are automatically disabled when using DeepSeek.

## Commands

All commands are available via the *Tools > Claudette* menu or the command palette.

| Command | Description |
|---------|-------------|
| **Ask Question** | Open an input panel to ask a question. <kbd>Enter</kbd> to submit, <kbd>Shift+Enter</kbd> for line breaks. |
| **Ask Question In New Chat** | Same as above, but always creates a new chat tab. |
| **Clear Chat History** | Clear conversation history to reduce token usage. |
| **Export Chat History** | Save the current conversation to a JSON file. |
| **Import Chat History** | Load a conversation from a JSON file. |
| **Add File to Chat** | Include a file or folder in the chat context (right-click in sidebar). |
| **Add Current File to Chat** | Include the currently open file in the chat context. |
| **Remove Current File from Chat** | Remove the current file from the chat context. |
| **Add All Open Files to Chat** | Include all open files in the chat context. |
| **Refresh Included Files** | Re-read context files from disk. |
| **Show Included Files** | Manage the list of included context files. |
| **Clear Included Files** | Remove all context files. |
| **Switch Model** | Fetch and select from available models for the active provider. |
| **Switch System Prompt** | Choose from configured system prompts. |
| **Switch API Key** | Switch between multiple configured API keys. |

## Keyboard Shortcuts

No default keybindings are set. Add your own via *Preferences > Key Bindings*:

```jsonc
[
    {
        "keys": ["ctrl+k", "ctrl+c"],
        "command": "claudette_ask_question"
    }
]
```

## Settings Reference

| Setting | Default | Description |
|---------|---------|-------------|
| `api_provider` | `"anthropic"` | API provider: `"anthropic"` or `"deepseek"` |
| `api_key` | `""` | Anthropic API key |
| `base_url` | `"https://api.anthropic.com/v1/"` | Anthropic API base URL |
| `model` | `"claude-sonnet-4-5"` | Claude model name |
| `deepseek.api_key` | `""` | DeepSeek API key |
| `deepseek.base_url` | `"https://api.deepseek.com/anthropic/"` | DeepSeek Anthropic-compatible endpoint |
| `deepseek.model` | `"deepseek-chat"` | DeepSeek model (`deepseek-chat` or `deepseek-reasoner`) |
| `deepseek.pricing` | `{...}` | DeepSeek pricing per 1M tokens (USD) |
| `max_tokens` | `8192` | Maximum output tokens per response |
| `temperature` | `"1.0"` | Model temperature (0.0–1.0) |
| `system_messages` | `[...]` | List of system prompts |
| `pricing` | `{...}` | Anthropic pricing per 1M tokens (USD) |
| `web_search` | `false` | Enable web search (Anthropic only) |
| `text_editor_tool` | `false` | Enable file editing tool (Anthropic only) |

## Installation

### Method 1: Package Control

1. Install [Package Control](https://packagecontrol.io/installation)
2. `Ctrl+Shift+P` → `Package Control: Install Package` → search `Claudette`

### Method 2: Manual (.sublime-package)

1. Download `Claudette.sublime-package`
2. Copy to:
   - **Windows**: `%APPDATA%\Sublime Text\Installed Packages\`
   - **macOS**: `~/Library/Application Support/Sublime Text/Installed Packages/`
   - **Linux**: `~/.config/sublime-text/Installed Packages/`
3. Restart Sublime Text

### Method 3: Development Mode

Clone the repo directly into the Packages directory:

- **Windows**: `%APPDATA%\Sublime Text\Packages\Claudette\`
- **macOS**: `~/Library/Application Support/Sublime Text/Packages/Claudette/`
- **Linux**: `~/.config/sublime-text/Packages/Claudette/`

## Privacy & Legal

Content sent in chat is transmitted to the active provider's servers.

- **Anthropic**: [Privacy & Legal](https://support.anthropic.com/en/collections/4078534-privacy-legal)
- **DeepSeek**: [Privacy Policy](https://platform.deepseek.com/privacy)

## Credits

The package was primarily written by Claude AI itself.

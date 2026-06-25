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
    "base_url": "https://api.deepseek.com/anthropic/",
    "models": ["deepseek-chat", "deepseek-reasoner"]
}
```

**Any other Anthropic-compatible API:**
```jsonc
{
    "api_key": "your-key",
    "model": "your-model",
    "base_url": "https://your-endpoint/v1/",
    "models": ["your-model", "another-model"]
}
```

That's it — just change `base_url`, `model`, and `api_key`. The plugin auto-detects third-party APIs by comparing `base_url` to the Anthropic default and disables Anthropic-only features (text editor tool, cache_control, anthropic-version header) automatically. Client-side web search and web fetch work with ALL providers. The optional `models` list powers the **Switch Model** command for providers that don't expose a `/models` endpoint (DeepSeek, OpenRouter, etc.). UI labels always show "Claude".

### 3. Ask a Question

`Ctrl+Shift+P` → `Claudette: Ask Question` → type → Enter

## Features

- Chat with AI in multiple chat windows simultaneously
- **Web search** — auto-searches before every question (configurable), works with ALL providers
- **Web fetch** — AI can read content from any URL (works with ALL providers, even with auto-search on)
- **Client-side tools** — `web_fetch` and `client_web_search` execute locally, so they work with every Anthropic-compatible provider
- Automatically include selected text as context
- Include files/folders in the chat context
- Choose between different AI models
- Configure custom system prompts
- Export/import conversations as JSON
- Multi-provider: any Anthropic-compatible API
- Per-key `base_url` / `model` overrides (use Claude and DeepSeek side by side)

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
| `models` | `[]` | Optional static model list for Switch Model (used when `/models` endpoint is unavailable, e.g. DeepSeek) |
| `max_tokens` | `8192` | Max output tokens per response |
| `request_timeout` | `180` | Per-request timeout in seconds (reasoning models can be slow) |
| `temperature` | `"1.0"` | Sampling temperature. Anthropic caps at 1.0; other providers allow up to 2.0. Out-of-range values are clamped |
| `system_messages` | `[...]` | List of system prompts |
| `pricing` | `{...}` | Pricing per 1M tokens (USD), matched by model name substring |
| `verify_ssl` | `true` | SSL certificate verification |
| `custom_headers` | `{}` | Extra HTTP headers for all requests |
| `force_web_search` | `true` | Auto-search before every question (all providers) |
| `enable_web_fetch` | `true` | AI can fetch and read URL content (all providers) |
| `enable_client_web_search` | `true` | AI-controlled web search when `force_web_search` is off |
| `web_search_backend` | `"duckduckgo"` | Search backend: `"duckduckgo"` or `"searxng"` |
| `searxng_instance_url` | `"https://searx.be"` | SearXNG instance URL (for searxng backend) |
| `web_search` | `false` | Server-side web search (Anthropic only) |
| `text_editor_tool` | `false` | File editing tool (Anthropic only) |

## Web Search

`force_web_search` (on by default) searches the web with your question before each request and feeds the results to the AI as context, so answers always reflect current information. If the search backend is unreachable, the plugin shows a status hint and continues without blocking.

### Search backends

| Backend | Notes |
|---------|-------|
| **DuckDuckGo** (default) | Free, no API key. Scrapes the HTML results page first, then falls back to the Instant Answer API. |
| **SearXNG** | Open-source meta-search engine; configure your own instance URL. |

### Network notes

- If DuckDuckGo is unreachable (common in mainland China), switch to SearXNG with a reachable instance:
  ```jsonc
  {
      "web_search_backend": "searxng",
      "searxng_instance_url": "https://your-instance.example"
  }
  ```
- Or set `force_web_search` to `false` to disable auto-search and let the AI decide when to search (tool mode).
- `web_fetch` fetches URLs directly, so it works whenever the target site is reachable.

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

### Rebuilding the `.sublime-package`

After editing source files, rebuild the package with:

```bash
python build_package.py
```

This strips BOM from `.py`/`.pyi` files (Sublime's zip importer cannot handle BOM) and zips the source into `Claudette.sublime-package`. Copy the result to your `Installed Packages/` directory and restart Sublime Text.

### Running the standalone test suite

A standalone test (`test_standalone.py`) exercises the API layer against your configured provider without launching Sublime Text. It mocks the `sublime`/`sublime_plugin` modules and runs real requests:

```bash
python test_standalone.py
```

It verifies temperature clamping, provider detection, model fetching, the `web_fetch` tool loop, the streaming response path, and the search backends. Configure your provider in `User/Claudette.sublime-settings` first.

## Privacy & Legal

Content sent in chat is transmitted to the configured API provider's servers.
- **Anthropic**: [Privacy & Legal](https://support.anthropic.com/en/collections/4078534-privacy-legal)
- **DeepSeek**: [Privacy Policy](https://platform.deepseek.com/privacy)

## Credits

The package was primarily written by Claude AI itself.

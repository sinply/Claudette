# Claudette – AI Assistant for Sublime Text

A [Sublime Text](http://www.sublimetext.com) package that integrates AI chat into your editor. Supports the **Anthropic Claude API** natively, and any **third-party Anthropic-compatible API** (DeepSeek, OpenRouter, etc.) via a simple config change.

---

## Quick Start

### 1. Get an API Key

- **Claude**: [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
- **DeepSeek**: [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)

### 2. Configure

*Preferences → Package Settings → Claudette → Settings*

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

That's it — just change `base_url`, `model`, and `api_key`. The plugin auto-detects third-party APIs by comparing `base_url` to the Anthropic default and disables Anthropic-only features (text editor tool, cache_control, `anthropic-version` header) automatically. Client-side web search and web fetch work with **all** providers. The optional `models` list powers the **Switch Model** command for providers that don't expose a `/models` endpoint (DeepSeek, OpenRouter, etc.). UI labels always show "Claude".

### 3. Ask a Question

`Ctrl+Shift+P` → `Claudette: Ask Question` → type → `Enter`

---

## Usage Guide

### Opening the chat view

There are two ways to start a conversation:

- **Claudette: Ask Question** — Opens an input panel. When you submit, the plugin reuses the *current chat tab* for the active window, or creates one if none exists. Use this for normal back-and-forth.
- **Claudette: Ask Question In New Chat View** — Always creates a fresh chat tab and makes it the current one. Use this when you want a clean conversation that doesn't carry over previous context.

Each Sublime Text window tracks its own "current chat" tab. If you have multiple chat tabs open in a window, focusing one marks it as the current chat — the next **Ask Question** goes there. You can keep separate chats in separate windows, or several tabs in one window.

The chat view is a read-only Markdown view named `Claude Chat`. It uses the Markdown syntax highlighter, so AI responses (headings, lists, code blocks) render with proper highlighting.

### Asking a question

1. Run **Claudette: Ask Question** (via command palette, or the *Tools → Claudette* menu).
2. An input panel appears at the bottom of the window with the prompt `Ask Claude:`.
3. Type your question and press `Enter` to submit. (`Esc` cancels the input panel without sending.)
4. The question is appended to the chat view, the view scrolls smoothly to it, and the request starts.

**With selected code:** If you have a selection in any editor view when you run **Ask Question**, the selected text is automatically captured *before* the input panel opens and included as context. The chat shows it under a `**Selected Code**` heading, and the underlying message to the API combines your question with the code.

> On some systems (notably ST4 on Windows), pressing `Enter` in the input panel can insert a newline instead of submitting. The plugin detects a trailing newline and treats it as submit, so `Enter` always sends.

### Keyboard shortcuts (inside a chat view)

| Key | Action |
|-----|--------|
| `Enter` | Submit a new question (opens the input panel, then sends) |
| `Esc` | Stop the in-flight request for this chat tab |

These bindings only apply while a chat view is focused (`claudette_is_chat_view` setting is `true`). They are defined in `Default.sublime-keymap` and can be overridden in your user keymap.

### Following the response

While the AI is thinking, an inline status phantom shows a random "working" verb (e.g. `ℹ️ Pondering ✻`) with an animated spinner. The response streams in token-by-token. When streaming finishes:

- The status phantom is cleared.
- Each fenced code block gets a **Copy** button rendered just below it. Click it to copy that block's code to the clipboard.
- If a code block was truncated mid-stream (e.g. you stopped the request, or `max_tokens` was hit), the plugin auto-appends a closing fence so the Markdown highlighter doesn't break.

**Cost / token display:** If `chat.show_cost` is `true` (default), a status line appears after each response:

```
⚡️ Tokens: 1,234 in, 567 out. Cost: $0.0023 ($0.0156 session)
```

The per-response cost and the running session total are both shown. Pricing is read from the `pricing` setting (see [Configuration Guide](#configuration-guide)).

### Stopping a request

Press `Esc` while focused on the chat view, or run **Claudette: Stop Request**. This cancels the in-flight HTTP request for that chat tab only — other tabs keep running. The partial response already streamed stays in the view and is added to the conversation history, so you can continue the conversation from there.

### Including files & folders as context

You can attach file contents to the conversation so the AI can see them:

| Action | How |
|--------|-----|
| **Add current file** | *Tools → Claudette → Chat Context → Add Current File To Chat*, or right-click in the editor → *Claudette → Add File to Chat* |
| **Remove current file** | *Tools → Claudette → Chat Context → Remove Current File From Chat*, or right-click → *Claudette → Remove from Chat* |
| **Add files/folders from sidebar** | Right-click a file or folder in the sidebar → *Claudette → Claudette* (uses `claudette_context_add_files`). Folders are scanned recursively; non-text files are skipped. |
| **Add all open files** | *Tools → Claudette → Chat Context → Add All Open Files To Chat* |
| **Refresh** | *Tools → Claudette → Chat Context → Refresh Included Files* — re-reads all included files from disk in case they changed |
| **List / clear** | *Show Included Files* opens a panel listing everything; *Clear Included Files* removes all |

Files are read once when added (or on refresh) and their contents are prepended to the system message on each request. They are *not* re-read on every turn automatically — use **Refresh Included Files** after editing them.

### Switching models, system prompts, and API keys

- **Switch Model** — Fetches the model list from the provider's `/models` endpoint and shows a quick panel. If the endpoint is unavailable (DeepSeek, OpenRouter, and most non-Anthropic providers return 404 or empty), the plugin falls back to the `models` setting. Selecting a model updates the active `model` immediately — the next request uses it.
- **Switch System Prompt** — Cycles through the `system_messages` list. The active one is sent as the system message on the next request. If the active entry is an empty string, no system message is sent at all.
- **Switch API Key** — Only meaningful if `api_key` is configured as an object with multiple keys. Shows a quick panel of key names; selecting one makes it active. This is how you flip between, say, a Claude key and a DeepSeek key without editing settings — **especially when each key carries its own `base_url`/`model` override** (see [Multi-provider side-by-side](#multi-provider-side-by-side)).

### Chat history

- **Clear Chat History** — Wipes the conversation history for the current chat tab (the visible text is cleared too). Use this to reduce token usage without opening a new tab.
- **Export Chat History** — Saves the current conversation (as a JSON file) to disk via a file dialog. Useful for keeping a record or sharing.
- **Import Chat History** — Loads a previously exported JSON file into the current chat tab. The conversation continues from the imported state.

---

## Features

- Chat with AI in multiple chat windows simultaneously
- **Web search** — auto-searches before every question (configurable), works with all providers
- **Web fetch** — AI can read content from any URL (works with all providers, even with auto-search on)
- **Client-side tools** — `web_fetch` and `client_web_search` execute locally, so they work with every Anthropic-compatible provider
- Automatically include selected text as context
- Include files/folders in the chat context
- Choose between different AI models
- Configure custom system prompts
- Export/import conversations as JSON
- Multi-provider: any Anthropic-compatible API
- Per-key `base_url` / `model` overrides (use Claude and DeepSeek side by side)

## Commands

All commands via *Tools → Claudette* or the command palette (`Ctrl+Shift+P`).

| Command | Description |
|---------|-------------|
| **Ask Question** | Open input panel. <kbd>Enter</kbd> to submit. Reuses current chat tab. |
| **Ask Question In New Chat View** | Always creates a new chat tab. |
| **Stop Request** | Cancel the in-flight request for the current chat tab. |
| **Clear Chat History** | Clear conversation history to reduce token usage. |
| **Export / Import Chat History** | Save or load conversations as JSON. |
| **Add File to Chat** | Include files/folders in context (sidebar right-click). |
| **Add Current/Open Files** | Include open files in context. |
| **Refresh Included Files** | Re-read context files from disk. |
| **Show / Clear Included Files** | Manage context files. |
| **Switch Model** | Fetch and select from available models (or use `models` list). |
| **Switch System Prompt** | Choose from configured system prompts. |
| **Switch API Key** | Switch between multiple configured API keys. |

---

## Configuration Guide

Open settings via *Preferences → Package Settings → Claudette → Settings*. This opens a split view: the package default on the left (read-only) and your user settings on the right. **Only edit the right side.** Settings files are JSONC — `//` comments and trailing commas are allowed.

Every setting below lives in `Claudette.sublime-settings`. Changes are picked up on the next request — no restart needed.

### Core settings

#### `api_key` *(string or object, default `""`)*

A single key, or a multi-key configuration. For one provider, just use a string:

```jsonc
{ "api_key": "sk-ant-..." }
```

For multiple keys (e.g. Claude + DeepSeek side by side), use the object form. Each entry can carry its own `base_url` and `model`, overriding the top-level settings — this is how one Sublime window can talk to two providers and switch between them with **Switch API Key**:

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

`active_key` is the zero-based index of the currently active key. **Switch API Key** updates it. If a key entry omits `base_url`/`model`, the top-level values are used.

#### `base_url` *(string, default `"https://api.anthropic.com/v1/"`)*

The API endpoint. A trailing `/` is added automatically if missing. **Provider detection** compares this (after trimming the trailing slash) to the Anthropic default — if they differ, Anthropic-only features (`text_editor_tool`, `cache_control`, the `anthropic-version` header, server-side `web_search`) are disabled, and the temperature ceiling is raised from 1.0 to 2.0.

#### `model` *(string, default `"claude-sonnet-4-5"`)*

The model id sent in requests. Use **Switch Model** to change it without editing settings.

#### `models` *(list, default `[]`)*

Static model list for **Switch Model** when the provider has no `/models` endpoint (DeepSeek, OpenRouter, etc.). Example:

```jsonc
"models": ["deepseek-chat", "deepseek-reasoner"]
```

When non-empty, **Switch Model** shows this list instead of querying the API.

#### `max_tokens` *(int, default `8192`)*

Maximum output tokens per response. **Must not exceed the model's output limit** — the API returns a 400 error if it does. Common limits:

| Model family | Output limit |
|--------------|--------------|
| Claude Opus 4.6 | 128,000 |
| Claude Sonnet 4.5 / Haiku 4.5 | 64,000 |
| Claude Sonnet 4 / Opus 4 | 8,192 |
| DeepSeek chat / reasoner | 8,192 |

#### `request_timeout` *(int, default `180`)*

Per-request timeout in seconds. Non-streaming requests with tool loops (web fetch, client search, text editor) can take a while on reasoning models (e.g. DeepSeek reasoner thinks before responding). Increase this if you hit timeouts. Streaming requests are also subject to it.

#### `temperature` *(string, default `"1.0"`)*

Sampling temperature, clamped per provider: Anthropic `0.0`–`1.0`, others `0.0`–`2.0`. Out-of-range values are clamped to the nearest bound; non-numeric values fall back to `1.0`. Stored as a string because Sublime settings parse unquoted numbers with reduced precision.

#### `system_messages` *(list, default: 3 prompts)*

A list of system prompts. **Switch System Prompt** cycles through these. Each entry is sent as the system message at the start of the next request. An empty string `""` means "send no system message."

```jsonc
"system_messages": [
    "You are a helpful AI assistant focused on programming help.",
    "You are a helpful AI assistant focused on writing and documentation.",
    ""
]
```

`default_system_message_index` (int, default `0`) picks the active one at startup.

#### `pricing` *(object, default: Claude tiers + DeepSeek entries)*

Per-1M-token prices in USD, used for the cost line after each response. Keys are matched as **case-insensitive substrings** of the model name — the first match wins. Add an entry for any model you use:

```jsonc
"pricing": {
    "haiku":  { "input": 1,    "output": 5,    "cache_write": 1.25, "cache_read": 0.1  },
    "sonnet": { "input": 3,    "output": 15,   "cache_write": 3.75, "cache_read": 0.3  },
    "opus":   { "input": 5,    "output": 25,   "cache_write": 6.25, "cache_read": 0.5  },
    "deepseek-chat":    { "input": 0.27, "output": 1.10 },
    "deepseek-reasoner":{ "input": 0.55, "output": 2.19 }
}
```

`cache_write`/`cache_read` only apply to Anthropic (prompt caching). If a model has no matching entry, the cost line shows `$0.0000`.

### Network settings

#### `verify_ssl` *(bool, default `true`)*

SSL certificate verification. Set to `false` only for trusted development servers with self-signed certs. **Disabling it reduces security** — never do this for production keys.

#### `custom_headers` *(object, default `{}`)*

Extra HTTP headers added to every API request. Useful for proxy auth, custom `anthropic-version` overrides, or provider-specific gateways:

```jsonc
"custom_headers": {
    "X-Custom-Auth": "bearer xyz",
    "Anthropic-Beta": "interleaved-thinking-2025-05-14"
}
```

### Web access settings

There are three **independent** client-side web toggles, plus two Anthropic-only server-side tools:

| Setting | Default | Scope | Behavior |
|---------|---------|-------|---------|
| `force_web_search` | `true` | All providers | Auto-search the web *before* every question and feed results as context. Uses streaming mode. |
| `enable_web_fetch` | `true` | All providers | Give the AI a `web_fetch` tool to read URLs it wants to follow up on. |
| `enable_client_web_search` | `true` | All providers | Give the AI a `client_web_search` tool to search on its own. Only active when `force_web_search` is `false`. |
| `web_search` | `false` | **Anthropic only** | Server-side web search tool (billed $10 / 1,000 searches). Auto-disabled for non-Anthropic. |
| `text_editor_tool` | `false` | **Anthropic only** | Server-side file edit tool. Auto-disabled for non-Anthropic. |

**How they interact:**

- If `force_web_search` is on (default), every question is pre-searched. `enable_web_fetch` still works alongside it — the AI can fetch URLs from the search results.
- If you turn `force_web_search` off, set `enable_client_web_search` to `true` so the AI can still search when it needs to.
- To go fully offline, set all three client toggles to `false`.

#### `web_search_backend` *(string, default `"duckduckgo"`)*

Which backend `force_web_search` and `client_web_search` use:

- `"duckduckgo"` — Free, no API key. Scrapes the HTML results page first, falls back to the Instant Answer API.
- `"searxng"` — Open-source meta-search. Requires `searxng_instance_url`.

#### `searxng_instance_url` *(string, default `"https://searx.be"`)*

SearXNG instance URL. Only used when `web_search_backend` is `"searxng"`. Public instances: [searx.be](https://searx.be), [searx.work](https://searx.work), or self-host your own.

### Anthropic-only tool settings

These only take effect when `base_url` points at Anthropic. They are ignored (auto-disabled) for third-party providers.

| Setting | Default | Description |
|---------|---------|-------------|
| `web_search_max_uses` | `5` | Max server-side searches per request (1–20). |
| `web_search_allowed_domains` | `[]` | Only include results from these domains. |
| `web_search_blocked_domains` | `[]` | Exclude results from these domains. |
| `web_search_user_location` | *(unset)* | Localize results. `{ "type": "approximate", "city": "...", "region": "...", "country": "...", "timezone": "..." }` |
| `text_editor_tool_roots` | `[]` | Extra allowed roots for file operations (paths must be under these or project folders). |
| `text_editor_tool_max_characters` | *(unset)* | Max chars when viewing a file (0 = no limit). |

### Chat view settings

```jsonc
"chat": {
    "line_numbers": false,
    "rulers": false,
    "set_scratch": true,
    "show_cost": true
}
```

| Key | Default | Description |
|-----|---------|-------------|
| `line_numbers` | `false` | Show line numbers in chat views. |
| `rulers` | `false` | Show rulers in chat views. |
| `set_scratch` | `true` | Mark chat views as scratch — closing them won't prompt to save. |
| `show_cost` | `true` | Show the tokens/cost line after each response. |

---

## Common Scenarios

### Minimal Claude setup

```jsonc
{
    "api_key": "sk-ant-your-key",
    "model": "claude-sonnet-4-5"
}
```

Everything else uses sensible defaults.

### DeepSeek (mainland China friendly)

DeepSeek's `/anthropic/` endpoint is Anthropic-compatible. The `/models` endpoint returns 404, so set the `models` list manually for **Switch Model**:

```jsonc
{
    "api_key": "sk-your-key",
    "base_url": "https://api.deepseek.com/anthropic/",
    "model": "deepseek-chat",
    "models": ["deepseek-chat", "deepseek-reasoner"],
    "temperature": "1.5"
}
```

If DuckDuckGo (the default search backend) is unreachable from your network, switch to a reachable SearXNG instance or disable auto-search:

```jsonc
{
    "web_search_backend": "searxng",
    "searxng_instance_url": "https://your-reachable-instance.example"
}
```

…or turn auto-search off and let the AI decide:

```jsonc
{ "force_web_search": false, "enable_client_web_search": true }
```

### Multi-provider side-by-side

Define both keys with per-key `base_url`/`model` overrides, then flip between them with **Switch API Key**:

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

The `text_editor_tool` and server-side `web_search` auto-disable when the active key points at DeepSeek, and re-enable when you switch back to Claude — no manual toggling.

### Self-hosted dev server

For a local proxy with a self-signed cert:

```jsonc
{
    "api_key": "dev-key",
    "base_url": "https://localhost:8443/v1/",
    "verify_ssl": false,
    "custom_headers": { "X-Dev-Origin": "sublime" }
}
```

### Fully offline (no web access)

```jsonc
{
    "force_web_search": false,
    "enable_web_fetch": false,
    "enable_client_web_search": false
}
```

The AI will only answer from its training data and the files you include as context.

### Disable web auto-search but keep on-demand fetch

```jsonc
{
    "force_web_search": false,
    "enable_web_fetch": true,
    "enable_client_web_search": true
}
```

The AI decides when to search or fetch, instead of auto-searching every question.

---

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

---

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

---

## Privacy & Legal

Content sent in chat is transmitted to the configured API provider's servers.
- **Anthropic**: [Privacy & Legal](https://support.anthropic.com/en/collections/4078534-privacy-legal)
- **DeepSeek**: [Privacy Policy](https://platform.deepseek.com/privacy)

## Credits

The package was primarily written by Claude AI itself.

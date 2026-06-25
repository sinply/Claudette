"""Standalone end-to-end test for Claudette's API layer.

Mocks the `sublime` / `sublime_plugin` modules so we can import the plugin
without Sublime Text, then exercises the real API against the configured
provider (DeepSeek or Anthropic). Prints a pass/fail summary.

Run: python test_standalone.py
"""
import json
import os
import re
import sys
import types

REPO = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(REPO)
# Drop CWD (REPO) from sys.path so `Claudette.py` doesn't shadow the
# `Claudette/` package directory when we import submodules.
sys.path[:] = [p for p in sys.path if os.path.abspath(p or ".") != REPO]
sys.path.insert(0, PARENT)

# --- Mock the sublime / sublime_plugin modules ------------------------------

sublime = types.ModuleType("sublime")
sublime.PLATFORM = "windows"


class _Settings(dict):
    def get(self, key, default=None):
        return super().get(key, default)

    def set(self, key, value):
        self[key] = value


_SETTINGS = _Settings()
sublime._SETTINGS = _SETTINGS

sublime.load_settings = lambda name: _SETTINGS
sublime.save_settings = lambda name: None
sublime.error_message = lambda msg: print("[SUBLIME ERROR]", msg)
sublime.status_message = lambda msg: None
sublime.active_window = lambda: None
sublime.windows = lambda: []


def _fire(cb, delay=0, **kw):
    # In Sublime, set_timeout defers to the UI thread. For tests, run
    # synchronously so callbacks (which drive chunk_callback / on_complete)
    # actually execute.
    try:
        cb()
    except Exception as e:
        print("[set_timeout callback error] {0}".format(e))


sublime.set_timeout = _fire
# Spinner uses set_timeout_async to re-arm itself; a no-op keeps tests quiet.
sublime.set_timeout_async = lambda cb, delay=0, **kw: None
sublime.set_clipboard = lambda text: None
sublime.cache_path = lambda: os.path.join(REPO, ".cache")
sublime.platform = lambda: "windows"


class _Region:
    def __init__(self, a, b=None):
        self.a = a
        self.b = b if b is not None else a


sublime.Region = _Region
sublime.LAYOUT_INLINE = 0
sublime.LAYOUT_BLOCK = 1
sublime.KEEP_OPEN_ON_FOCUS_LOST = 0


class _Phantom:
    def __init__(self, region, content, layout, on_navigate):
        self.region = region
        self.content = content
        self.layout = layout
        self.on_navigate = on_navigate


class _PhantomSet:
    def __init__(self, view, key=""):
        self.phantoms = []

    def update(self, phantoms):
        self.phantoms = list(phantoms)


sublime.Phantom = _Phantom
sublime.PhantomSet = _PhantomSet
sublime.message_dialog = lambda msg: print("[DIALOG]", msg)
sublime.ok_cancel_dialog = lambda msg, ok="": True
sublime.open_dialog = lambda cb, *a, **kw: None
sublime.save_dialog = lambda cb, *a, **kw: None
sublime.run_command = lambda *a, **kw: None
sys.modules["sublime"] = sublime

sublime_plugin = types.ModuleType("sublime_plugin")


class _WindowCommand:
    def __init__(self, window=None):
        self.window = window


class _TextCommand:
    def __init__(self, view=None):
        self.view = view


class _EventListener:
    pass


class _ViewEventListener:
    pass


sublime_plugin.WindowCommand = _WindowCommand
sublime_plugin.TextCommand = _TextCommand
sublime_plugin.EventListener = _EventListener
sublime_plugin.ViewEventListener = _ViewEventListener
sys.modules["sublime_plugin"] = sublime_plugin

# --- Load user settings from the deployed User settings file ----------------
USER_SETTINGS_PATH = os.path.join(
    os.environ.get("APPDATA", ""),
    "Sublime Text",
    "Packages",
    "User",
    "Claudette.sublime-settings",
)
if os.path.isfile(USER_SETTINGS_PATH):
    with open(USER_SETTINGS_PATH, "r", encoding="utf-8") as f:
        raw_user = f.read()
    # Sublime tolerates trailing commas + // comments; json does not.
    raw_user = re.sub(r"^\s*//.*$", "", raw_user, flags=re.MULTILINE)
    raw_user = re.sub(r",\s*([}\]])", r"\1", raw_user)
    user_settings = json.loads(raw_user)
    _SETTINGS.update(user_settings)
    print("Loaded user settings from {0}".format(USER_SETTINGS_PATH))
    print(
        "  base_url={0} model={1} api_key={2}...".format(
            _SETTINGS.get("base_url"),
            _SETTINGS.get("model"),
            (_SETTINGS.get("api_key") or "")[:8],
        )
    )

# Apply package defaults too (so request_timeout etc. have defaults)
DEFAULTS_PATH = os.path.join(REPO, "Claudette.sublime-settings")
with open(DEFAULTS_PATH, "r", encoding="utf-8") as f:
    raw = f.read()
cleaned = re.sub(r"^\s*//.*$", "", raw, flags=re.MULTILINE)
cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)
defaults = json.loads(cleaned)
for k, v in defaults.items():
    if k not in _SETTINGS:
        _SETTINGS[k] = v

# --- Now import the plugin's API and run tests ------------------------------

from Claudette.api.api import ClaudetteClaudeAPI
from Claudette.api.provider import is_anthropic
from Claudette.tools.web_fetch import run_web_fetch
from Claudette.tools.web_search_client import run_web_search

api = ClaudetteClaudeAPI()
print(
    "\nProvider: is_anthropic={0} base_url={1} model={2} timeout={3}s".format(
        api.is_anthropic, api.base_url, api.model, api.request_timeout
    )
)

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("  [PASS] {0}".format(name))
    else:
        FAIL += 1
        print("  [FAIL] {0} {1}".format(name, detail))


# Test 1: temperature clamping respects provider
print("\n--- Test 1: temperature clamping ---")
check(
    "Anthropic temp 1.5 -> 1.0",
    api.get_valid_temperature(1.5, True) == 1.0,
    "got {0}".format(api.get_valid_temperature(1.5, True)),
)
check(
    "Non-Anthropic temp 1.5 -> 1.5",
    api.get_valid_temperature(1.5, False) == 1.5,
    "got {0}".format(api.get_valid_temperature(1.5, False)),
)
check(
    "Non-Anthropic temp 2.5 -> 2.0",
    api.get_valid_temperature(2.5, False) == 2.0,
    "got {0}".format(api.get_valid_temperature(2.5, False)),
)
check(
    "Negative temp -> 0.0",
    api.get_valid_temperature(-0.5, False) == 0.0,
)
check(
    "Invalid temp -> 1.0",
    api.get_valid_temperature("abc", False) == 1.0,
)
check(
    "Provider-aware for this config",
    api.get_valid_temperature(1.5, api.is_anthropic) == (1.0 if api.is_anthropic else 1.5),
)

# Test 2: provider detection
print("\n--- Test 2: provider detection ---")
check("Anthropic URL detected", is_anthropic("https://api.anthropic.com/v1/") is True)
check(
    "DeepSeek URL detected as non-Anthropic",
    is_anthropic("https://api.deepseek.com/anthropic/") is False,
)
check(
    "DeepSeek URL (no trailing slash) non-Anthropic",
    is_anthropic("https://api.deepseek.com/anthropic") is False,
)

# Test 3: fetch_models returns something (or falls back to `models` setting)
print("\n--- Test 3: fetch_models ---")
models = api.fetch_models()
check(
    "fetch_models returned a list",
    isinstance(models, list),
    "got {0}".format(type(models).__name__),
)
if models:
    print("    Available models: {0}".format(models[:5]))
else:
    print("    (empty — set \"models\" in settings to enable Switch Model)")

# Test 4: non-streaming request with web_fetch tool (tool loop)
print("\n--- Test 4: tool loop with web_fetch (non-streaming) ---")

collected = {"chunks": [], "done": False, "usage": None, "cancelled": False}


def chunk_cb(chunk, is_done=False, usage_info=None, was_cancelled=False, **kw):
    if chunk:
        collected["chunks"].append(chunk)
    if is_done:
        collected["done"] = True
        collected["usage"] = usage_info
        collected["cancelled"] = was_cancelled


class _FakeChatView:
    def __init__(self):
        self.tool_status = None

    def set_tool_status(self, msg):
        self.tool_status = msg

    def clear_tool_status(self):
        self.tool_status = None

    def settings(self):
        return _SETTINGS


fake_chat_view = _FakeChatView()

messages = [{"role": "user", "content": "Use the web_fetch tool to read https://example.com and tell me the page title in 5 words or less."}]

try:
    api.run_with_client_tools_loop(
        chunk_callback=chunk_cb,
        messages=messages,
        chat_view=fake_chat_view,
    )
    full_text = "".join(collected["chunks"])
    check("Tool loop completed", collected["done"], "not done")
    check(
        "Got non-empty response",
        bool(full_text.strip()),
        "chunks={0}".format(collected["chunks"][:3]),
    )
    check(
        "Usage info present",
        collected["usage"] is not None,
    )
    print("    Response: {0}".format(full_text[:200]))
except Exception as e:
    check("Tool loop ran without exception", False, str(e))
    import traceback

    traceback.print_exc()

# Test 5: web_search_client backends
print("\n--- Test 5: web_search_client backends ---")
result = run_web_search("test query", backend="duckduckgo", timeout=10)
check(
    "DuckDuckGo returns a string",
    isinstance(result, str),
    "got {0}".format(type(result).__name__),
)
if result.startswith("Error"):
    print("    (DuckDuckGo unreachable from this network — OK in CN)")
elif "No results" in result:
    print("    (No results — backend reachable but query had none)")
else:
    print("    DuckDuckGo OK: {0} chars".format(len(result)))

result = run_web_search(
    "test query", backend="searxng", searxng_instance="https://searx.be", timeout=10
)
check(
    "SearXNG returns a string",
    isinstance(result, str),
    "got {0}".format(type(result).__name__),
)

# Test 6: web_fetch
print("\n--- Test 6: web_fetch ---")
content = run_web_fetch("https://example.com", timeout=10)
check(
    "web_fetch example.com returns text",
    isinstance(content, str) and "Example" in content,
    "got: {0}".format(content[:80]),
)

# Test 7: streaming response (single turn, no tools)
print("\n--- Test 7: streaming response ---")
collected2 = {"chunks": [], "done": False, "usage": None}


def chunk_cb2(chunk, is_done=False, usage_info=None, **kw):
    if chunk:
        collected2["chunks"].append(chunk)
    if is_done:
        collected2["done"] = True
        collected2["usage"] = usage_info


try:
    api.stream_response(
        chunk_callback=chunk_cb2,
        messages=[{"role": "user", "content": "Reply with exactly: pong"}],
        chat_view=None,
    )
    text = "".join(collected2["chunks"])
    check("Streaming completed", collected2["done"])
    check(
        "Streaming produced text",
        bool(text.strip()),
        "chunks={0}".format(collected2["chunks"][:3]),
    )
    print("    Streamed: {0}".format(text[:200]))
except Exception as e:
    check("Streaming ran without exception", False, str(e))
    import traceback

    traceback.print_exc()

print("\n=== RESULTS: {0} passed, {1} failed ===".format(PASS, FAIL))
sys.exit(1 if FAIL else 0)

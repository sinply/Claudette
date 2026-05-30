"""Provider detection and configuration for multi-provider support."""

from ..constants import (
    DEFAULT_BASE_URL,
    DEFAULT_DEEPSEEK_BASE_URL,
    DEFAULT_DEEPSEEK_MODEL,
    DEFAULT_MODEL,
)


def get_provider(settings):
    """Return the active API provider: 'anthropic' or 'deepseek'."""
    return settings.get("api_provider", "anthropic")


def get_effective_settings(settings):
    """Return (provider, base_url, model, api_key) for the active provider."""
    provider = get_provider(settings)
    if provider == "deepseek":
        ds = settings.get("deepseek", {})
        base_url = ds.get("base_url") or DEFAULT_DEEPSEEK_BASE_URL
        model = ds.get("model") or DEFAULT_DEEPSEEK_MODEL
        api_key = _extract_key_value(ds.get("api_key", ""))
        pricing = ds.get("pricing", {})
    else:
        base_url = settings.get("base_url", DEFAULT_BASE_URL)
        model = settings.get("model", DEFAULT_MODEL)
        api_key = _extract_key_value(settings.get("api_key"))
        pricing = settings.get("pricing")
    return provider, base_url, model, api_key, pricing


def _extract_key_value(api_key_config):
    """Extract the actual key string from a single key or named-key dict."""
    if isinstance(api_key_config, str) and api_key_config.strip():
        return api_key_config
    if isinstance(api_key_config, dict):
        keys = api_key_config.get("keys", [])
        active = api_key_config.get("active_key", 0)
        if isinstance(active, int) and 0 <= active < len(keys):
            entry = keys[active]
            if isinstance(entry, dict):
                return entry.get("key", "")
        for entry in keys:
            if isinstance(entry, dict) and entry.get("key"):
                return entry["key"]
    return ""


def provider_label(provider):
    """Human-readable provider name for UI."""
    return "DeepSeek" if provider == "deepseek" else "Claude"

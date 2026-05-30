"""Provider detection — controls Anthropic-specific features via base_url."""

from ..constants import DEFAULT_BASE_URL


def is_anthropic(base_url):
    """Return True if base_url points to the native Anthropic API."""
    if not base_url:
        return True
    return base_url.rstrip("/") == DEFAULT_BASE_URL.rstrip("/")

"""Provider detection — controls UI labels and Anthropic-specific features."""


def get_provider(settings):
    """Return the active API provider: 'anthropic' or other value."""
    return settings.get("api_provider", "anthropic")


def is_anthropic(settings):
    """Return True if the provider is the native Anthropic API."""
    return get_provider(settings) == "anthropic"


def provider_label(provider):
    """Human-readable provider name for UI."""
    if provider == "anthropic":
        return "Claude"
    return provider.capitalize() if provider else "Claude"

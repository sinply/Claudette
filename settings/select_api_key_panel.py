import sublime
import sublime_plugin

from ..constants import SETTINGS_FILE


class ClaudetteSelectApiKeyPanelCommand(sublime_plugin.WindowCommand):
    """
    A command to switch between different API keys.

    Shows a quick panel of API keys so the user can switch the active key.
    """

    def _get_api_key_config(self, settings):
        """Return (api_key_config, setting_key_path) for the active provider."""
        provider = settings.get("api_provider", "anthropic")
        if provider == "deepseek":
            ds = settings.get("deepseek", {})
            return ds.get("api_key", ""), "deepseek"
        return settings.get("api_key"), "api_key"

    def is_visible(self):
        return True

    def is_enabled(self):
        settings = sublime.load_settings(SETTINGS_FILE)
        api_key, _ = self._get_api_key_config(settings)

        return (
            isinstance(api_key, dict)
            and api_key.get("keys")
            and isinstance(api_key["keys"], list)
            and len(api_key["keys"]) > 1
        )

    def run(self):
        try:
            settings = sublime.load_settings(SETTINGS_FILE)
            api_key, key_path = self._get_api_key_config(settings)
            panel_items = []

            if isinstance(api_key, str) and api_key.strip():
                panel_items.append(["Default"])
            elif (
                isinstance(api_key, dict)
                and api_key.get("keys")
                and isinstance(api_key["keys"], list)
            ):
                for i, key_entry in enumerate(api_key["keys"]):
                    if isinstance(key_entry, dict) and key_entry.get("key"):
                        name = key_entry.get(
                            "name", f"Untitled {i}" if i > 0 else "Untitled"
                        )
                        panel_items.append([name])

            settings_item = (
                "→ Manage API keys" if panel_items else "＋ Add new API key"
            )
            panel_items.append([settings_item])

            def on_select(index):
                if index == -1:
                    return

                if index == len(panel_items) - 1:
                    self.window.run_command(
                        "edit_settings",
                        {
                            "base_file": (
                                "${packages}/Claudette/"
                                "Claudette.sublime-settings"
                            ),
                            "default": "{\n\t$0\n}\n",
                        },
                    )
                else:
                    if isinstance(api_key, str):
                        pass
                    elif isinstance(api_key, dict) and api_key.get("keys"):
                        updated_api_key = api_key.copy()
                        updated_api_key["active_key"] = index
                        if key_path == "deepseek":
                            ds = settings.get("deepseek", {})
                            ds["api_key"] = updated_api_key
                            settings.set("deepseek", ds)
                        else:
                            settings.set("api_key", updated_api_key)
                        sublime.save_settings(SETTINGS_FILE)

                    sublime.status_message(
                        f"Switched to API key: {panel_items[index][0]}"
                    )

            selection_index = 0
            if isinstance(api_key, dict) and api_key.get("keys"):
                current_index = api_key.get("active_key", 0)
                if isinstance(current_index, int) and 0 <= current_index < len(
                    api_key["keys"]
                ):
                    selection_index = current_index

            self.window.show_quick_panel(
                panel_items, on_select, 0, selection_index
            )

        except Exception as e:
            sublime.error_message(
                f"Error showing API key selection panel: {str(e)}"
            )

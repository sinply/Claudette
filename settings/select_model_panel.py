import sublime
import sublime_plugin

from ..api.api import ClaudetteClaudeAPI
from ..api.provider import provider_label
from ..constants import SETTINGS_FILE


class ClaudetteSelectModelPanelCommand(sublime_plugin.WindowCommand):
    """
    A command to switch between different AI models.

    This command shows a quick panel with available models
    and allows the user to select and switch to a different model.
    """

    def is_visible(self):
        return True

    def run(self):
        try:
            api = ClaudetteClaudeAPI()
            settings = sublime.load_settings(SETTINGS_FILE)
            provider = api.provider
            label = provider_label(provider)

            if provider == "deepseek":
                ds = settings.get("deepseek", {})
                current_model = ds.get("model", "deepseek-chat")
            else:
                current_model = settings.get("model")

            models = api.fetch_models()

            if current_model in models:
                selected_index = models.index(current_model)
            else:
                models.insert(0, current_model)
                selected_index = 0

            def on_select(index):
                if index != -1:
                    try:
                        selected_model = models[index]
                        if provider == "deepseek":
                            ds = settings.get("deepseek", {})
                            ds["model"] = selected_model
                            settings.set("deepseek", ds)
                        else:
                            settings.set("model", selected_model)
                        sublime.save_settings(SETTINGS_FILE)

                        sublime.status_message(
                            "{0} model switched to {1}".format(
                                label, str(selected_model)
                            )
                        )
                    except Exception as e:
                        print(f"Error saving model setting: {str(e)}")
                        sublime.error_message(
                            f"Error saving model setting: {str(e)}"
                        )

            self.window.show_quick_panel(models, on_select, 0, selected_index)
        except Exception as e:
            print(f"Error showing model selection panel: {str(e)}")
            sublime.error_message(
                f"Error showing model selection panel: {str(e)}"
            )

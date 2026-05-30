import random
import threading

import sublime
import sublime_plugin

from ..api.api import ClaudetteClaudeAPI
from ..api.handler import ClaudetteStreamingResponseHandler
from ..constants import PLUGIN_NAME, SETTINGS_FILE, TOOL_STATUS_MESSAGES
from ..utils import (
    claudette_chat_status_message,
    claudette_get_api_key_value,
)
from .chat_view import ClaudetteChatView

# Module-level references to prevent GC of input panel callbacks (ST4 bug)
_pending_self = None
_pending_code = ""
_pending_is_new = False
_pending_callback = None


def _show_input_panel(window, cmd_instance, code, is_new):
    """Show the input panel with a module-level callback reference."""
    global _pending_callback

    def on_done(q):
        print("[Claudette DEBUG] on_done triggered, q=", repr(q[:80]))
        cmd_instance.handle_input(code, q)

    _pending_callback = on_done  # Prevent GC
    prompt = "Ask Claude (New Chat):" if is_new else "Ask Claude:"
    v = window.show_input_panel(prompt, "", on_done, None, None)
    print("[Claudette DEBUG] input panel created, view=", v)


class ClaudetteAskQuestionCommand(sublime_plugin.WindowCommand):
    """WindowCommand so Tools menu works without a focused editor view."""

    def load_settings(self):
        if not getattr(self, "settings", None):
            self.settings = sublime.load_settings(SETTINGS_FILE)
        if not hasattr(self, "chat_view"):
            self.chat_view = None

    def get_window(self):
        return self.window or sublime.active_window()

    def is_visible(self):
        return True

    def is_enabled(self):
        return True

    def create_chat_panel(self, force_new=False):
        """
        Creates a chat panel, optionally forcing a new view creation.

        Args:
            force_new (bool): If True, always create a new view instead of
                reusing an existing one.

        Returns:
            sublime.View: The created or existing view
        """
        window = self.get_window()
        if not window:
            print(f"{PLUGIN_NAME} Error: No active window found")
            sublime.error_message(
                f"{PLUGIN_NAME} Error: No active window found"
            )
            return None

        try:
            if force_new:
                self.chat_view = ClaudetteChatView.get_instance(
                    window, self.settings
                )
                return self.chat_view.create_new_chat_view()
            else:
                self.chat_view = ClaudetteChatView.get_instance(
                    window, self.settings
                )
                return self.chat_view.create_or_get_view()

        except Exception as e:
            print(f"{PLUGIN_NAME} Error: {str(e)}")
            sublime.error_message(
                f"{PLUGIN_NAME} Error: Could not create or get chat panel"
            )
            return None

    def handle_input(self, code, question):
        print("[Claudette DEBUG] handle_input called, question=", repr(question[:50] if question else None))
        if not question or question.strip() == "":
            return None

        if not self.create_chat_panel():
            return

        api = ClaudetteClaudeAPI()
        api_key = api.api_key

        if not api_key:
            window = self.get_window()
            claudette_chat_status_message(
                window,
                (
                    "Please add your Claude API key via the "
                    "`Settings > Package Settings > Claudette` menu."
                ),
                "⚠️",
            )
            claudette_chat_status_message(
                window,
                (
                    "Claudette allows you to define a single key, or you can "
                    "add multiple keys each with their own name. For example, "
                    'you can define a "Work" and "Personal" key. If you have '
                    "multiple API keys defined the "
                    "`Claudette: Switch API Key` command allows you switch "
                    "between them."
                ),
                "",
            )
            return

        self.send_to_claude(code, question.strip())

    def run(self, code=None, question=None):
        print("[Claudette DEBUG] AskQuestionCommand.run() called")
        try:
            self.load_settings()

            window = self.get_window()
            if not window:
                print(f"{PLUGIN_NAME} Error: No active window found")
                sublime.error_message(
                    f"{PLUGIN_NAME} Error: No active window found"
                )
                return

            if code is not None and question is not None:
                if not self.create_chat_panel():
                    return
                self.send_to_claude(code, question)
                return

            active = window.active_view()
            sel = active.sel() if active else None
            _pending_code = (
                active.substr(sel[0])
                if active and sel is not None and len(sel) > 0
                else ""
            )
            _pending_self = self
            _pending_is_new = False

            sublime.set_timeout(lambda: _show_input_panel(window, _pending_self, _pending_code, _pending_is_new), 10)

        except Exception as e:
            print(f"{PLUGIN_NAME} Error in run command: {str(e)}")
            sublime.error_message(
                f"{PLUGIN_NAME} Error: Could not process request"
            )

    def send_to_claude(self, code, question):
        print("[Claudette DEBUG] send_to_claude called, question=", repr(question[:80]))
        try:
            if not self.chat_view:
                print("[Claudette DEBUG] no chat_view, returning")
                return

            message = "\n\n---\n\n" if self.chat_view.get_size() > 0 else ""

            message += f"# Question\n\n{question}\n\n"

            if code.strip():
                message += f"**Selected Code**\n\n```\n{code}\n```\n\n"

            user_message = question
            if code.strip():
                user_message = f"{question}\n\nCode:\n{code}"

            conversation = self.chat_view.handle_question(user_message)

            # Capture position before appending
            question_start = self.chat_view.view.size()

            # Save current selection before appending
            view = self.chat_view.view
            saved_selection = [(r.a, r.b) for r in view.sel()]

            self.chat_view.append_text(message)

            # Init API instance for provider-specific labels and request
            api = ClaudetteClaudeAPI()
            use_text_editor = api.settings.get("text_editor_tool", False)
            if use_text_editor and not api.is_anthropic:
                use_text_editor = False

            # Add response heading before streaming begins
            self.chat_view.append_text(
                "# Claude's Response\n\n"
            )

            if self.chat_view.get_size() > 0:
                self.chat_view.focus()

            def smooth_scroll_to_question():
                target_pos = view.text_to_layout(question_start)
                current_pos = view.viewport_position()
                distance_y = target_pos[1] - current_pos[1]
                steps = 20
                step_delay = 15  # ms between steps

                def scroll_step(step):
                    if step >= steps:
                        # Final position to ensure accuracy
                        view.set_viewport_position(target_pos, animate=False)
                        # Restore selection/cursor position
                        view.sel().clear()
                        if saved_selection:
                            for a, b in saved_selection:
                                view.sel().add(sublime.Region(a, b))
                        else:
                            view.sel().add(
                                sublime.Region(question_start, question_start)
                            )
                        return

                    # Ease-out animation (starts fast, slows down)
                    progress = step / steps
                    eased = 1 - (1 - progress) ** 3  # Cubic ease-out

                    new_y = current_pos[1] + (distance_y * eased)
                    view.set_viewport_position(
                        (current_pos[0], new_y), animate=False
                    )

                    sublime.set_timeout(
                        lambda: scroll_step(step + 1), step_delay
                    )

                scroll_step(0)

            sublime.set_timeout(smooth_scroll_to_question, 50)

            message_start = self.chat_view.view.size()

            # Create cancellation token for this request, keyed to this view
            request_view_id = self.chat_view.view.id()
            cancellation_token = self.chat_view.start_request(request_view_id)

            def on_complete(usage_info=None):
                # Clear the active request token for this view
                self.chat_view.clear_request(request_view_id)
                # Clear in-chat tool status so it is not in saved response
                self.chat_view.clear_tool_status()
                # Add response to conversation history after streaming ends
                response_end = self.chat_view.view.size()
                response_region = sublime.Region(message_start, response_end)
                response_text = self.chat_view.view.substr(response_region)
                self.chat_view.handle_response(response_text)
                self.chat_view.on_streaming_complete()
                # Display cost info in the chat view
                if usage_info and self.settings.get("chat", {}).get("show_cost", True):
                    input_tokens = usage_info.get("input_tokens", 0)
                    output_tokens = usage_info.get("output_tokens", 0)
                    cost = usage_info.get("cost", 0.0)
                    session_cost = usage_info.get("session_cost", 0.0)
                    cost_msg = (
                        "Tokens: {0:,} in, {1:,} out. "
                        "Cost: ${2:.4f} (${3:.4f} session)\n"
                    ).format(input_tokens, output_tokens, cost, session_cost)
                    claudette_chat_status_message(
                        self.get_window(), cost_msg, "⚡️"
                    )

            self.chat_view.set_tool_status(random.choice(TOOL_STATUS_MESSAGES))

            handler = ClaudetteStreamingResponseHandler(
                view=self.chat_view.view,
                on_complete=on_complete,
                response_header_end=message_start,
            )
            if use_text_editor:
                target = api.run_with_text_editor_loop
                args = (
                    handler.append_chunk,
                    conversation,
                    self.chat_view,
                    on_complete,
                    cancellation_token,
                )
            else:
                target = api.stream_response
                args = (
                    handler.append_chunk,
                    conversation,
                    self.chat_view.view,
                    cancellation_token,
                )

            thread = threading.Thread(target=target, args=args)
            thread.start()

        except Exception as e:
            print(f"{PLUGIN_NAME} Error sending to API: {str(e)}")
            sublime.error_message(
                f"{PLUGIN_NAME} Error: Could not send message"
            )


class ClaudetteAskNewQuestionCommand(sublime_plugin.WindowCommand):
    def run(self):
        try:
            window = self.window or sublime.active_window()
            if not window:
                print(f"{PLUGIN_NAME} Error: No active window found")
                sublime.error_message(
                    f"{PLUGIN_NAME} Error: No active window found"
                )
                return

            ask_command = ClaudetteAskQuestionCommand(window)
            ask_command.load_settings()

            if not ask_command.create_chat_panel(force_new=True):
                return

            sublime.set_timeout(lambda: _show_input_panel(window, ask_command, "", True), 10)

        except Exception as e:
            print(f"{PLUGIN_NAME} Error in run command: {str(e)}")
            sublime.error_message(
                f"{PLUGIN_NAME} Error: Could not process request"
            )

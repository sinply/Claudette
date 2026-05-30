"""Minimal test for Sublime Text callbacks."""

import sublime
import sublime_plugin

_cb_holder = []


class ClaudetteTestPanelCommand(sublime_plugin.WindowCommand):
    """Test: show_input_panel with all three callbacks."""
    def run(self):
        print("[TEST] run() called")

        def on_done(text):
            print("[TEST] on_done CALLED! text=", repr(text[:80]))

        def on_change(text):
            print("[TEST] on_change CALLED! text=", repr(text[:80]))

        def on_cancel():
            print("[TEST] on_cancel CALLED!")

        _cb_holder.extend([on_done, on_change, on_cancel])

        v = self.window.show_input_panel(
            "TEST:", "", on_done, on_change, on_cancel
        )
        print("[TEST] panel created, view=", v)

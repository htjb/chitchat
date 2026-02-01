from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.widgets import Footer, Header, Static, TextArea


class ChatInput(TextArea):
    """A TextArea that sends a custom message on Shift+Enter."""

    MIN_HEIGHT = 2
    MAX_HEIGHT = 10

    class Submitted(Message):
        """Posted when the user presses Shift+Enter."""

        def __init__(self, text_area: "ChatInput", value: str) -> None:
            """Initialise with the source TextArea and its current value."""
            super().__init__()
            self.text_area = text_area
            self.value = value

    BINDINGS = [("shift+enter", "submit", "Send message")]

    def action_submit(self) -> None:
        """Post a Submitted message with the current text."""
        self.post_message(self.Submitted(self, self.text))

    def _update_height(self) -> None:
        """Grow/shrink to fit the current number of lines."""
        lines = self.text.count("\n") + 1
        # +1 for a blank line below the text so it doesn't feel cramped
        new_height = max(self.MIN_HEIGHT, min(lines + 1, self.MAX_HEIGHT))
        self.styles.height = new_height

    def on_text_area_changed(self) -> None:
        """Called whenever the text changes (typing or clearing)."""
        self._update_height()


class ChitChat(App):
    CSS_PATH = "static/styles.css"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(id="messages")
        yield ChatInput(
            id="chat_input",
            language="text",
        )
        yield Footer()

    def on_chat_input_submitted(
        self, event: ChatInput.Submitted
    ) -> None:
        """Called when the user presses Shift+Enter."""
        content = event.value.strip()
        if not content:
            return
        event.text_area.clear()  # clear the text area

        messages = self.query_one("#messages", Vertical)

        # User message
        user_msg = Static(f"You: {content}")
        user_msg.add_class("msg-user")
        messages.mount(user_msg)

        # Placeholder LLM reply (swap this out for the real call later)
        llm_msg = Static("Assistant: ...")
        llm_msg.add_class("msg-llm")
        messages.mount(llm_msg)


if __name__ == "__main__":
    app = ChitChat()
    app.run()

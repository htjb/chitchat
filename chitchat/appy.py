from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.widgets import Footer, Header, Static, TextArea


class ChatInput(TextArea):
    """A TextArea that sends a custom message on Shift+Enter."""

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



class ChitChat(App):
    CSS_PATH = "static/styles.css"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(id="messages")
        with Vertical(id="bottom"):
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

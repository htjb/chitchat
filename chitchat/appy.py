from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.events import Key
from textual.widgets import Footer, Header, Input, Static


class CustomInput(Input):
    def on_key(self, event: Key) -> None:
        # 1. Check for the specific key combo you want
        if event.key == "shift+enter":  # Many terminals send ctrl+enter as ctrl+j
             self.post_message(Input.Submitted(self, self.value))
             event.stop()  # Prevent further handling
             event.prevent_default()

        elif event.key == "enter":
             event.stop()
             event.prevent_default()


class ChitChat(App):
    CSS_PATH = "static/styles.css"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(id="messages")  # for messages
        yield CustomInput(placeholder="Type your message here...", id="chat_input")
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """This is called when the user presses Enter in an Input widget."""
        content = event.value
        event.input.value = ""  # clear the input

        messages = self.query_one("#messages", Vertical)
        messages.mount(Static(content))  # add message to the list

if __name__ == "__main__":
    app = ChitChat()
    app.run()

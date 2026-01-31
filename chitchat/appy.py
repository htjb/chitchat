from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TextArea


class ChitChat(App):
    """A Textual app to chat to ollama models."""

    CSS_PATH = "static/styles.css"

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield TextArea(id='inputtext', placeholder="Type your message here...")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme ==
            "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = ChitChat()
    app.run()

"""Main module for the ChitChat application."""

from chitchat.chat import ChitChat


def main() -> None:
    """Main entry point for chitchat."""
    app = ChitChat()
    app.run()

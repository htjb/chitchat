from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.widgets import Footer, Header, Static, TextArea

import os
import yaml
import ollama
from ollama import chat

home = os.environ['HOME']

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
    def __init__(self) -> None:
        super().__init__()
        self.history = []


        config_path = home + "/.config/chitchat/chitchat.yaml"
        if os.path.exists(config_path):
            config = yaml.safe_load(open(config_path))

        available_models = ollama.list()
        self.models = [av.model.split(':')[0] 
                       for av in available_models.models]
        self.model_name = config.get('default_model', self.models[0]) \
            if 'config' in locals() else self.models[0]
        

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(id="messages")
        with Vertical(id="bottom"):
            yield ChatInput(
                id="chat_input",
                language="text",
            )
            yield Footer()

    def on_mount(self) -> None:
        system_msg = Static("Welcome to ChitChat! Type your message and press Shift+Enter to chat.\n" +
                            f"Using model: {self.model_name.split(':')[0]}\n" +
                            f"Available models: {', '.join(models.split(':')[0] for models in self.models)}\n" +
                            "To change model type /model MODEL_NAME\n" +
                            "--- Type /exit or /quit to leave the chat ---")
        system_msg.add_class("msg-system")

        messages = self.query_one("#messages", Vertical)
        messages.mount(system_msg)
        self.history.append({'role': 'system', 'content': system_msg.content})

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

        if content.lower() in ['/exit', '/quit']:
            print("Exiting the chat. Goodbye!")
            self.exit()
            return
        elif content.lower().startswith('/model '):
            _, model_name = content.split(' ', 1)
            if model_name in self.models:
                self.model_name = model_name
                system_msg = Static(f"Switched to model: {model_name}")
                system_msg.add_class("msg-system")
                messages.mount(system_msg)
            else:
                system_msg = Static(f"Model '{model_name}' not found." +  
                            f"Available models: {', '.join(self.models)}")
                system_msg.add_class("msg-system")
                messages.mount(system_msg)
            self.history.append({'role': 'system', 'content': system_msg.content})
            return

        self.history.append({'role': 'user', 'content': content})

        # Mount the LLM message now so it appears immediately
        llm_msg = Static("Assistant: ")
        llm_msg.add_class("msg-llm")
        messages.mount(llm_msg)

        # Stream the reply in a background thread
        self.run_worker(
            lambda: self._stream_reply(llm_msg),
            thread=True,
            name="llm_stream",
            exclusive=True,
        )

    def _stream_reply(self, llm_msg: Static) -> None:
        """Run the ollama stream in a thread, updating the widget per token."""
        response = ""
        for chunk in chat(
            model=self.model_name,
            messages=self.history,
            stream=True,
        ):
            response += chunk["message"]["content"]
            self.call_from_thread(
                llm_msg.update, f"Assistant: {response}"
            )
        self.history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    app = ChitChat()
    app.run()

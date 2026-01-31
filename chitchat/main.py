from chitchat.chat import converse

def main():
    stream = True
    history = []
    while stream:
        user_input = input("\nYou: ")
        if user_input.lower() in ['/exit', '/quit']:
            print("Exiting the chat. Goodbye!")
            break
        history = converse(user_input, history)

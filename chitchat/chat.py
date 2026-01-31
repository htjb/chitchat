from ollama import chat

def converse(message: str, history: list, model: str) -> list:
    message = message.strip()

    # Add user message to history
    history.append({'role': 'user', 'content': message})

    
    stream = chat(
            model=model,
            messages=history,
            stream=True)

    # Collect the full response
    response = ''
    for chunk in stream:
        content = chunk['message']['content']
        print(content, end='', flush=True)
        response += content

    # Add complete assistant response to history
    history.append({'role': 'assistant', 'content': response})
    return history

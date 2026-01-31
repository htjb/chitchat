"""Main module for the ChitChat application."""

from chitchat.chat import converse
import ollama
import os
import yaml

home = os.environ['HOME']

def main():
    """Main entry point for chitchat."""
    print("Welcome to ChitChat! Type your message and press Enter to chat.")
    
    config_path = home + "/.config/chitchat/chitchat.yaml"
    if os.path.exists(config_path):
        config = yaml.safe_load(open(config_path))

    available_models = ollama.list()
    models = [av.model for av in available_models.models]
    model_name = config.get('default_model', models[0]) if 'config' in locals() else models[0]

    print('Using model: ', model_name.split(':')[0])
    print('Available models: ', ', '.join(models.split(':')[0] for models in models))
    print('To change model type /model MODEL_NAME')
    print('--- Type /exit or /quit to leave the chat ---')

    stream = True

    history = []
    while stream:
        user_input = input("\nYou: ")
        if user_input.lower() in ['/exit', '/quit']:
            stream = False
        elif user_input.lower().startswith('/model '):
            _, model_name = user_input.split(' ', 1)
            if model_name in models:
                print(f"Switching to model: {model_name}")
            else:
                print(f"Model '{model_name}' not found. Available models: {', '.join(models)}")
        else:
            history = converse(user_input, history, model=model_name)

    
    print("Exiting the chat. Goodbye!")

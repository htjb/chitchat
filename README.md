# chitchat

Minimal terminal REPL for ollama models.

## Installation

- Need to install [ollama](https://ollama.com/download) first.
- Then install the ollama python package using pip:

```bash
pip install ollama
```

- Then clone this repository and install chitchat:

```bash
git clone https://github.com/htjb/chitchat
cd chitchat
pip install .
```

- Then finally install a model using ollama, e.g.:

```bash
ollama pull gemma3
```

## Usage

Run the `chitchat` command in the terminal and type /exit to quit.

![chitchat_screenshot.svg](https://github.com/htjb/chitchat/raw/tui/chitchat_screenshot.svg)
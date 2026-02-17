# Build an AI agent on your mac

## Inspiration 

https://fly.io/blog/everyone-write-an-agent/ 

## Slides 

https://docs.google.com/presentation/d/1NetuiK9HCjfAA4B-EsnQg75FCkjn6oGchTKw81IaxGw/edit?usp=sharing

## Installation 

Python dependencies:
```
python3 -m venv .venv
source .venv/bin/activate
pip install openai colorama rich
```

OpenAI API key configuration: 
```
export OPENAI_API_KEY=XXX
```

Install `ollama` to download and serve open-source LLMs on your mac: 
```
curl -fsSL https://ollama.com/install.sh | sh
PATH=$PATH:$HOME/.local/bin
export OLLAMA_CONTEXT_LENGTH=16384
ollama pull qwen3:8b
ollama serve
```

## Lessons

1. Accumulating messages to give the illusion of state (`llms_are_stateless.py`) 
2. Chatbots are based on the Read-Eval-Print Loop (`repl.py`)
3. Our first AI agent: A genomics assistant that can translate DNA sequences to proteins (`one_tool.py`)
4. The LLM, not the user, orchestrates the correct sequence of function calling (`two_tools.py`)
5. Neurally guided program synthesis (`four_tools.py`)
6. Local LLM deployment for practical genomics applications is becoming a reality (`four_tools.py --local`) 
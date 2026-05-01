# Running Local LLMs with Ollama

This repository contains a 2-hour beginner workshop on running open-source language models locally with Ollama and Python.

The examples are intentionally small and heavily commented so participants can see the raw mechanics:

1. Basic text generation
2. Streaming chat in the terminal
3. Structured JSON outputs with Pydantic
4. Local tool calling with a Python function

## Workshop Goal

By the end of the session, you will have a tiny offline AI stack running on your own machine:

- Ollama serving a model locally
- Python scripts talking to `http://localhost:11434`
- Pydantic validating JSON responses
- A model deciding when to call a Python tool

This feels similar to calling a cloud API, but the compute happens on your laptop instead of on a remote service.

## Prerequisites

Install these before the workshop:

1. Python 3.11+
2. Ollama desktop for macOS, Windows, or Linux
3. A code editor such as VS Code or Cursor

Then pull one model that fits your hardware.

### Option A: Older laptop or under 8 GB RAM

```bash
ollama pull qwen2.5:0.5b
# or
ollama pull llama3.2:1b
```

### Option B: Standard laptop, 8 GB to 16 GB RAM

```bash
ollama pull llama3.2
```

### Option C: Larger machine, 32 GB+ RAM or strong GPU

```bash
ollama pull llama3.1
```

## Project Setup

Clone the repository and enter it:

```bash
git clone https://github.com/Nyala-Labs/ollama-workshop.git
cd ollama-workshop
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # macOS / Linux / WSL
# venv\Scripts\activate   # Windows PowerShell / CMD
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Copy the example environment file:

```bash
cp .env.example .env
```

The defaults are already fine for most participants. If needed, change `OLLAMA_MODEL` in `.env` or edit the `MODEL` variable at the top of any script.

## File Layout

```text
.
├── 01_basic_generation.py
├── 02_streaming_chat.py
├── 03_structured_outputs.py
├── 04_local_tool_calling.py
├── .env.example
├── .gitignore
├── .codex
├── README.md
└── requirements.txt
```

## Run The Workshop

Start Ollama first. The desktop app should be running in your system tray or menu bar.

If you want to warm up a model before running the scripts, you can do:

```bash
ollama run llama3.2:1b
```

Swap the model name to match the one you pulled.

### Part 1: Basic local generation

```bash
python 01_basic_generation.py
```

What this teaches:

- Ollama exposes a local HTTP API on `localhost`
- The Python SDK wraps that local API
- A normal chat request returns one complete response

### Part 2: Streaming chat in the terminal

```bash
python 02_streaming_chat.py
```

What this teaches:

- `stream=True` yields chunks instead of one full response
- We can print tokens as they arrive
- We keep conversation history in a Python list

### Part 3: Structured outputs with Pydantic

```bash
python 03_structured_outputs.py
```

What this teaches:

- We can pass a JSON schema to Ollama
- The model returns machine-readable JSON instead of free-form prose
- Pydantic validates the response before our app trusts it

### Part 4: Local tool calling

```bash
python 04_local_tool_calling.py
```

What this teaches:

- The model can decide when it needs a tool
- Ollama sends back tool calls instead of only plain text
- Python executes the tool and feeds the result back into the conversation

## Suggested Teaching Flow

### 1. Start simple

Open `01_basic_generation.py` and point out:

- `MODEL` can be changed for different hardware
- `Client(host=HOST)` still talks to a local server
- `messages` looks like a cloud chat API, but the model runs on-device

### 2. Add interactivity

Move to `02_streaming_chat.py` and show:

- how streaming improves perceived speed
- how the assistant reply is accumulated
- why we append both user and assistant turns into `messages`

### 3. Make the output reliable

Open `03_structured_outputs.py` and show:

- the Pydantic schema
- the `format=` argument
- the difference between raw model text and validated JSON

### 4. Give the model a tool

Open `04_local_tool_calling.py` and show:

- the Python `get_weather` function
- the `tools=[get_weather]` argument
- the ReAct-style loop that keeps asking the model what to do next

## Troubleshooting

If a script says it cannot reach Ollama:

1. Make sure the Ollama desktop app is running.
2. Make sure the model is already pulled.
3. Try warming up the model once in a terminal:

```bash
ollama run llama3.2:1b
```

If tool calling behaves strangely on a tiny model:

- try `qwen2.5:0.5b`
- or use a stronger tool-capable model such as `llama3.1`

If structured outputs are inconsistent:

- keep the prompt explicit
- ask for JSON only
- use `temperature=0`

## Hardware Tuning Notes

For a short workshop, the easiest tuning advice is:

- Smaller models start faster and use less RAM
- Longer prompts and longer chat history consume more context
- If your machine slows down, switch to a smaller model
- If Ollama is holding too much memory, stop the running model from the Ollama app or CLI

## Dependencies

This project uses:

- `ollama`
- `pydantic`
- `python-dotenv`

Everything is written in plain Python on purpose. There is no LangChain, no LlamaIndex, and no extra framework hiding what is happening.

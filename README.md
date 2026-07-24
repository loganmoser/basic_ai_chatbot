# Basic AI Chatbot

A small autonomous coding agent, written in Python, that uses an LLM (via [OpenRouter](https://openrouter.ai/)) to investigate, fix, and verify code in a target directory — all from the command line.

You give it a single instruction (e.g. "fix the bug in the calculator"), and it decides for itself which files to look at, what changes to make, and how to check its own work, using a small set of tools you give it.

## How It Works

At its core, this project is a **tool-use loop**. Instead of the model just replying with text, it can ask your program to run functions on its behalf — reading files, writing files, or executing code — and see the results before deciding what to do next.

The agent has four tools available:

| Tool | What it does |
|---|---|
| `get_files_info` | Lists files/directories in the working directory |
| `get_file_content` | Reads the contents of a specific file |
| `run_python_file` | Executes a Python file and captures its output |
| `write_file` | Writes/overwrites a file with new content |

Each turn of the loop works like this:

1. Your prompt (plus a system prompt describing the agent's workflow) is sent to the model along with the list of available tools.
2. The model replies — either with a final answer, or with one or more **tool calls** (e.g. "call `get_file_content` on `main.py`").
3. Your program actually executes those tool calls locally, and feeds the results back to the model as new messages.
4. This repeats (up to 20 iterations) until the model responds with plain text instead of a tool call — at which point that's treated as the final answer and printed.

This is the same basic pattern behind most "AI agent" tools: the model doesn't take actions directly — it asks, your code executes, and the loop continues until the task is done.

The system prompt instructs the agent to follow a specific workflow for each request: **investigate** (look at only what's needed), **act** (write the fix, without asking permission), **verify** (run the code to confirm it works), and **report** (summarize what changed).

By default, the agent operates on the `calculator/` directory in this repo, which acts as a small sandbox project for it to read, modify, and test.

## Requirements

- Python 3.12+
- An [OpenRouter API key](https://openrouter.ai/keys) (used to access LLMs through OpenRouter's OpenAI-compatible API)
- [`uv`](https://docs.astral.sh/uv/) (the project uses `pyproject.toml` + `uv.lock` for dependency management), or `pip` if you prefer

## Installation

```bash
# Clone the repository
git clone https://github.com/loganmoser/basic_ai_chatbot.git
cd basic_ai_chatbot

# Install dependencies with uv
uv sync

# or, with pip
pip install openai python-dotenv
```

## Setup

1. Sign up at [openrouter.ai](https://openrouter.ai/) and generate an API key.
2. Create a `.env` file in the project root:

   ```
   OPENROUTER_API_KEY=your-api-key-here
   ```

`.env` is already listed in `.gitignore`, so your key won't get committed.

## Usage

The agent takes your instruction as a single command-line argument (it's not an interactive chat loop — one prompt in, one final answer out, with the tool-use loop happening in between):

```bash
uv run main.py "fix the bug in the calculator app"
```

Or with plain Python:

```bash
python main.py "fix the bug in the calculator app"
```

Add `--verbose` to see token usage and the exact arguments passed to each tool call as the agent works:

```bash
uv run main.py "fix the bug in the calculator app" --verbose
```

Example output:

```
 - Calling function: get_files_info
 - Calling function: get_file_content
 - Calling function: write_file
 - Calling function: run_python_file
Fixed a divide-by-zero error in calculator/operations.py and confirmed
the app now runs correctly with the corrected input.
```

## Project Structure

```
basic_ai_chatbot/
├── main.py              # CLI entry point + the tool-use loop
├── call_function.py     # Dispatches model tool calls to real Python functions
├── prompts.py           # System prompt defining the agent's workflow
├── functions/           # Tool implementations (get_files_info, get_file_content, run_python_file, write_file)
├── calculator/          # Sandbox project the agent reads/modifies/tests
├── tests/               # Test suite
├── pyproject.toml       # Project metadata & dependencies (uv)
└── uv.lock
```

## Configuration

The model is set in `main.py`:

```python
response = client.chat.completions.create(
    model="openrouter/free",
    ...
)
```

You can swap this for any model OpenRouter supports (see [OpenRouter's model list](https://openrouter.ai/models)) — just note that models with actual tool-calling support will work much better than ones without it, since this agent's whole approach depends on tool calls.

## Possible Improvements

Ideas if you want to extend this project further:

- Point the agent at other directories, not just `calculator/`
- Add more tools (e.g. running tests, searching across files)
- Stream the model's output instead of waiting for the full reply
- Add a proper interactive/multi-turn chat mode alongside the single-prompt mode

# Charlie AI - English Teacher for Kids

A core backend service for an interactive English lesson flow, powered by AI. Charlie is an 8-year-old fox from London who guides kids (ages 4-8) through a vocabulary mini-lesson.

## Architecture & Technical Decisions

Working with kids requires strict control over the educational flow. A pure LLM agent approach is prone to hallucinations, skipping logic, or discussing off-topic subjects (like Roblox) indefinitely.

To solve this, this service uses a **Hybrid FSM + Two-Step LLM Pipeline**:
1. **Finite State Machine (FSM):** The lesson logic (`engine.py`) is rigidly controlled by code (`GREETING` -> `PRESENTATION` -> `PRACTICE` -> `GOODBYE`). This guarantees the lesson never derails.
2. **Two-Step LLM Pipeline (`llm_client.py`):**
   - **Evaluator (JSON Mode):** Analyzes the child's raw input and categorizes intent (`correct`, `incorrect`, `off_topic`, `silence`). Temperature is set to `0.0` for deterministic routing.
   - **Persona Generator:** Receives the evaluated intent, the target word, and the child's input to generate an empathetic, context-aware, and character-accurate response. Temperature is set to `0.7` for natural conversational flow.

## Quick Start

This project uses `uv` for lightning-fast, deterministic dependency management. It is fully cross-platform and works seamlessly on Windows (PowerShell/CMD), WSL, macOS, and Linux.

### Prerequisites
- Python >= 3.11
- [uv](https://github.com/astral-sh/uv) installed

### Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd charlie_ai
   ```

2. Set up your environment variables:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=gsk_your_api_key_here
   ```

3. Run the interactive CLI tester. `uv` will automatically handle the virtual environment and dependencies:
   ```bash
   uv run main.py
   ```

# ResearchAgent

An autonomous AI research assistant built with Streamlit. Give it a topic — it searches the web, reads the results, extracts facts, and produces a structured markdown report you can download as a PDF.

## How it works

The agent runs in a loop controlled by the depth you select:

1. **Plan** — asks Groq (LLaMA 3.3 70B) what to search for next, given everything already gathered
2. **Search** — runs a real web search via DuckDuckGo
3. **Extract** — feeds the top 3 results back to Groq to pull out key facts
4. **Repeat** — continues until the iteration limit is reached
5. **Synthesise** — makes a final Groq call to write a full structured report from all accumulated facts

## Features

- Live activity log that updates in real time as the agent works
- Three depth levels: Quick (3 searches), Standard (5), Deep (8)
- Post-run stats: iterations, sources read, facts extracted
- Styled markdown report rendered directly in the app
- One-click PDF download

## Project structure

```
ResearchAgent/
├── app.py            # Agent logic and Streamlit layout
├── ui.py             # All CSS, HTML components, and styling helpers
├── requirements.txt  # Python dependencies
└── .gitignore
```

## Setup

**1. Clone the repo and install dependencies**

```bash
pip install -r requirements.txt
```

**2. Set your Groq API key**

Get a free key at [console.groq.com](https://console.groq.com).

```bash
# macOS / Linux
export GROQ_API_KEY=your_key_here

# Windows (PowerShell)
$env:GROQ_API_KEY = "your_key_here"
```

Or create a `.env` file and load it before running:

```
GROQ_API_KEY=your_key_here
```

**3. Run the app**

```bash
streamlit run app.py
```

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `groq` | LLM inference via Groq API |
| `duckduckgo-search` | Web search (no API key needed) |
| `fpdf2` | PDF generation |
| `markdown` | Markdown-to-HTML conversion for the report |

## Model

Uses `llama-3.3-70b-versatile` via the Groq API for all three agent steps: query planning, fact extraction, and report synthesis.

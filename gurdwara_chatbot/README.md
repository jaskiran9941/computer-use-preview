# Fremont Gurdwara Sahib Chatbot
### Darbar & Langar Etiquette Guide

A RAG-powered chatbot that answers questions about Gurdwara etiquette for
visitors and sangat members. Built with Python, Flask, and the Claude API.

---

## Features

- **30 knowledge-base entries** across three categories: Darbar, Langar, General
- **RAG pipeline**: keyword-overlap retrieval feeds grounded context into Claude
- **Multi-turn conversations** with per-session history
- **FAQ sidebar** for quick browsing of common questions
- **Honest uncertainty**: redirects to the Gurdwara office when the KB doesn't have an answer
- **Culturally authentic tone**: English-primary with natural Punjabi terms

---

## Project Structure

```
gurdwara_chatbot/
├── app.py                  # Flask web app (API routes + session management)
├── rag_engine.py           # RAG retrieval + Claude API integration + prompt templates
├── knowledge_base.json     # 30 curated Q&A entries (Darbar, Langar, General)
├── requirements.txt        # Python dependencies
├── PROMPT_ENGINEERING.md   # 1-page explanation of prompt design decisions
├── templates/
│   └── index.html          # Chatbot HTML shell
└── static/
    ├── style.css           # Navy + saffron Sikh-themed UI
    └── chat.js             # Frontend: message rendering, FAQ panel, session management
```

---

## Setup & Running

### Prerequisites
- Python 3.11+
- An [Anthropic API key](https://console.anthropic.com/)

### Install

```bash
cd gurdwara_chatbot
pip install -r requirements.txt
```

### Run

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python app.py
```

Then open **http://localhost:5000** in your browser.

---

## Knowledge Base

The knowledge base (`knowledge_base.json`) is a JSON file with 30 entries
organized into three categories:

| Category | Topics |
|---|---|
| **Darbar** | Head covering, shoe removal, Matha Tek, Ardas, Karah Prashad, Maryada, Kirtan etiquette |
| **Langar** | Vegetarian food, serving hours, pangat seating, seva, donations |
| **General** | Gurdwara location, visiting hours, Waheguru, Guru Granth Sahib Ji, Gurpurab, children, seva |

To extend the knowledge base, add new entries to `knowledge_base.json`
following the existing schema — no code changes required.

---

## Prompt Engineering

See [`PROMPT_ENGINEERING.md`](PROMPT_ENGINEERING.md) for a full explanation of:
- The system prompt and why each instruction was chosen
- The RAG user-message template
- Two example conversations (1 easy, 1 tricky)
- Why RAG outperforms a standalone LLM for this use case

---

## RAG Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────┐
│  Retrieval (keyword overlap, top-3)             │
│  knowledge_base.json → matching Q&A entries     │
└───────────────────┬─────────────────────────────┘
                    │ context passages
                    ▼
┌─────────────────────────────────────────────────┐
│  Augmentation                                   │
│  System prompt + CONTEXT block + user query     │
└───────────────────┬─────────────────────────────┘
                    │ augmented prompt
                    ▼
┌─────────────────────────────────────────────────┐
│  Generation (Claude claude-sonnet-4-6)              │
│  Grounded, respectful, bilingual response       │
└─────────────────────────────────────────────────┘
```

---

*Waheguru Ji Ka Khalsa, Waheguru Ji Ki Fateh!*

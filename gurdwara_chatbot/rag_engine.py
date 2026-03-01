"""
RAG Engine for Fremont Gurdwara Sahib Chatbot.

Implements a simple but effective Retrieval-Augmented Generation (RAG) flow:
  1. Retrieve: search the knowledge base for entries relevant to the user query
  2. Augment: inject retrieved context into a carefully engineered prompt
  3. Generate: call the Claude API to produce a respectful, grounded response
"""

import json
import os
import re
from pathlib import Path
from typing import Optional
import anthropic

# ---------------------------------------------------------------------------
# Knowledge-base loading
# ---------------------------------------------------------------------------

KB_PATH = Path(__file__).parent / "knowledge_base.json"


def load_knowledge_base() -> list[dict]:
    """Load all entries from the JSON knowledge base."""
    with open(KB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["entries"]


KB_ENTRIES: list[dict] = load_knowledge_base()


# ---------------------------------------------------------------------------
# Retrieval helpers
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> set[str]:
    """Simple whitespace/punctuation tokenizer lowercased."""
    return set(re.findall(r"[a-z]+", text.lower()))


def retrieve(query: str, top_k: int = 3) -> list[dict]:
    """
    Keyword-overlap retrieval: score each KB entry by the number of query
    tokens that appear in its keyword list, question, or answer, then return
    the top_k entries with a score > 0.

    This is intentionally lightweight — no embedding server required.
    """
    query_tokens = _tokenize(query)
    scored: list[tuple[float, dict]] = []

    for entry in KB_ENTRIES:
        # Build a token set for this entry from all relevant fields
        entry_tokens = (
            set(entry.get("keywords", []))
            | _tokenize(entry["question"])
            | _tokenize(entry["answer"])
        )
        overlap = len(query_tokens & entry_tokens)
        if overlap > 0:
            scored.append((overlap, entry))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [e for _, e in scored[:top_k]]


# ---------------------------------------------------------------------------
# Prompt engineering
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are the friendly and knowledgeable chatbot for Fremont Gurdwara Sahib. \
Your role is to help visitors and sangat members understand Darbar (the main \
prayer hall) etiquette, Langar (community kitchen) etiquette, and general \
information about the Gurdwara.

Guidelines for every response:
- Be warm, respectful, and welcoming — every person who asks is a guest of \
  the Gurdwara.
- Keep answers concise (2–4 short paragraphs at most).
- Write primarily in English, but naturally weave in a small number of Punjabi \
  or Gurmukhi terms where they add meaning or authenticity \
  (e.g., seva, sangat, Waheguru, matha tek, pangat, Gurbani, Maryada). \
  Always briefly clarify a Punjabi term the first time you use it.
- Ground every answer in the CONTEXT passages below. Do NOT invent facts.
- If the CONTEXT does not contain enough information to answer confidently, \
  say so honestly and invite the visitor to ask the Gurdwara office directly \
  or visit the official website. Never guess.
- End with a warm closing that reinforces the Gurdwara's welcoming spirit when \
  appropriate (e.g., "The sangat looks forward to welcoming you!").
"""


def build_user_message(query: str, context_entries: list[dict]) -> str:
    """Construct the user-facing message that includes retrieved context."""
    if context_entries:
        context_block = "\n\n".join(
            f"[{e['category'].upper()} — Q: {e['question']}]\n{e['answer']}"
            for e in context_entries
        )
        return (
            f"CONTEXT (from Gurdwara knowledge base):\n"
            f"---\n{context_block}\n---\n\n"
            f"Visitor question: {query}"
        )
    else:
        return (
            "CONTEXT: No matching entries were found in the knowledge base.\n\n"
            f"Visitor question: {query}"
        )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def chat(
    query: str,
    conversation_history: Optional[list[dict]] = None,
    top_k: int = 3,
) -> dict:
    """
    Main entry point. Returns a dict with:
      - answer (str): the assistant's response
      - sources (list[dict]): the KB entries used for context
      - retrieved_count (int): number of entries retrieved
    """
    if conversation_history is None:
        conversation_history = []

    # Step 1 — Retrieve relevant context
    sources = retrieve(query, top_k=top_k)

    # Step 2 — Build the augmented user message
    user_message = build_user_message(query, sources)

    # Step 3 — Assemble the messages list (support multi-turn)
    messages = list(conversation_history) + [
        {"role": "user", "content": user_message}
    ]

    # Step 4 — Call the Claude API
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {
            "answer": (
                "I'm sorry, I cannot connect to the AI service right now. "
                "Please contact the Gurdwara office directly for assistance. "
                "Waheguru Ji Ka Khalsa, Waheguru Ji Ki Fateh!"
            ),
            "sources": [],
            "retrieved_count": 0,
        }

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    )

    answer = response.content[0].text.strip()

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_count": len(sources),
    }

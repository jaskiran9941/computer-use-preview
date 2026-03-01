"""
Flask web application for the Fremont Gurdwara Sahib Chatbot.

Routes:
  GET  /           → serve the chatbot UI
  POST /api/chat   → RAG-powered chat endpoint
  GET  /api/faq    → return the full knowledge base for the FAQ panel
"""

from flask import Flask, jsonify, render_template, request, send_from_directory
import os
import json
from pathlib import Path

# Import our RAG engine
import sys
sys.path.insert(0, str(Path(__file__).parent))
from rag_engine import chat, KB_ENTRIES

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)


# ---------------------------------------------------------------------------
# In-memory session store (keyed by session_id sent from the browser)
# ---------------------------------------------------------------------------
_sessions: dict[str, list[dict]] = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(force=True)
    query = (data.get("message") or "").strip()
    session_id = (data.get("session_id") or "default").strip()

    if not query:
        return jsonify({"error": "No message provided"}), 400

    # Retrieve or create conversation history for this session
    history = _sessions.get(session_id, [])

    result = chat(query, conversation_history=history)

    # Append this turn to history (use the raw query — not the augmented msg)
    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": result["answer"]})

    # Keep history bounded to the last 20 turns to avoid token bloat
    _sessions[session_id] = history[-20:]

    return jsonify({
        "answer": result["answer"],
        "retrieved_count": result["retrieved_count"],
        "sources": [
            {
                "category": s["category"],
                "question": s["question"],
            }
            for s in result["sources"]
        ],
    })


@app.route("/api/faq")
def api_faq():
    """Return the knowledge base entries grouped by category."""
    grouped: dict[str, list] = {}
    for entry in KB_ENTRIES:
        cat = entry["category"]
        grouped.setdefault(cat, []).append({
            "id": entry["id"],
            "question": entry["question"],
            "answer": entry["answer"],
        })
    return jsonify(grouped)


@app.route("/api/reset", methods=["POST"])
def api_reset():
    data = request.get_json(force=True)
    session_id = (data.get("session_id") or "default").strip()
    _sessions.pop(session_id, None)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)

# Prompt Engineering for the Fremont Gurdwara Sahib Chatbot

## 1. Overview

This document explains the two-layer prompt design used by the chatbot and the
reasoning behind each decision.

---

## 2. System Prompt

```
You are the friendly and knowledgeable chatbot for Fremont Gurdwara Sahib.
Your role is to help visitors and sangat members understand Darbar (the main
prayer hall) etiquette, Langar (community kitchen) etiquette, and general
information about the Gurdwara.

Guidelines for every response:
- Be warm, respectful, and welcoming — every person who asks is a guest of
  the Gurdwara.
- Keep answers concise (2–4 short paragraphs at most).
- Write primarily in English, but naturally weave in a small number of Punjabi
  or Gurmukhi terms where they add meaning or authenticity
  (e.g., seva, sangat, Waheguru, matha tek, pangat, Gurbani, Maryada).
  Always briefly clarify a Punjabi term the first time you use it.
- Ground every answer in the CONTEXT passages below. Do NOT invent facts.
- If the CONTEXT does not contain enough information to answer confidently,
  say so honestly and invite the visitor to ask the Gurdwara office directly
  or visit the official website. Never guess.
- End with a warm closing that reinforces the Gurdwara's welcoming spirit when
  appropriate (e.g., "The sangat looks forward to welcoming you!").
```

### Why this system prompt works

| Design choice | Rationale |
|---|---|
| **Role definition** ("You are the friendly chatbot for…") | Anchors the model's persona immediately. Without this, the LLM may default to a generic assistant tone that feels cold or overly formal for a religious setting. |
| **Explicit warmth instruction** | Gurdwara etiquette is a sensitive topic for many visitors. A warm, welcoming tone reduces anxiety about "doing the wrong thing." |
| **Length constraint** (2–4 paragraphs) | Etiquette questions deserve complete answers, but walls of text overwhelm visitors who are often on mobile devices. The constraint forces conciseness. |
| **Bilingual instruction** (English + selective Punjabi) | Using terms like *seva*, *sangat*, and *Maryada* authentically conveys the Sikh context without alienating non-Punjabi speakers. The "clarify on first use" rule prevents confusion. |
| **"Ground every answer in CONTEXT"** | This is the core RAG safety rail. Without this, the model may confabulate details (wrong hours, incorrect rituals). Grounding prevents hallucination. |
| **Honest uncertainty behavior** | Instructing the model to say "I don't know" and redirect to the office is critical for a religious/cultural guide. Incorrect etiquette advice could offend visitors or cause embarrassment. |
| **Warm closing** | Mirrors the Gurdwara's actual culture of hospitality (*sarbat da bhala* — welfare of all). It leaves every interaction on a positive note. |

---

## 3. User Message Template (RAG Augmentation)

```
CONTEXT (from Gurdwara knowledge base):
---
[DARBAR — Q: What should I wear when entering the Darbar Sahib?]
Please dress modestly and cover your head with a rumala (head scarf)…

[LANGAR — Q: Is the Langar food vegetarian?]
Yes, Langar is always strictly vegetarian…
---

Visitor question: <the actual user query>
```

### Why this user-message structure works

| Design choice | Rationale |
|---|---|
| **Explicit `CONTEXT:` label with `---` delimiters** | Clearly delineates retrieved knowledge from the user's question. The model reliably treats content between delimiters as reference material rather than part of the question. |
| **Category prefix in brackets** (`[DARBAR — Q: …]`) | Gives the model instant structural awareness of where each passage comes from, making it easier to synthesize across categories when a question spans multiple topics. |
| **Original question + answer format** | Providing the matched question helps the model understand the intent of each passage, not just its content, leading to more precise answers. |
| **No-context fallback message** | When retrieval returns zero results, the context block explicitly says "No matching entries were found." This prevents the model from searching its own training data and potentially hallucinating Gurdwara-specific details. |

---

## 4. Retrieval Strategy

The RAG retrieval uses **keyword overlap scoring**:

1. Tokenize both the user query and each knowledge-base entry (keywords + question text + answer text).
2. Score each entry by the number of shared tokens.
3. Return the top-3 entries by score.

**Why keyword overlap (vs. embeddings)?**

- No embedding server or vector database is required — the chatbot runs entirely with a JSON file and the Claude API.
- Etiquette questions are domain-specific and highly predictable (shoe removal, head covering, Langar diet). The keyword vocabulary maps well to the KB, so cosine similarity over embeddings adds complexity without meaningful recall improvement for this use case.
- Zero external dependencies makes the system easy for teachers and students to understand, run, and modify.

---

## 5. Example Conversations

### Easy Conversation

> **Visitor:** Do I need to take my shoes off?
>
> **Bot:** Yes, all footwear must be removed before entering the Gurdwara.
> There are shoe racks outside the main entrance. This is a sign of humility
> and respect for this sacred space — in Punjabi, we sometimes call it the
> *pavan dargah* (the holy court of the Guru). The sangat looks forward to
> welcoming you!

*Why it works:* The keyword "shoes" maps directly to entry #2. The bot answers
concisely, adds cultural color (*pavan dargah*), and closes warmly.

---

### Tricky Conversation

> **Visitor:** My grandmother is elderly and cannot sit on the floor easily.
> Are there any accommodations in the Langar hall?
>
> **Bot:** That's a thoughtful question. The Langar hall traditionally practices
> *pangat* — sitting together on the floor in rows as a symbol of equality.
> However, my knowledge base doesn't contain specific information about
> accessibility accommodations at Fremont Gurdwara Sahib.
>
> I'd recommend contacting the Gurdwara office directly before your visit so
> they can help make arrangements for your grandmother. Gurdwaras are deeply
> committed to ensuring every member of the *sangat* (community) can
> participate comfortably. Waheguru Ji Ka Khalsa, Waheguru Ji Ki Fateh!

*Why it works:* No KB entry covers accessibility. The bot transparently
acknowledges the gap, redirects to the Gurdwara office, and maintains a warm
tone — it does *not* guess or invent a policy.

---

## 6. Why RAG Is Better Than a Standalone LLM Here

| Without RAG | With RAG |
|---|---|
| May generate plausible-sounding but wrong details about Fremont Gurdwara Sahib specifically | Answers are grounded in verified KB entries |
| Tone may be generic | System prompt enforces warm, culturally appropriate tone |
| Cannot reflect Gurdwara-specific policies (e.g., local Langar schedule) | KB can be updated by Gurdwara staff without retraining a model |
| May confidently answer questions it doesn't know | Explicit uncertainty behavior redirects gracefully |

The knowledge base (JSON file) acts like a curated Google Sheet: Gurdwara staff
or teachers can add, edit, or remove entries without touching any code — only
the JSON needs updating.

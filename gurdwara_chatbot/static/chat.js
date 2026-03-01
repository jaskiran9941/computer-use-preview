/**
 * Fremont Gurdwara Sahib Chatbot – Frontend
 *
 * Handles:
 *  - Message sending / receiving via /api/chat
 *  - Multi-turn session management (session_id in localStorage)
 *  - Typing indicator animation
 *  - FAQ sidebar population from /api/faq
 *  - FAQ click-to-ask shortcut
 *  - New Chat / reset flow
 */

(function () {
  "use strict";

  // ── DOM refs ────────────────────────────────────────────────────────────
  const form        = document.getElementById("chat-form");
  const input       = document.getElementById("user-input");
  const sendBtn     = document.getElementById("send-btn");
  const chatWindow  = document.getElementById("chat-window");
  const faqPanel    = document.getElementById("faq-panel");
  const faqToggle   = document.getElementById("faq-toggle");
  const faqClose    = document.getElementById("faq-close");
  const faqCats     = document.getElementById("faq-categories");
  const appWrapper  = document.getElementById("app-wrapper");
  const resetBtn    = document.getElementById("reset-btn");

  // ── Session ID ──────────────────────────────────────────────────────────
  function getSessionId() {
    let id = localStorage.getItem("gurdwara_session");
    if (!id) {
      id = "sess_" + Math.random().toString(36).slice(2, 10);
      localStorage.setItem("gurdwara_session", id);
    }
    return id;
  }
  let SESSION_ID = getSessionId();

  // ── FAQ Sidebar ─────────────────────────────────────────────────────────
  faqToggle.addEventListener("click", () => {
    faqPanel.classList.toggle("open");
    appWrapper.classList.toggle("faq-open");
  });
  faqClose.addEventListener("click", () => {
    faqPanel.classList.remove("open");
    appWrapper.classList.remove("faq-open");
  });

  async function loadFAQ() {
    try {
      const res = await fetch("/api/faq");
      const grouped = await res.json();
      faqCats.innerHTML = "";
      for (const [category, items] of Object.entries(grouped)) {
        const section = document.createElement("div");
        const title = document.createElement("div");
        title.className = "faq-category-title";
        title.textContent = category;
        section.appendChild(title);
        items.forEach((item) => {
          const btn = document.createElement("div");
          btn.className = "faq-item";
          btn.textContent = item.question;
          btn.addEventListener("click", () => {
            input.value = item.question;
            // close sidebar on mobile
            if (window.innerWidth < 600) {
              faqPanel.classList.remove("open");
              appWrapper.classList.remove("faq-open");
            }
            input.focus();
          });
          section.appendChild(btn);
        });
        faqCats.appendChild(section);
      }
    } catch (err) {
      faqCats.innerHTML = `<p class="loading-text">Could not load FAQs.</p>`;
    }
  }
  loadFAQ();

  // ── Message rendering ────────────────────────────────────────────────────
  function appendMessage(role, text, sources) {
    const msg = document.createElement("div");
    msg.className = `message ${role === "user" ? "user-message" : "bot-message"}`;

    const avatar = document.createElement("div");
    avatar.className = `avatar ${role === "user" ? "user-avatar" : "bot-avatar"}`;
    avatar.textContent = role === "user" ? "You" : "☬";

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    // Convert newlines to paragraphs
    const paragraphs = text.split(/\n\n+/);
    paragraphs.forEach((para) => {
      if (!para.trim()) return;
      const p = document.createElement("p");
      p.innerHTML = para.trim().replace(/\n/g, "<br />");
      bubble.appendChild(p);
    });

    // Source chips (bot only)
    if (role === "bot" && sources && sources.length > 0) {
      const badge = document.createElement("div");
      badge.className = "sources-badge";
      sources.forEach((s) => {
        const chip = document.createElement("span");
        chip.className = "source-chip";
        chip.textContent = s.category;
        badge.appendChild(chip);
      });
      bubble.appendChild(badge);
    }

    msg.appendChild(avatar);
    msg.appendChild(bubble);
    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return msg;
  }

  function showTyping() {
    const msg = document.createElement("div");
    msg.className = "message bot-message typing-indicator";
    msg.id = "typing";
    const avatar = document.createElement("div");
    avatar.className = "avatar bot-avatar";
    avatar.textContent = "☬";
    const bubble = document.createElement("div");
    bubble.className = "bubble";
    [1, 2, 3].forEach(() => {
      const dot = document.createElement("span");
      dot.className = "dot";
      bubble.appendChild(dot);
    });
    msg.appendChild(avatar);
    msg.appendChild(bubble);
    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return msg;
  }

  function removeTyping() {
    const el = document.getElementById("typing");
    if (el) el.remove();
  }

  // ── Chat submission ──────────────────────────────────────────────────────
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = input.value.trim();
    if (!query) return;

    input.value = "";
    input.disabled = true;
    sendBtn.disabled = true;

    appendMessage("user", query);
    const typing = showTyping();

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: query, session_id: SESSION_ID }),
      });
      const data = await res.json();
      removeTyping();

      if (data.error) {
        appendMessage("bot", "I'm sorry, something went wrong. Please try again.", []);
      } else {
        appendMessage("bot", data.answer, data.sources || []);
      }
    } catch (err) {
      removeTyping();
      appendMessage(
        "bot",
        "I'm unable to connect right now. Please check your connection or contact the Gurdwara office directly. Waheguru Ji Ka Khalsa, Waheguru Ji Ki Fateh!",
        []
      );
    } finally {
      input.disabled = false;
      sendBtn.disabled = false;
      input.focus();
    }
  });

  // ── New Chat / Reset ──────────────────────────────────────────────────────
  resetBtn.addEventListener("click", async () => {
    try {
      await fetch("/api/reset", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: SESSION_ID }),
      });
    } catch (_) {}

    // Generate new session
    SESSION_ID = "sess_" + Math.random().toString(36).slice(2, 10);
    localStorage.setItem("gurdwara_session", SESSION_ID);

    // Clear chat (keep welcome msg)
    chatWindow.innerHTML = "";
    const welcome = document.createElement("div");
    welcome.className = "message bot-message";
    welcome.innerHTML = `
      <div class="avatar bot-avatar">☬</div>
      <div class="bubble">
        <p><strong>Waheguru Ji Ka Khalsa, Waheguru Ji Ki Fateh!</strong></p>
        <p>Starting a fresh conversation. How can I help you today?</p>
      </div>`;
    chatWindow.appendChild(welcome);
    input.focus();
  });

  // ── Auto-focus ────────────────────────────────────────────────────────────
  input.focus();
})();

async function sendPrompt() {
    const promptBox = document.getElementById("prompt");
    const chatBox = document.getElementById("chat-box");
    const promptText = promptBox.value.trim();

    if (!promptText) return;

    // 🔹 Add User Message
    const userDiv = document.createElement("div");
    userDiv.className = "message user";
    userDiv.innerHTML = `<div class="bubble">${promptText}</div>`;
    chatBox.appendChild(userDiv);

    // 🔹 Add Thinking Bubble
    const thinkingDiv = document.createElement("div");
    thinkingDiv.className = "message bot";
    thinkingDiv.id = "thinking";
    thinkingDiv.innerHTML = `<div class="bubble">BonBon is thinking...</div>`;
    chatBox.appendChild(thinkingDiv);

    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("/solve", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: promptText })
        });

        const data = await response.json();

        // Remove thinking
        const thinking = document.getElementById("thinking");
        if (thinking) thinking.remove();

        if (!data || !data.content) {
            const errDiv = document.createElement("div");
            errDiv.className = "message bot";
            errDiv.innerHTML = `<div class="bubble">Error: ${JSON.stringify(data)}</div>`;
            chatBox.appendChild(errDiv);
            return;
        }

        // 🔹 Convert Markdown → HTML
        const renderedContent = marked.parse(data.content);

        // 🔹 Build RAG badge if RAG was used
        let ragHTML = "";
        if (data.rag_used && data.rag_topics && data.rag_topics.length > 0) {
            const chips = data.rag_topics
                .map(topic => `<span class="rag-chip">${topic}</span>`)
                .join("");
            ragHTML = `
                <div class="rag-bar">
                    <span class="rag-badge">⚡ RAG</span>
                    ${chips}
                </div>
            `;
        }

        // 🔹 Build metrics bar for DSA mode
        let metricsHTML = "";
        if (data.type === "code") {
            metricsHTML = `
                <div class="metrics-bar">
                    <span>Mode: ${data.mode || "N/A"}</span>
                    <span>Time: ${data.time || 0}s</span>
                    <span>Repairs: ${data.repairs || 0}</span>
                </div>
            `;
        }

        // 🔹 Append bot response using appendChild
        const msgDiv = document.createElement("div");
        msgDiv.className = "message bot markdown";
        msgDiv.innerHTML = `
            <div class="bubble">
                ${renderedContent}
                ${metricsHTML}
                ${ragHTML}
            </div>
        `;
        chatBox.appendChild(msgDiv);

        // 🔹 Syntax Highlighting
        if (window.hljs) {
            document.querySelectorAll("pre code").forEach((block) => {
                window.hljs.highlightElement(block);
            });
        }

    } catch (err) {
        const thinking = document.getElementById("thinking");
        if (thinking) thinking.remove();

        const errDiv = document.createElement("div");
        errDiv.className = "message bot";
        errDiv.innerHTML = `<div class="bubble">Connection Error: ${err}</div>`;
        chatBox.appendChild(errDiv);
    }

    promptBox.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;
}

// 🔹 Enter to Send (Shift+Enter = new line)
document.getElementById("prompt").addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendPrompt();
    }
});
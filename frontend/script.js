async function sendPrompt() {
    const promptBox = document.getElementById("prompt");
    const chatBox = document.getElementById("chat-box");
    const promptText = promptBox.value.trim();

    if (!promptText) return;

    // 🔹 Add User Message
    chatBox.innerHTML += `
        <div class="message user">
            <div class="bubble">
                ${promptText}
            </div>
        </div>
    `;

    // 🔹 Add Thinking Bubble
    chatBox.innerHTML += `
        <div class="message bot" id="thinking">
            <div class="bubble">
                BonBon is thinking...
            </div>
        </div>
    `;

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
            chatBox.innerHTML += `
                <div class="message bot">
                    <div class="bubble">
                        Error: ${JSON.stringify(data)}
                    </div>
                </div>
            `;
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

        chatBox.innerHTML += `
            <div class="message bot markdown">
                <div class="bubble">
                    ${renderedContent}
                    ${metricsHTML}
                    ${ragHTML}
                </div>
            </div>
        `;

        // 🔹 Syntax Highlighting
        if (window.hljs) {
            document.querySelectorAll("pre code").forEach((block) => {
                window.hljs.highlightElement(block);
            });
        }

    } catch (err) {
        const thinking = document.getElementById("thinking");
        if (thinking) thinking.remove();

        chatBox.innerHTML += `
            <div class="message bot">
                <div class="bubble">
                    Connection Error: ${err}
                </div>
            </div>
        `;
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
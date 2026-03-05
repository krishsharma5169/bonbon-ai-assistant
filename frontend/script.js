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

        chatBox.innerHTML += `
            <div class="message bot markdown">
                <div class="bubble">
                    ${renderedContent}
                    ${data.type === "code" ? `
                    <div style="margin-top:12px;font-size:12px;opacity:0.7;">
                        Mode: ${data.mode || "N/A"} |
                        Time: ${data.time || 0}s |
                        Repairs: ${data.repairs || 0}
                    </div>` : ""}
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
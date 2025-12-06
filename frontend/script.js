const API_URL = "http://127.0.0.1:8000";

// -----------------
// Convert function
// -----------------
async function convert() {
    const r = await fetch("http://127.0.0.1:8000/convert/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            source: src.value,
            target: dst.value,
            value: valueInput.value
        })
    });

    const data = await r.json();

    if (data.error) {
        convert_result.innerHTML = `<span style="color:red">❌ ${data.error}</span>`;
        return;
    }

    convert_result.innerHTML = `
        <div>
            <strong>Input:</strong> ${data.input} <br>
            <strong>From (${data.source_system}):</strong> ${data.input} <br>
            <strong>To (${data.target_system}):</strong> ${data.result}
        </div>
    `;
}


// -----------------
// Explain conversion
// -----------------
async function explainConversion() {
    const src = document.getElementById("src").value;
    const dst = document.getElementById("dst").value;
    const value = document.getElementById("value").value;

    const res = await fetch(`${API_URL}/explain/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ src_system: src, dst_system: dst, value })
    });

    const data = await res.json();
    document.getElementById("explain").innerText = data.steps.join("\n");
}

// -----------------
// Puzzle generate
// -----------------
async function getPuzzle() {
    const res = await fetch(`${API_URL}/puzzle/`);
    const data = await res.json();

    document.getElementById("puzzle-question").innerText = data.question;
    window.currentPuzzleAnswer = data.answer;
}

// -----------------
// Puzzle check
// -----------------
function checkPuzzle() {
    const user = document.getElementById("puzzle-input").value;

    if (user.trim() === window.currentPuzzleAnswer.trim()) {
        alert("Correct!");
    } else {
        alert("Incorrect. Try again!");
    }
}

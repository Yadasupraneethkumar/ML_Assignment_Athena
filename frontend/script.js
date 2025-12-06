const API_URL = "http://127.0.0.1:8000";

// -----------------
// Convert
// -----------------
async function convert() {
    const srcSystem = document.getElementById("src").value;
    const dstSystem = document.getElementById("dst").value;
    const rawValue = document.getElementById("valueInput").value;

    try {
        // Conversion to target
        const res = await fetch(`${API_URL}/convert/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                source: srcSystem,
                target: dstSystem,
                value: rawValue
            })
        });
        const data = await res.json();
        if (data.error) {
            convert_result.innerHTML = `<span style='color:red'>❌ ${data.error}</span>`;
            return;
        }

        // Conversion to Arabic for source display
        const resArabic = await fetch(`${API_URL}/convert/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                source: srcSystem,
                target: "arabic",
                value: rawValue
            })
        });
        const arabicData = await resArabic.json();
        const arabicValue = arabicData.result;

        convert_result.innerHTML = `
🟦 <strong>Input:</strong> ${rawValue}
🟩 <strong>Source (${srcSystem} → arabic):</strong> ${arabicValue}
🟨 <strong>Target (${dstSystem}):</strong> ${data.result}
        `;
    } catch (e) {
        convert_result.innerHTML = `<span style='color:red'>❌ ${e}</span>`;
    }
}

// -----------------
// Explain
// -----------------
async function explain() {
    const srcSystem = document.getElementById("ex_src").value;
    const dstSystem = document.getElementById("ex_dst").value;
    const rawValue = document.getElementById("ex_value").value;

    try {
        const res = await fetch(`${API_URL}/explain/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                source: srcSystem,
                target: dstSystem,
                value: rawValue
            })
        });
        const data = await res.json();

        if (data.error) {
            explain_result.innerHTML = `<span style="color:red">❌ ${data.error}</span>`;
            return;
        }

        explain_result.innerHTML = data.steps.join("<br>");
    } catch (e) {
        explain_result.innerHTML = `<span style='color:red'>❌ ${e}</span>`;
    }
}

// -----------------
// Puzzle
// -----------------
let puzzle_id = null;

async function getPuzzle() {
    try {
        const res = await fetch(`${API_URL}/puzzle/`);
        const data = await res.json();
        puzzle_id = data.puzzle_id;
        puzzle_question.textContent = "🧩 Puzzle: " + data.question;
    } catch (e) {
        puzzle_question.textContent = "❌ " + e;
    }
}

async function checkPuzzle() {
    const user = document.getElementById("puzzle_answer").value;
    try {
        const res = await fetch(`${API_URL}/puzzle/check`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ puzzle_id, answer: user })
        });
        const data = await res.json();
        puzzle_result.textContent = data.message;
    } catch (e) {
        puzzle_result.textContent = "❌ " + e;
    }
}

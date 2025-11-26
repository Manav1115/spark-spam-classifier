async function analyze() {
    const text = document.getElementById("text").value;

    const response = await fetch("http://10.198.228.48:5000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    const result = await response.json();
    document.getElementById("result").innerText =
        `Sentiment: ${result.sentiment}  | Score: ${result.score}`;
}

document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    const res = await fetch("/analyze", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    document.getElementById("result").innerHTML = `
        <h3>Skin Tone RGB: ${data.skin_rgb}</h3>
        <pre>${data.recommendation}</pre>
    `;
});
// api/prediction.js
export default async function handler(req, res) {
    // Aapki Gemini Key jo aapne code mein hi rakhne ko kaha
    const GEMINI_KEY = "AIzaSyD-WE7SdSUYHQGHtF9NJDvEaM8tVWFVrLk";
    const WINGO_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json?pageSize=10";

    try {
        // Step 1: Wingo API se data lena (Server-side fetch mein CORS ka masla nahi aata)
        const wingoRes = await fetch(WINGO_URL + "&ts=" + Date.now());
        const wingoData = await wingoRes.json();
        const history = wingoData.data.list;

        // Step 2: Gemini Prompt taiyar karna
        const prompt = `Analyze these 10 Wingo results: ${JSON.stringify(history)}. Predict next BIG/SMALL and 2 jackpot numbers. JSON format ONLY: {"p":"BIG/SMALL","n":[x,y],"c":"95%"}`;
        
        const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_KEY}`;
        
        const geminiRes = await fetch(geminiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
        });

        const geminiData = await geminiRes.json();
        const aiText = geminiData.candidates[0].content.parts[0].text;
        const prediction = JSON.parse(aiText.replace(/```json|```/g, ""));

        // Step 3: Result wapas bhejna
        res.status(200).json({ prediction, latestIssue: history[0].issueNumber });
    } catch (error) {
        res.status(500).json({ error: "API Error", message: error.message });
    }
}

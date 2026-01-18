// api/prediction.js
export default async function handler(req, res) {
    const GEMINI_KEY = "AIzaSyBHMDf4_A_3W_xQ_1nvAfc5m0nZNP2io6A";
    const WINGO_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json?pageSize=10";

    try {
        console.log("FETCHING WINGO DATA...");
        const wingoRes = await fetch(WINGO_URL + "&ts=" + Date.now());
        const wingoData = await wingoRes.json();

        if (!wingoData || !wingoData.data || !wingoData.data.list) {
            throw new Error("Wingo API returned invalid data");
        }

        const history = wingoData.data.list;
        console.log("WINGO DATA SUCCESS. CALLING GEMINI...");

        const prompt = `Wingo 1M History: ${JSON.stringify(history)}. Predict next BIG/SMALL and 2 jackpot numbers. Response format JSON ONLY: {"p":"BIG/SMALL","n":[x,y],"c":"95%"}`;
        const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_KEY}`;
        
        const geminiRes = await fetch(geminiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
        });

        const geminiJson = await geminiRes.json();
        
        if (geminiJson.error) {
            console.error("GEMINI ERROR:", geminiJson.error.message);
            return res.status(500).json({ error: geminiJson.error.message });
        }

        const aiText = geminiJson.candidates[0].content.parts[0].text;
        const prediction = JSON.parse(aiText.replace(/```json|```/g, ""));

        console.log("PREDICTION SUCCESSFUL");
        res.status(200).json({ prediction, latestIssue: history[0].issueNumber });

    } catch (error) {
        console.error("SERVER CRASHED:", error.message);
        res.status(500).json({ error: "Server Error", details: error.message });
    }
}

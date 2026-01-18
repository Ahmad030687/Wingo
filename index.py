<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Supreme v16 | Ahmad Ali Singularity</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root { --gold: #FFD700; --cyan: #00f3ff; }
        body { background: radial-gradient(circle, #0a0a20 0%, #000 100%); font-family: 'Rajdhani', sans-serif; color: #fff; min-height: 100vh; display: flex; justify-content: center; align-items: center; margin: 0; }
        .panel { width: 440px; background: rgba(5, 5, 15, 0.98); border: 1px solid rgba(255, 215, 0, 0.4); border-radius: 40px; padding: 30px; position: relative; box-shadow: 0 0 100px #000; }
        .gold-glow { font-family: 'Orbitron'; color: var(--gold); text-shadow: 0 0 20px var(--gold); }
        .j-box { width: 75px; height: 75px; background: #000; border: 2px solid var(--gold); border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; font-weight: 900; color: var(--gold); box-shadow: inset 0 0 15px rgba(255,215,0,0.2); }
        #console { height: 150px; overflow-y: auto; font-size: 10px; font-family: monospace; border-top: 1px solid #333; padding-top: 10px; color: #777; scroll-behavior: smooth; }
        .btn-neural { background: linear-gradient(90deg, #b8860b, #ffd700); color: #000; font-weight: 900; letter-spacing: 2px; transition: 0.3s; }
        .btn-neural:hover { transform: scale(1.02); box-shadow: 0 0 20px var(--gold); }
    </style>
</head>
<body>

    <div class="panel">
        <div class="flex justify-between items-start mb-8">
            <div>
                <h1 class="text-[10px] tracking-[5px] text-gray-500 font-bold uppercase">Universal AI Sniper</h1>
                <div class="flex items-center gap-2 mt-1">
                    <span id="ai-pulse" class="w-2 h-2 rounded-full bg-red-600 animate-pulse"></span>
                    <span id="ai-status" class="text-[10px] text-red-500 font-bold tracking-widest uppercase">Kernel Offline</span>
                </div>
            </div>
            <div class="text-right">
                <p class="gold-glow text-2xl font-black">V.MAX</p>
                <p class="text-[8px] text-gray-500 tracking-widest uppercase">Ahmad Ali Singularity</p>
            </div>
        </div>

        <div class="bg-white/5 p-8 rounded-[40px] border border-white/10 text-center mb-6 shadow-inner relative overflow-hidden">
            <p class="text-[11px] tracking-[6px] text-gray-400 uppercase mb-4">Neural Jackpot Result</p>
            <h2 class="text-7xl font-bold italic gold-glow" id="main-val">--</h2>
            
            <div class="mt-8 flex justify-center gap-8">
                <div class="flex flex-col items-center"><div class="j-box" id="n1">?</div><p class="text-[9px] text-gray-500 mt-2 font-bold uppercase">Primary</p></div>
                <div class="flex flex-col items-center"><div class="j-box" id="n2" style="border-color: var(--cyan); color: var(--cyan);">?</div><p class="text-[9px] text-gray-500 mt-2 font-bold uppercase">Mirror</p></div>
            </div>
        </div>

        <div class="grid grid-cols-2 gap-4 mb-6 text-center">
            <div class="bg-black/50 p-4 rounded-3xl border-b-2 border-yellow-500">
                <p class="text-[10px] text-gray-500 uppercase font-black">Period ID</p>
                <p class="text-lg font-bold text-gray-200" id="issue-id">#-----</p>
            </div>
            <div class="bg-black/50 p-4 rounded-3xl border-b-2 border-cyan-500">
                <p class="text-[10px] text-gray-500 uppercase font-black">Confidence</p>
                <p class="text-lg font-bold text-cyan-400" id="conf">0%</p>
            </div>
        </div>

        <button onclick="manualSync()" class="w-full btn-neural py-4 rounded-2xl mb-6 uppercase text-sm">Force Neural Scan</button>

        <div>
            <p class="text-[10px] text-gray-600 font-bold tracking-[4px] mb-3 uppercase">Activity Monitor</p>
            <div id="console">
                <div>[SYSTEM]: Bot Loaded. Awaiting market transition...</div>
            </div>
        </div>
    </div>

    <script>
        const GEMINI_KEY = "AIzaSyD-WE7SdSUYHQGHtF9NJDvEaM8tVWFVrLk";
        const WINGO_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json?pageSize=10";
        const PROXY = "https://api.allorigins.win/raw?url=";
        let lastIssue = null;

        function log(msg, cls = "text-gray-500") {
            const con = document.getElementById('console');
            const time = new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit', second:'2-digit'});
            con.innerHTML = `<div class="mb-1 ${cls}"><span class="opacity-40">[${time}]</span> > ${msg}</div>` + con.innerHTML;
        }

        async function manualSync() {
            log("INITIALIZING: Forcing Quantum Scan...", "text-blue-400");
            await runEngine();
        }

        async function runEngine() {
            try {
                // Step 1: Fetch Wingo Data using Proxy
                const fetchUrl = PROXY + encodeURIComponent(WINGO_URL + "&ts=" + Date.now());
                const res = await fetch(fetchUrl);
                const data = await res.json();
                const history = data.data.list;
                const latest = history[0];

                if (lastIssue !== latest.issueNumber) {
                    lastIssue = latest.issueNumber;
                    log(`SYNC: Data captured for #${latest.issueNumber.slice(-4)}. Analyzing...`, "text-yellow-500");
                    
                    // Step 2: Prediction via Gemini
                    const aiResult = await askGemini(history);
                    if (aiResult) {
                        updateHUD(aiResult, latest.issueNumber);
                        log("SUCCESS: Prediction locked. Level 1 ready.", "text-green-500 font-bold");
                    }
                } else {
                    log("IDLE: Period unchanged. System in standby.");
                }
            } catch (err) {
                log("NETWORK: Handshake failed. Retrying in next cycle...", "text-red-500");
            }
        }

        async function askGemini(history) {
            const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_KEY}`;
            const prompt = `Act as an Elite Pattern Decoder. Analyze these 10 Wingo rounds: ${JSON.stringify(history)}. Predict the NEXT outcome (BIG or SMALL) and the two most likely Jackpot Numbers (0-9). Format: JSON ONLY {"p":"BIG/SMALL","n":[num1,num2],"c":"95%"}`;
            
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
                });

                const result = await response.json();
                if (result.error) {
                    log(`AI ERROR: ${result.error.message}`, "text-red-600");
                    return null;
                }

                const aiResponse = result.candidates[0].content.parts[0].text;
                const prediction = JSON.parse(aiResponse.replace(/```json|```/g, ""));
                
                // Update AI Status
                document.getElementById('ai-pulse').className = "w-2 h-2 rounded-full bg-green-500 shadow-[0_0_10px_#39ff14]";
                document.getElementById('ai-status').innerText = "AI ONLINE";
                document.getElementById('ai-status').className = "text-[10px] text-green-500 font-bold tracking-widest uppercase";
                
                return prediction;
            } catch (err) {
                log("AI LINK: Handshake rejected. Check Key/Rate Limit.", "text-red-500");
                return null;
            }
        }

        function updateHUD(data, issue) {
            const main = document.getElementById('main-val');
            main.innerText = data.p;
            main.className = `text-7xl font-bold italic gold-glow ${data.p === 'BIG' ? 'text-green-500' : 'text-red-600'}`;
            document.getElementById('n1').innerText = data.n[0];
            document.getElementById('n2').innerText = data.n[1];
            document.getElementById('conf').innerText = data.c;
            document.getElementById('issue-id').innerText = "#" + (BigInt(issue) + 1n).toString().slice(-5);
        }

        // 24/7 Automation Loop (Every 40 seconds to stay within Free Plan limits)
        setInterval(() => {
            const s = new Date().getSeconds();
            if (s === 2 || s === 40) runEngine();
        }, 1000);

        // First Boot
        runEngine();
    </script>
</body>
</html>

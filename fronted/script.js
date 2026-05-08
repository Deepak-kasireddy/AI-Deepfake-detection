const API_BASE = window.location.origin;

// Helper to safely format percentages
function safeFormat(value) {
    if (value === null || value === undefined) return "0";
    let num = parseFloat(value);
    if (isNaN(num)) return "0";
    // Convert 0-1 range to 0-100
    if (num <= 1 && num > 0) num = num * 100;
    return num.toFixed(1);
}

// Get Badge Class
function getBadgeClass(label) {
    const l = (label || "").toLowerCase();
    if (l.includes("authentic") || l.includes("real")) return "authentic";
    if (l.includes("suspicious")) return "suspicious";
    return "fake";
}

// DOM Elements
const dropZone = document.getElementById('drop-zone');
const imageInput = document.getElementById('image-input');
const preview = document.getElementById('preview');
const scanImageBtn = document.getElementById('scan-image-btn');
const scanTextBtn = document.getElementById('scan-text-btn');
const scanUrlBtn = document.getElementById('scan-url-btn');
const analyzeBtn = document.getElementById('analyze-btn');
const textInput = document.getElementById('text-input');
const urlInput = document.getElementById('url-input');
const resultDashboard = document.getElementById('result-dashboard');
const analysisOutput = document.getElementById('analysis-output');

// Image Selection
dropZone.addEventListener('click', () => imageInput.click());
dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('dragging'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragging'));
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragging');
    if (e.dataTransfer.files.length) {
        imageInput.files = e.dataTransfer.files;
        handleImageSelect(e.dataTransfer.files[0]);
    }
});

imageInput.addEventListener('change', (e) => {
    if (e.target.files[0]) handleImageSelect(e.target.files[0]);
});

function handleImageSelect(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        preview.src = e.target.result;
        preview.classList.remove('hidden');
        document.querySelector('.drop-zone-content').classList.add('hidden');
    };
    reader.readAsDataURL(file);
}

// Main Analysis Logic
async function performAnalysis(endpoint, body, isFormData = false) {
    try {
        const options = { method: 'POST', body: body };
        if (!isFormData) options.headers = { 'Content-Type': 'application/json' };

        const response = await fetch(`${API_BASE}${endpoint}`, options);
        if (!response.ok) throw new Error(`Server returned ${response.status}`);
        
        return await response.json();
    } catch (error) {
        console.error("Analysis Error:", error);
        return { error: error.message };
    }
}

function renderResult(data) {
    resultDashboard.classList.remove('hidden');
    
    if (data.error) {
        analysisOutput.innerHTML = `<div class="badge fake">Error: ${data.error}</div>`;
        return;
    }

    const badgeClass = getBadgeClass(data.label);
    
    analysisOutput.innerHTML = `
        <div class="summary-header">
            <div class="score-circle" style="border-color: var(--${badgeClass})">
                <span>${safeFormat(data.score)}%</span>
                <label>Authentic</label>
            </div>
            <div style="text-align: right">
                <div class="badge ${badgeClass}">${data.label}</div>
                <p style="margin-top: 10px; color: var(--text-dim)">Analysis timestamp: ${new Date().toLocaleTimeString()}</p>
            </div>
        </div>

        <div class="analysis-description">
            <p>${data.summary || "No description available."}</p>
        </div>

        <div class="highlights-title">✦ Detailed Insights & Highlights</div>
        <ul class="highlight-list">
            ${(data.insights || ["No specific insights available."]).map(insight => `
                <li class="highlight-item">${insight}</li>
            `).join('')}
        </ul>

        <div class="detail-grid" style="margin-top: 2rem;">
            <div class="detail-card">
                <h4>Visual Forensics</h4>
                <div style="font-size: 1.2rem; font-weight: 600;">${data.image?.result || "N/A"}</div>
                <div class="detail-progress-bg">
                    <div class="detail-progress-fill" style="width: ${safeFormat(data.image?.confidence)}%"></div>
                </div>
                <small>${safeFormat(data.image?.confidence)}% probability</small>
            </div>

            <div class="detail-card">
                <h4>Linguistic Analysis</h4>
                <div style="font-size: 1.2rem; font-weight: 600;">${data.text?.result || "N/A"}</div>
                <div class="detail-progress-bg">
                    <div class="detail-progress-fill" style="width: ${safeFormat(data.text?.confidence)}%"></div>
                </div>
                <small>${safeFormat(data.text?.confidence)}% confidence</small>
            </div>

            <div class="detail-card">
                <h4>Source Credibility</h4>
                <div style="font-size: 1.2rem; font-weight: 600;">${data.source?.status || "Unknown"}</div>
                <div class="detail-progress-bg">
                    <div class="detail-progress-fill" style="width: ${data.source?.score || 0}%"></div>
                </div>
                <small>Trust Score: ${data.source?.score || 0}/100</small>
            </div>
        </div>

        ${data.text?.sources && data.text.sources.length > 0 ? `
        <div style="margin-top: 2rem;">
            <div class="highlights-title">🔗 Corroborating Sources</div>
            <ul style="list-style: none; padding-left: 0;">
                ${data.text.sources.map(s => `
                    <li style="margin-bottom: 8px;">
                        <a href="${s.url}" target="_blank" style="color: var(--primary); text-decoration: none;">➜ ${s.name}</a>
                    </li>
                `).join('')}
            </ul>
        </div>` : ''}
    `;
    
    // Smooth scroll to results
    resultDashboard.scrollIntoView({ behavior: 'smooth' });
}

// Event Listeners
analyzeBtn.addEventListener('click', async () => {
    const file = imageInput.files[0];
    const text = textInput.value.trim();
    const url = urlInput.value.trim();

    if (!file && !text && !url) {
        alert("Please provide at least one input (image, text, or URL).");
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Processing Neural Layers...";

    const formData = new FormData();
    if (file) formData.append('image', file);
    if (text) formData.append('text', text);
    if (url) formData.append('url', url);

    const result = await performAnalysis('/analyze', formData, true);
    renderResult(result);

    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Run Full Neural Analysis";
});

// Single scanners (re-use the render logic for consistency)
scanImageBtn.addEventListener('click', async () => {
    if (!imageInput.files[0]) return alert("Select image first");
    scanImageBtn.disabled = true;
    const formData = new FormData();
    formData.append('file', imageInput.files[0]);
    const result = await performAnalysis('/predict/image', formData, true);
    // Wrap single result in aggregator-like structure for the renderer
    renderResult({
        score: result.confidence * 100,
        label: result.result === "Real" ? "Authentic" : "Likely Fake",
        summary: `Visual analysis of the uploaded media indicates ${result.result.toLowerCase()} patterns.`,
        insights: result.issues || [],
        image: result
    });
    scanImageBtn.disabled = false;
});

scanTextBtn.addEventListener('click', async () => {
    if (!textInput.value.trim()) return alert("Enter text first");
    scanTextBtn.disabled = true;
    const result = await performAnalysis('/predict/text', JSON.stringify({ text: textInput.value.trim() }));
    renderResult({
        score: result.confidence * 100,
        label: result.result === "Real" ? "Authentic" : "Likely Fake",
        summary: `Linguistic analysis of the provided text suggests ${result.result.toLowerCase()} characteristics.`,
        insights: result.issues || [],
        text: result
    });
    scanTextBtn.disabled = false;
});

scanUrlBtn.addEventListener('click', async () => {
    if (!urlInput.value.trim()) return alert("Enter URL first");
    scanUrlBtn.disabled = true;
    const result = await performAnalysis('/check/source', JSON.stringify({ url: urlInput.value.trim() }));
    renderResult({
        score: result.score,
        label: result.score > 70 ? "Authentic" : "Suspicious",
        summary: `The source domain "${urlInput.value}" has a trust score of ${result.score}/100.`,
        insights: [result.status],
        source: result
    });
    scanUrlBtn.disabled = false;
});

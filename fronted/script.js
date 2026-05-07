const API_BASE = window.location.origin;

// Helper to safely format percentages and handle NaN/null/undefined
function safeFormat(value) {
    if (value === null || value === undefined) return "0.00";
    let num = parseFloat(value);
    if (isNaN(num) || !isFinite(num)) return "0.00";
    // If the value is already likely a percentage (e.g. 85.5) and not a probability (0-1)
    // but the code expects probability, we should be careful.
    // However, the current backend returns probabilities (0-1).
    return (num * 100).toFixed(2);
}

// DOM Elements
const dropZone = document.getElementById('drop-zone');
const imageInput = document.getElementById('image-input');
const preview = document.getElementById('preview');
const scanImageBtn = document.getElementById('scan-image-btn');
const imageResult = document.getElementById('image-result');
const imageLabel = document.getElementById('image-label');
const imageConfidence = document.getElementById('image-confidence');
const imageProgress = document.getElementById('image-progress');

const textInput = document.getElementById('text-input');
const scanTextBtn = document.getElementById('scan-text-btn');
const textResult = document.getElementById('text-result');
const textLabel = document.getElementById('text-label');
const textConfidence = document.getElementById('text-confidence');
const textProgress = document.getElementById('text-progress');
const textSourcesContainer = document.getElementById('text-sources-container');
const textSourcesList = document.getElementById('text-sources-list');

const urlInput = document.getElementById('url-input');
const scanUrlBtn = document.getElementById('scan-url-btn');
const urlResult = document.getElementById('url-result');
const urlStatus = document.getElementById('url-status');
const urlScore = document.getElementById('url-score');

const analyzeBtn = document.getElementById('analyze-btn');
const output = document.getElementById('output');

// Image Upload Logic
dropZone.addEventListener('click', () => imageInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragging');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragging');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragging');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        imageInput.files = files;
        handleImageSelect(files[0]);
    }
});

imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleImageSelect(file);
    }
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

// Scan Image
scanImageBtn.addEventListener('click', async () => {
    const file = imageInput.files[0];
    if (!file) {
        alert("Please select an image first.");
        return;
    }

    scanImageBtn.textContent = "Analyzing...";
    scanImageBtn.disabled = true;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE}/predict/image`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            imageLabel.textContent = "Error";
            imageConfidence.textContent = "0.00";
            imageProgress.style.width = '0%';
            alert("Image Analysis Error:\n" + data.error + (data.traceback ? "\n\nTraceback:\n" + data.traceback : ""));
        } else {
            imageLabel.textContent = data.result;
            imageConfidence.textContent = safeFormat(data.confidence);
            imageProgress.style.width = (parseFloat(safeFormat(data.confidence)) || 0) + '%';
        }
        imageResult.classList.remove('hidden');

    } catch (error) {
        imageLabel.textContent = "Error";
        imageConfidence.textContent = "0.00";
        alert("System Error during image analysis:\n" + error.message);
        console.error(error);
    } finally {
        scanImageBtn.textContent = "Scan Image";
        scanImageBtn.disabled = false;
    }
});

// Scan Text
scanTextBtn.addEventListener('click', async () => {
    const text = textInput.value.trim();
    if (!text) {
        alert("Please enter text to analyze.");
        return;
    }

    scanTextBtn.textContent = "Analyzing...";
    scanTextBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/predict/text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            textLabel.textContent = "Error";
            textConfidence.textContent = "0.00";
            textProgress.style.width = '0%';
            alert("Text Analysis Error:\n" + data.error + (data.traceback ? "\n\nTraceback:\n" + data.traceback : ""));
        } else {
            textLabel.textContent = data.result;
            textConfidence.textContent = safeFormat(data.confidence);
            textProgress.style.width = (parseFloat(safeFormat(data.confidence)) || 0) + '%';
            
            // Display sources if available
            if (data.sources && data.sources.length > 0) {
                textSourcesList.innerHTML = data.sources.map(source => 
                    `<li><a href="${source.url}" target="_blank">${source.name}</a></li>`
                ).join('');
                textSourcesContainer.classList.remove('hidden');
            } else {
                textSourcesContainer.classList.add('hidden');
            }
        }
        textResult.classList.remove('hidden');

    } catch (error) {
        textLabel.textContent = "Error";
        textConfidence.textContent = "0.00";
        alert("System Error during text analysis:\n" + error.message);
        console.error(error);
    } finally {
        scanTextBtn.textContent = "Scan Text";
        scanTextBtn.disabled = false;
    }
});

// Check Source
scanUrlBtn.addEventListener('click', async () => {
    const url = urlInput.value.trim();
    if (!url) {
        alert("Please enter a URL.");
        return;
    }

    scanUrlBtn.textContent = "Checking...";
    scanUrlBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/check/source`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        urlStatus.textContent = data.status;
        let scoreVal = parseFloat(data.score);
        urlScore.textContent = isNaN(scoreVal) ? "0.00" : scoreVal.toFixed(2);
        urlResult.classList.remove('hidden');

    } catch (error) {
        alert("Error checking source: " + error.message);
        console.error(error);
    } finally {
        scanUrlBtn.textContent = "Check Source";
        scanUrlBtn.disabled = false;
    }
});

// Analyze All
analyzeBtn.addEventListener('click', async () => {
    const file = imageInput.files[0];
    const text = textInput.value.trim();
    const url = urlInput.value.trim();

    if (!file && !text && !url) {
        alert("Please provide at least one input (image, text, or URL).");
        return;
    }

    analyzeBtn.textContent = "Analyzing...";
    analyzeBtn.disabled = true;

    const formData = new FormData();
    if (file) formData.append('image', file);
    if (text) formData.append('text', text);
    if (url) formData.append('url', url);

    try {
        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            output.innerHTML = `<div class="error-box"><strong>Analysis Error:</strong> ${data.error}</div>`;
            alert("Analysis Error:\n" + data.error);
        } else {
            // Create a more readable output than just raw JSON
            output.innerHTML = `
                <div class="summary-box">
                    <h3>Overall Authenticity: ${safeFormat(data.score / 100)}%</h3>
                    <p class="status-label ${(data.label || 'Unknown').toLowerCase().replace(' ', '-')}">Result: ${data.label}</p>
                </div>
                <div class="details-grid">
                    <div class="detail-item"><strong>Image:</strong> ${data.image.result} (${safeFormat(data.image.confidence)}%)</div>
                    <div class="detail-item"><strong>Text:</strong> ${data.text.result} (${safeFormat(data.text.confidence)}%)</div>
                    <div class="detail-item"><strong>Source:</strong> ${data.source.status} (Score: ${parseFloat(data.source.score || 0).toFixed(2)})</div>
                </div>
                ${data.text.sources && data.text.sources.length > 0 ? `
                <div class="sources-summary">
                    <h4>Verified Sources:</h4>
                    <ul>
                        ${data.text.sources.map(s => `<li><a href="${s.url}" target="_blank">${s.name}</a></li>`).join('')}
                    </ul>
                </div>` : ''}
            `;
        }
        output.classList.remove('hidden');

    } catch (error) {
        alert("System Error during analysis:\n" + error.message);
        console.error(error);
    } finally {
        analyzeBtn.textContent = "Analyze All";
        analyzeBtn.disabled = false;
    }
});

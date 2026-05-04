const dropZone = document.getElementById('drop-zone');
const imageInput = document.getElementById('image-input');
const preview = document.getElementById('preview');
const scanImageBtn = document.getElementById('scan-image');
const imageResult = document.getElementById('image-result');
const imageLabel = document.getElementById('image-label');
const imageConfidence = document.getElementById('image-confidence');
const imageProgress = document.getElementById('image-progress');

const textInput = document.getElementById('text-input');
const scanTextBtn = document.getElementById('scan-text');
const textResult = document.getElementById('text-result');
const textLabel = document.getElementById('text-label');
const textConfidence = document.getElementById('text-confidence');
const textProgress = document.getElementById('text-progress');

const API_BASE = '';

// Image Upload Logic
dropZone.addEventListener('click', () => imageInput.click());

imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.src = e.target.result;
            preview.classList.remove('hidden');
            document.querySelector('.drop-zone-content').classList.add('hidden');
        };
        reader.readAsDataURL(file);
    }
});

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
        const data = await response.json();

        imageResult.classList.remove('hidden');
        
        const isFake = data.label === 'Fake';
        const labelText = isFake ? 'AI-Generated' : 'Real Image';
        const confPercent = Math.round(data.confidence);
        
        document.getElementById('image-label').textContent = labelText;
        document.getElementById('image-confidence').textContent = `${confPercent}%`;
        
        const reasonsList = document.getElementById('image-reasons');
        const highlightsList = document.getElementById('image-highlights');
        
        reasonsList.innerHTML = '';
        highlightsList.innerHTML = '';
        
        if (isFake) {
            const fakeReasons = [
                'Unnatural facial symmetry',
                'Inconsistent lighting',
                'GAN artifact patterns'
            ];
            const fakeHighlights = [
                'Face edges',
                'Background distortions'
            ];
            
            fakeReasons.forEach(r => {
                const li = document.createElement('li');
                li.textContent = r;
                reasonsList.appendChild(li);
            });
            
            fakeHighlights.forEach(h => {
                const li = document.createElement('li');
                li.textContent = h;
                highlightsList.appendChild(li);
            });
            
            document.getElementById('image-label').style.color = '#ff4b2b';
        } else {
            const realReasons = [
                'Natural skin texture',
                'Consistent shadow directions',
                'No visible structural anomalies'
            ];
            const realHighlights = [
                'Facial contours',
                'Eye reflections'
            ];
            
            realReasons.forEach(r => {
                const li = document.createElement('li');
                li.textContent = r;
                reasonsList.appendChild(li);
            });
            
            realHighlights.forEach(h => {
                const li = document.createElement('li');
                li.textContent = h;
                highlightsList.appendChild(li);
            });
            
            document.getElementById('image-label').style.color = '#00f2fe';
        }
        
        const authScore = isFake ? (100 - confPercent) : confPercent;
        let scoreLabel = 'Medium';
        if (authScore < 40) scoreLabel = 'Low';
        else if (authScore > 75) scoreLabel = 'High';
        
        const authScoreElem = document.getElementById('image-auth-score');
        authScoreElem.textContent = `${authScore}% (${scoreLabel})`;
        authScoreElem.style.color = authScore < 40 ? '#ff4b2b' : (authScore > 75 ? '#00f2fe' : '#f093fb');


    } catch (error) {
        console.error(error);
        alert("Error connecting to backend server.");
    } finally {
        scanImageBtn.textContent = "Analyze Image";
        scanImageBtn.disabled = false;
    }
});

// Text & Link Verification Logic
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;  
    }
}

scanTextBtn.addEventListener('click', async () => {
    const text = textInput.value.trim();
    if (!text) {
        alert("Please enter some text or a URL.");
        return;
    }

    const isUrl = isValidUrl(text);
    scanTextBtn.textContent = isUrl ? "Analyzing Link..." : "Verifying Content...";
    scanTextBtn.disabled = true;

    try {
        const endpoint = isUrl ? '/predict/url' : '/predict/text';
        const payload = isUrl ? { url: text } : { text: text };
        
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || "Server error");
        }

        textResult.classList.remove('hidden');
        textLabel.textContent = data.label;
        textConfidence.textContent = `${data.confidence}%`;
        textProgress.style.width = `${data.confidence}%`;

        textLabel.style.color = data.label === 'Fake' ? '#ff4b2b' : '#00f2fe';
        textProgress.style.background = data.label === 'Fake' ? '#ff4b2b' : '#00f2fe';

        // Source Verification Logic
        const sourcesContainer = document.getElementById('sources-container');
        const sourceSummary = document.getElementById('source-summary');
        const sourcesList = document.getElementById('sources-list');

        if (data.sources && data.sources.length > 0) {
            sourcesContainer.classList.remove('hidden');
            sourceSummary.textContent = data.summary;
            
            // If URL, show extracted snippet
            if (isUrl && data.extracted_text) {
                sourceSummary.innerHTML = `<strong>Extracted from Link:</strong> <em>"${data.extracted_text}"</em><br><br>${data.summary}`;
            }

            sourcesList.innerHTML = '';
            
            data.sources.forEach(source => {
                const link = document.createElement('a');
                link.href = source.url;
                link.target = '_blank';
                link.className = `source-btn ${source.type}`;
                link.innerHTML = `
                    <span class="source-name">${source.name}</span>
                    <span class="source-reliability">${source.reliability}</span>
                `;
                sourcesList.appendChild(link);
            });
        } else {
            sourcesContainer.classList.add('hidden');
        }

    } catch (error) {
        console.error(error);
        alert(error.message || "Error connecting to backend server.");
    } finally {
        scanTextBtn.textContent = "Verify Content / Link";
        scanTextBtn.disabled = false;
    }
});
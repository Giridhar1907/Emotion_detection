// TODO: Change this to your actual deployed backend URL (e.g., Hugging Face Spaces URL)
// For local development, use: "http://localhost:8000/analyze"
const BACKEND_URL = "https://your-space-name.hf.space/analyze"; // Update this after deployment

document.addEventListener('DOMContentLoaded', async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: getSelectionText,
    }, async (injectionResults) => {
        if (!injectionResults || injectionResults.length === 0) return;
        
        const selectedText = injectionResults[0].result;
        
        if (selectedText) {
            document.getElementById('no-selection').classList.add('hidden');
            
            const textElement = document.getElementById('selectedText');
            // Show truncated text if it's too long
            textElement.innerText = selectedText.length > 300 ? selectedText.substring(0, 300) + "..." : selectedText;
            document.getElementById('selection-card').classList.remove('hidden');
            document.getElementById('loading').classList.remove('hidden');

            try {
                const response = await fetch(BACKEND_URL, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ text: selectedText })
                });

                if (!response.ok) throw new Error("API Error");

                const data = await response.json();
                document.getElementById('loading').classList.add('hidden');
                document.getElementById('results').classList.remove('hidden');

                displayResults(data.overall_emotions);
                
            } catch (error) {
                document.getElementById('loading').classList.add('hidden');
                alert("Failed to connect to backend. Please ensure the backend is running and BACKEND_URL is correct.");
                console.error(error);
            }
        }
    });
});

function getSelectionText() {
    return window.getSelection().toString().trim();
}

let chartInstance = null;

function displayResults(emotions) {
    const listElement = document.getElementById('emotionList');
    listElement.innerHTML = '';

    const labels = [];
    const scores = [];

    emotions.forEach(e => {
        labels.push(e.label);
        scores.push((e.score * 100).toFixed(1));
        
        const item = document.createElement('div');
        item.className = 'emotion-item';
        
        const nameSpan = document.createElement('span');
        nameSpan.innerText = e.label;
        nameSpan.style.textTransform = 'capitalize';
        
        const scoreSpan = document.createElement('span');
        scoreSpan.innerText = `${(e.score * 100).toFixed(1)}%`;
        
        item.appendChild(nameSpan);
        item.appendChild(scoreSpan);
        listElement.appendChild(item);
    });

    renderChart(labels, scores);
}

function renderChart(labels, data) {
    const ctx = document.getElementById('emotionChart').getContext('2d');
    
    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Probability (%)',
                data: data,
                backgroundColor: [
                    'rgba(139, 92, 246, 0.7)',
                    'rgba(59, 130, 246, 0.7)',
                    'rgba(16, 185, 129, 0.7)',
                    'rgba(245, 158, 11, 0.7)',
                    'rgba(239, 68, 68, 0.7)'
                ],
                borderColor: [
                    'rgb(139, 92, 246)',
                    'rgb(59, 130, 246)',
                    'rgb(16, 185, 129)',
                    'rgb(245, 158, 11)',
                    'rgb(239, 68, 68)'
                ],
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: '#3f3f46' },
                    ticks: { color: '#a1a1aa' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#e4e4e7', font: { size: 10, textTransform: 'capitalize' } }
                }
            }
        }
    });
}
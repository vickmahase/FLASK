function runEmotionAnalysis() {
    const textToAnalyze = document.getElementById('textToAnalyze').value;
    const outputDiv = document.getElementById('output');

    if (!textToAnalyze.trim()) {
        outputDiv.textContent = 'Invalid text! Please try again!';
        return;
    }

    outputDiv.textContent = 'Analyzing...';

    fetch('/emotionDetector?textToAnalyze=' + encodeURIComponent(textToAnalyze))
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text); });
            }
            return response.text();
        })
        .then(data => {
            outputDiv.textContent = data;
        })
        .catch(error => {
            outputDiv.textContent = error.message || 'Invalid text! Please try again!';
        });
}

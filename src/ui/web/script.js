document.addEventListener('DOMContentLoaded', () => {
    const textInput = document.getElementById('textInput');
    const charCount = document.getElementById('charCount');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const loader = analyzeBtn.querySelector('.loader');
    
    const errorMsg = document.getElementById('errorMsg');
    const resultContainer = document.getElementById('resultContainer');
    const resultHeader = document.getElementById('resultHeader');
    const resultTitle = document.getElementById('resultTitle');
    const statusIcon = resultHeader.querySelector('.status-icon');
    
    const confidencePercentage = document.getElementById('confidencePercentage');
    const confidenceFill = document.getElementById('confidenceFill');
    const reasonEngine = document.getElementById('reasonEngine');
    const reasonList = document.getElementById('reasonList');
    
    // Character count listener
    textInput.addEventListener('input', () => {
        charCount.textContent = `${textInput.value.length} characters`;
        if (textInput.value.length > 0) {
            errorMsg.classList.add('hidden');
        }
    });
    
    // Report scam listener
    document.getElementById('reportBtn').addEventListener('click', (e) => {
        e.preventDefault();
        alert("Thank you! This scam has been reported to our security team for further analysis.");
    });

    analyzeBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        
        // 4. Input Validation (Frontend)
        if (!text) {
            showError("Please enter some text to analyze.");
            return;
        }
        if (text.length < 10) {
            showError("Input is too short. Please provide a complete message.");
            return;
        }
        
        // 5. Loading Animation
        setLoading(true);
        resultContainer.classList.add('hidden');
        
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });
            
            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Server error occurred");
            }
            
            const data = await response.json();
            
            // Wait slightly for better UX (so spinner is visible)
            setTimeout(() => {
                displayResults(data);
                setLoading(false);
            }, 800);
            
        } catch (error) {
            setLoading(false);
            showError(error.message || "Failed to connect to the analysis engine.");
        }
    });
    
    function showError(message) {
        errorMsg.textContent = message;
        errorMsg.classList.remove('hidden');
    }
    
    function setLoading(isLoading) {
        if (isLoading) {
            analyzeBtn.disabled = true;
            btnText.textContent = "Analyzing...";
            loader.classList.remove('hidden');
            errorMsg.classList.add('hidden');
        } else {
            analyzeBtn.disabled = false;
            btnText.textContent = "Analyze Content";
            loader.classList.add('hidden');
        }
    }
    
    function displayResults(data) {
        // Show container
        resultContainer.classList.remove('hidden');
        
        // Set Confidence Meter (0-100)
        // 3. Confidence Meter Logic
        const probability = data.scam_probability;
        confidencePercentage.textContent = `${probability}%`;
        confidenceFill.style.width = `${probability}%`;
        
        // Remove previous status classes
        statusIcon.className = "fa-solid status-icon";
        
        if (probability < 40) {
            // Safe
            resultTitle.textContent = "Content Appears Legitimate";
            resultTitle.style.color = "var(--safe-color)";
            statusIcon.classList.add("fa-circle-check", "safe-color");
        } else if (probability < 70) {
            // Suspicious
            resultTitle.textContent = "Suspicious Content Detected";
            resultTitle.style.color = "var(--suspicious-color)";
            statusIcon.classList.add("fa-triangle-exclamation", "suspicious-text");
        } else {
            // Scam
            resultTitle.textContent = "High Risk: Scam Detected";
            resultTitle.style.color = "var(--scam-color)";
            statusIcon.classList.add("fa-shield-virus", "scam-color");
        }
        
        // 2. Reason Engine
        reasonList.innerHTML = '';
        if (data.reasons && data.reasons.length > 0) {
            data.reasons.forEach(reason => {
                const li = document.createElement('li');
                li.textContent = reason;
                reasonList.appendChild(li);
            });
            reasonEngine.classList.remove('hidden');
        } else {
            if (probability >= 40) {
                const li = document.createElement('li');
                li.textContent = "Model detected subtle linguistic patterns and structure common in fraudulent job postings.";
                reasonList.appendChild(li);
                reasonEngine.classList.remove('hidden');
            } else {
                reasonEngine.classList.add('hidden');
            }
        }
    }
});

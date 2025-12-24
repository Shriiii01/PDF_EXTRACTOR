const form = document.getElementById('pdfForm');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const results = document.getElementById('results');
const submitBtn = document.getElementById('submitBtn');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Hide previous results and errors
    error.classList.add('hidden');
    results.classList.add('hidden');
    loading.classList.remove('hidden');
    submitBtn.disabled = true;
    
    const formData = new FormData(form);
    
    try {
        const response = await fetch('http://localhost:8000/api/process-pdf', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'An error occurred');
        }
        
        // Display results
        displayResults(data);
        
    } catch (err) {
        showError(err.message);
    } finally {
        loading.classList.add('hidden');
        submitBtn.disabled = false;
    }
});

function displayResults(data) {
    // Display AI response
    const aiResponseDiv = document.getElementById('aiResponse');
    aiResponseDiv.textContent = data.ai_response;
    
    // Display extracted text
    const extractedTextDiv = document.getElementById('extractedText');
    extractedTextDiv.textContent = data.extracted_text;
    
    // Display input details
    document.getElementById('procedureDisplay').textContent = data.procedure;
    document.getElementById('insurancePayerDisplay').textContent = data.insurance_payer;
    
    // Show results section
    results.classList.remove('hidden');
    
    // Scroll to results
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showError(message) {
    error.textContent = `Error: ${message}`;
    error.classList.remove('hidden');
}


document.addEventListener('DOMContentLoaded', function() {
    const videoForm = document.getElementById('videoForm');
    const processingSection = document.getElementById('processingSection');
    const resultsSection = document.getElementById('resultsSection');
    const errorSection = document.getElementById('errorSection');
    const progressBar = document.querySelector('.progress-bar');
    const statusText = document.getElementById('statusText');
    const reelsContainer = document.getElementById('reelsContainer');

    let processingInterval;

    videoForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Reset UI
        processingSection.classList.remove('d-none');
        resultsSection.classList.add('d-none');
        errorSection.classList.add('d-none');
        progressBar.style.width = '0%';
        
        const formData = new FormData(videoForm);
        
        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('Failed to process video');
            }
            
            // Start progress monitoring
            startProgressMonitoring();
            
        } catch (error) {
            showError(error.message);
        }
    });

    function startProgressMonitoring() {
        processingInterval = setInterval(checkProgress, 1000);
    }

    async function checkProgress() {
        try {
            const response = await fetch('/status');
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            progressBar.style.width = `${data.progress}%`;
            statusText.textContent = `Processing: ${data.progress}%`;
            
            if (data.status === 'completed') {
                clearInterval(processingInterval);
                showResults();
            }
            
        } catch (error) {
            clearInterval(processingInterval);
            showError(error.message);
        }
    }

    function showResults() {
        processingSection.classList.add('d-none');
        resultsSection.classList.remove('d-none');
        
        // Clear previous results
        reelsContainer.innerHTML = '';
        
        // Add download buttons for each segment
        for (let i = 0; i < 10; i++) {
            const col = document.createElement('div');
            col.className = 'col-md-6 mb-3';
            
            col.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Reel ${i + 1}</h5>
                        <a href="/download/${i}" class="btn btn-secondary w-100">
                            Download Reel ${i + 1}
                        </a>
                    </div>
                </div>
            `;
            
            reelsContainer.appendChild(col);
        }
    }

    function showError(message) {
        processingSection.classList.add('d-none');
        errorSection.classList.remove('d-none');
        document.getElementById('errorText').textContent = message;
    }
});

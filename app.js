document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');
    const nicheInput = document.getElementById('niche-input');
    const modal = document.getElementById('capture-modal');
    const closeModal = document.querySelector('.close-modal');
    const targetKeywordSpan = document.getElementById('target-keyword');
    const leadForm = document.getElementById('lead-form');

    // Open Modal on Analyze
    analyzeBtn.addEventListener('click', () => {
        const query = nicheInput.value.trim();
        if (!query) {
            nicheInput.classList.add('shake');
            setTimeout(() => nicheInput.classList.remove('shake'), 500);
            return;
        }

        // Set the keyword in the modal
        targetKeywordSpan.textContent = query;

        // Show modal
        modal.classList.remove('hidden');
        // Slight delay to allow display:block to apply before opacity transition
        setTimeout(() => modal.classList.add('visible'), 10);
    });

    // Close Modal
    closeModal.addEventListener('click', () => {
        modal.classList.remove('visible');
        setTimeout(() => modal.classList.add('hidden'), 300);
    });

    // Handle Form Submission
    leadForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const button = leadForm.querySelector('button');
        const originalText = button.textContent;

        console.log("Submitting lead:", email);

        // Simulator loader
        button.textContent = "Validating...";
        button.disabled = true;

        fetch('/api/subscribe', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: email,
                keyword: document.getElementById('target-keyword').textContent
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    button.textContent = "Success! Check your inbox.";
                    button.style.background = "#10b981"; // Green
                } else {
                    button.textContent = "Error. Try again.";
                    button.style.background = "#ef4444"; // Red
                }

                // Reset after 2 seconds
                setTimeout(() => {
                    modal.classList.remove('visible');
                    setTimeout(() => {
                        modal.classList.add('hidden');
                        button.textContent = originalText;
                        button.disabled = false;
                        button.style.background = ""; // Reset
                        nicheInput.value = ""; // Clear input
                    }, 300);
                }, 2000);
            })
            .catch(err => {
                console.error(err);
                button.textContent = "Network Error";
            });
    });
});

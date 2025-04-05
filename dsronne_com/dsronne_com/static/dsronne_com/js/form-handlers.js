// form-handlers.js
function initializeFormWithLoading(formId, resultContainerId, loadingSpinnerId) {
    document.getElementById(formId).addEventListener('submit', function(e) {
        e.preventDefault();

        // Show loading spinner, hide results
        document.getElementById(loadingSpinnerId).style.display = 'block';
        document.getElementById(resultContainerId).style.display = 'none';

        // Get form data
        const formData = new FormData(this);

        // Send AJAX request
        fetch(this.action || window.location.href, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading spinner
            document.getElementById(loadingSpinnerId).style.display = 'none';

            // Show and update results
            const resultContainer = document.getElementById(resultContainerId);
            resultContainer.style.display = 'block';
            resultContainer.innerHTML = data.result;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById(loadingSpinnerId).style.display = 'none';
            // Handle error case
        });
    });
}
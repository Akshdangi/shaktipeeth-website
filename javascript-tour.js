async function validateForm(event) {
    event.preventDefault();
    const form = event.target;
    
    if (!form.checkValidity()) {
        return false;
    }

    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.classList.add('loading');
    submitButton.textContent = 'Processing...';

    try {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        const response = await fetch('http://127.0.0.1:5500/book-tour-complete.html', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        if (response.ok) {
            const successMessage = document.querySelector('.success-message');
            successMessage.style.display = 'block';
            form.reset();
        } else {
            alert(result.error || 'Booking failed. Please try again.');
        }
    } catch (error) {
        alert('An error occurred. Please try again.');
    } finally {
        submitButton.classList.remove('loading');
        submitButton.textContent = 'Book Now';
    }

    return false;
}
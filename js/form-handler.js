/**
 * Form Handler for MedStat Forms
 * Handles contact form and demo request submissions to FastAPI backend
 */

(function () {
    'use strict';

    // Configuration
    const API_BASE_URL = 'http://localhost:8000';  // Change for production

    /**
     *  Show loading state on form
     */
    function showLoading(form, button) {
        button.disabled = true;
        button.dataset.originalText = button.textContent;
        button.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Sending...';
        form.style.opacity = '0.7';
    }

    /**
     * Hide loading state
     */
    function hideLoading(form, button) {
        button.disabled = false;
        button.textContent = button.dataset.originalText;
        form.style.opacity = '1';
    }

    /**
     * Show success message
     */
    function showSuccess(message, form) {
        const successDiv = document.createElement('div');
        successDiv.className = 'form-message form-success';
        successDiv.innerHTML = `
            <i class="fa fa-check-circle"></i>
            <p>${message}</p>
        `;

        form.insertBefore(successDiv, form.firstChild);

        // Scroll to message
        successDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });

        // Remove after 8 seconds
        setTimeout(() => {
            successDiv.style.opacity = '0';
            setTimeout(() => successDiv.remove(), 300);
        }, 8000);

        // Reset form
        form.reset();
    }

    /**
     * Show error message
     */
    function showError(message, form) {
        // Remove any existing messages
        const existingMessages = form.querySelectorAll('.form-message');
        existingMessages.forEach(msg => msg.remove());

        const errorDiv = document.createElement('div');
        errorDiv.className = 'form-message form-error';
        errorDiv.innerHTML = `
            <i class="fa fa-exclamation-circle"></i>
            <p>${message}</p>
        `;

        form.insertBefore(errorDiv, form.firstChild);

        // Scroll to message
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });

        // Remove after 8 seconds
        setTimeout(() => {
            errorDiv.style.opacity = '0';
            setTimeout(() => errorDiv.remove(), 300);
        }, 8000);
    }

    /**
     * Submit form to API
     */
    async function submitForm(endpoint, formData, form, button) {
        try {
            showLoading(form, button);

            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                showSuccess(data.message, form);
            } else {
                throw new Error(data.detail || 'Something went wrong');
            }

        } catch (error) {
            console.error('Form submission error:', error);
            showError(
                error.message || 'Failed to submit form. Please try again or contact us directly.',
                form
            );
        } finally {
            hideLoading(form, button);
        }
    }

    /**
     * Handle contact form submission
     */
    function handleContactForm() {
        const form = document.getElementById('contact-form');
        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = {
                name: form.querySelector('[name="name"]').value.trim(),
                email: form.querySelector('[name="email"]').value.trim(),
                phone: form.querySelector('[name="phone"]').value.trim(),
                type: form.querySelector('[name="type"]').value,
                message: form.querySelector('[name="message"]').value.trim()
            };

            const button = form.querySelector('button[type="submit"]');
            await submitForm('/api/contact', formData, form, button);
        });
    }

    /**
     * Handle demo request form submission
     */
    function handleDemoForm() {
        const form = document.getElementById('demo-form');
        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = {
                name: form.querySelector('[name="name"]').value.trim(),
                clinic: form.querySelector('[name="clinic"]').value.trim(),
                role: form.querySelector('[name="role"]').value.trim(),
                email: form.querySelector('[name="email"]').value.trim(),
                phone: form.querySelector('[name="phone"]').value.trim(),
                interests: form.querySelector('[name="interests"]').value.trim()
            };

            const button = form.querySelector('button[type="submit"]');
            await submitForm('/api/demo-request', formData, form, button);
        });
    }

    /**
     * Initialize forms when DOM is ready
     */
    function init() {
        handleContactForm();
        handleDemoForm();
    }

    // Run when DOM is loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

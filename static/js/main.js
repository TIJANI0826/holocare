// Habib Medical Hospital - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeAccessibility();
    initializeFormHandling();
});

/**
 * Initialize accessibility features
 */
function initializeAccessibility() {
    // Focus management for modals
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            const focusableElements = this.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            if (focusableElements.length > 0) {
                focusableElements[0].focus();
            }
        });
    });

    // Add ARIA labels to interactive elements
    document.querySelectorAll('[role="button"]').forEach(el => {
        if (!el.getAttribute('aria-label')) {
            el.setAttribute('aria-label', el.innerText);
        }
    });

    // Ensure all interactive elements are keyboard accessible
    document.querySelectorAll('a, button, input, select, textarea').forEach(el => {
        el.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && this.tagName !== 'TEXTAREA') {
                this.click();
            }
        });
    });
}

/**
 * Initialize form handling
 */
function initializeFormHandling() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            this.classList.add('was-validated');
        });
    });
}

/**
 * API fetch helper with error handling
 */
async function fetchAPI(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

/**
 * Show notification/toast
 */
function showNotification(message, type = 'info', duration = 3000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    const container = document.querySelector('main') || document.body;
    container.insertBefore(alertDiv, container.firstChild);

    if (duration > 0) {
        setTimeout(() => {
            alertDiv.remove();
        }, duration);
    }
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

/**
 * Debounce function for search inputs
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Toggle mobile menu
 */
function toggleMobileMenu() {
    const menu = document.getElementById('navbarNav');
    if (menu) {
        menu.classList.toggle('show');
    }
}

/**
 * Smooth scroll to element
 */
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Log page view for analytics
 */
function trackPageView(pageName) {
    if (typeof gtag !== 'undefined') {
        gtag('config', 'GA_MEASUREMENT_ID', {
            'page_title': pageName,
            'page_path': window.location.pathname
        });
    }
}

// Export functions for module usage if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        fetchAPI,
        showNotification,
        formatDate,
        debounce,
        toggleMobileMenu,
        smoothScrollTo,
        trackPageView
    };
}

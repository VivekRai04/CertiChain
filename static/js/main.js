// Main JavaScript file for Certificate Verification System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide flash messages after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        });
    }, 5000);

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // File upload preview
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                displayFileInfo(file, input);
            }
        });
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// File information display function
function displayFileInfo(file, input) {
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
    
    let message = '';
    let alertClass = 'alert-info';
    
    if (!allowedTypes.includes(file.type)) {
        message = `Invalid file type. Please select PDF, JPG, or PNG files only.`;
        alertClass = 'alert-danger';
    } else if (file.size > maxSize) {
        message = `File too large. Maximum size is 16MB. Selected file: ${(file.size / 1024 / 1024).toFixed(2)}MB`;
        alertClass = 'alert-warning';
    } else {
        message = `Selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)}MB)`;
        alertClass = 'alert-success';
    }
    
    // Remove existing alerts
    const existingAlerts = input.parentNode.querySelectorAll('.file-info-alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert ${alertClass} file-info-alert mt-2`;
    alertDiv.innerHTML = `<i class="fas fa-info-circle me-2"></i>${message}`;
    
    input.parentNode.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Utility function to format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Copy to clipboard utility
function copyToClipboard(text, successMessage = 'Copied to clipboard!') {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showNotification(successMessage, 'success');
        }).catch(function(err) {
            fallbackCopyToClipboard(text, successMessage);
        });
    } else {
        fallbackCopyToClipboard(text, successMessage);
    }
}

// Fallback copy method for older browsers
function fallbackCopyToClipboard(text, successMessage) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.top = '-9999px';
    document.body.appendChild(textArea);
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showNotification(successMessage, 'success');
        } else {
            showNotification('Failed to copy to clipboard', 'error');
        }
    } catch (err) {
        showNotification('Failed to copy to clipboard', 'error');
    }
    
    document.body.removeChild(textArea);
}

// Show notification toast
function showNotification(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    
    const iconMap = {
        success: 'fa-check-circle',
        error: 'fa-times-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    
    const colorMap = {
        success: 'var(--bs-success)',
        error: 'var(--bs-danger)',
        warning: 'var(--bs-warning)',
        info: 'var(--bs-info)'
    };
    
    toast.innerHTML = `<i class="fas ${iconMap[type]} me-2"></i>${message}`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colorMap[type]};
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 9999;
        animation: slideInRight 0.3s ease-out;
        max-width: 300px;
        word-wrap: break-word;
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 4000);
    
    // Click to dismiss
    toast.addEventListener('click', () => {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    });
}

// Add CSS animations if not already added
if (!document.getElementById('toast-animations')) {
    const style = document.createElement('style');
    style.id = 'toast-animations';
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
        
        .toast-notification {
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        
        .toast-notification:hover {
            transform: scale(1.02);
        }
    `;
    document.head.appendChild(style);
}

// Loading spinner utility
function showLoadingSpinner(element, text = 'Loading...') {
    if (element) {
        element.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            ${text}
        `;
        element.disabled = true;
    }
}

function hideLoadingSpinner(element, originalText) {
    if (element) {
        element.innerHTML = originalText;
        element.disabled = false;
    }
}

// Format date utility
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Blockchain hash display utility
function truncateHash(hash, startLength = 8, endLength = 8) {
    if (hash.length <= startLength + endLength + 3) {
        return hash;
    }
    return `${hash.substring(0, startLength)}...${hash.substring(hash.length - endLength)}`;
}

// Form validation helpers
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password.length >= 6;
}

function validateAccessCode(code) {
    const cleanCode = code.replace(/[-\s]/g, '');
    return cleanCode.length === 12 && /^[A-Z0-9]+$/.test(cleanCode);
}

// Export functions for global use
window.CertVerifyUtils = {
    copyToClipboard,
    showNotification,
    showLoadingSpinner,
    hideLoadingSpinner,
    formatDate,
    truncateHash,
    validateEmail,
    validatePassword,
    validateAccessCode,
    formatFileSize
};

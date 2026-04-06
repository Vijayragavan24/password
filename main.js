// =====================
// Global Functions
// =====================

// Initialize tooltips and popovers
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Smooth scroll to anchor
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Format date
function formatDate(date) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(date).toLocaleDateString('en-US', options);
}

// Show toast notification
function showToast(message, type = 'info') {
    const toastHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const container = document.createElement('div');
    container.innerHTML = toastHTML;
    document.body.appendChild(container.firstElementChild);

    setTimeout(() => {
        document.querySelector('.alert').remove();
    }, 5000);
}

// Check if user is authenticated
function isAuthenticated() {
    // This would typically check a session or token
    return window.location.href.includes('/dashboard') || window.location.href.includes('/password-tool');
}

// =====================
// Event Listeners
// =====================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS animations
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            once: true,
            offset: 100
        });
    }

    // Initialize tooltips
    initializeTooltips();

    // Add smooth scroll to all internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                smoothScroll(href);
            }
        });
    });

    // Add animation to elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('[data-aos]').forEach(el => {
        observer.observe(el);
    });
});

// =====================
// Password Strength Validator
// =====================

class PasswordValidator {
    static MIN_LENGTH = 8;
    
    static validate(password) {
        const strength = {
            length: password.length >= this.MIN_LENGTH,
            lowercase: /[a-z]/.test(password),
            uppercase: /[A-Z]/.test(password),
            numbers: /\d/.test(password),
            special: /[!@#$%^&*()_+\-=\[\]{};:'",.<>?/\\|`~]/.test(password)
        };

        return {
            isValid: Object.values(strength).every(v => v === true),
            strength: strength,
            score: this.calculateScore(strength)
        };
    }

    static calculateScore(strength) {
        let score = 0;
        let requirements = Object.keys(strength).length;

        Object.values(strength).forEach(met => {
            if (met) score += Math.ceil(100 / requirements);
        });

        return Math.min(score, 100);
    }

    static getStrengthLevel(score) {
        if (score < 20) return 'Very Weak';
        if (score < 40) return 'Weak';
        if (score < 60) return 'Medium';
        if (score < 80) return 'Strong';
        return 'Very Strong';
    }
}

// =====================
// API Utilities
// =====================

class APIClient {
    static async request(endpoint, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json'
            }
        };

        const finalOptions = { ...defaultOptions, ...options };

        try {
            const response = await fetch(endpoint, finalOptions);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'An error occurred');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    static async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    static async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

// =====================
// DOM Utilities
// =====================

const DOM = {
    query: (selector) => document.querySelector(selector),
    queryAll: (selector) => document.querySelectorAll(selector),
    
    addClass: (el, className) => {
        if (typeof el === 'string') el = DOM.query(el);
        el?.classList.add(className);
    },
    
    removeClass: (el, className) => {
        if (typeof el === 'string') el = DOM.query(el);
        el?.classList.remove(className);
    },
    
    toggleClass: (el, className) => {
        if (typeof el === 'string') el = DOM.query(el);
        el?.classList.toggle(className);
    },
    
    hasClass: (el, className) => {
        if (typeof el === 'string') el = DOM.query(el);
        return el?.classList.contains(className);
    },
    
    setText: (el, text) => {
        if (typeof el === 'string') el = DOM.query(el);
        if (el) el.textContent = text;
    },
    
    setHTML: (el, html) => {
        if (typeof el === 'string') el = DOM.query(el);
        if (el) el.innerHTML = html;
    },
    
    setAttribute: (el, attr, value) => {
        if (typeof el === 'string') el = DOM.query(el);
        el?.setAttribute(attr, value);
    },
    
    getAttribute: (el, attr) => {
        if (typeof el === 'string') el = DOM.query(el);
        return el?.getAttribute(attr);
    },
    
    on: (el, event, handler) => {
        if (typeof el === 'string') {
            document.querySelectorAll(el).forEach(e => {
                e.addEventListener(event, handler);
            });
        } else {
            el?.addEventListener(event, handler);
        }
    },
    
    off: (el, event, handler) => {
        if (typeof el === 'string') el = DOM.query(el);
        el?.removeEventListener(event, handler);
    },
    
    show: (el) => {
        if (typeof el === 'string') el = DOM.query(el);
        if (el) el.style.display = '';
    },
    
    hide: (el) => {
        if (typeof el === 'string') el = DOM.query(el);
        if (el) el.style.display = 'none';
    }
};

// =====================
// Form Utilities
// =====================

class FormValidator {
    constructor(formSelector) {
        this.form = typeof formSelector === 'string' ? DOM.query(formSelector) : formSelector;
        this.errors = {};
    }

    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    validateRequired(field) {
        const value = field.value?.trim();
        return value !== '' && value !== undefined;
    }

    validateMinLength(field, minLength) {
        return field.value?.length >= minLength;
    }

    addError(fieldName, message) {
        if (!this.errors[fieldName]) {
            this.errors[fieldName] = [];
        }
        this.errors[fieldName].push(message);
    }

    clearErrors() {
        this.errors = {};
    }

    getErrors() {
        return this.errors;
    }

    hasErrors() {
        return Object.keys(this.errors).length > 0;
    }
}

// =====================
// Storage Utilities
// =====================

const Storage = {
    set: (key, value) => {
        localStorage.setItem(key, JSON.stringify(value));
    },
    
    get: (key) => {
        const value = localStorage.getItem(key);
        return value ? JSON.parse(value) : null;
    },
    
    remove: (key) => {
        localStorage.removeItem(key);
    },
    
    clear: () => {
        localStorage.clear();
    }
};

// =====================
// Performance Monitoring
// =====================

const Performance = {
    time: {},
    
    start: (label) => {
        Performance.time[label] = performance.now();
    },
    
    end: (label) => {
        const endTime = performance.now();
        const duration = endTime - Performance.time[label];
        console.log(`${label}: ${duration.toFixed(2)}ms`);
        delete Performance.time[label];
        return duration;
    }
};

// =====================
// Utility Functions
// =====================

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Generate UUID
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy', 'danger');
    });
}

// Export utilities for use in other scripts
window.PasswordValidator = PasswordValidator;
window.APIClient = APIClient;
window.DOM = DOM;
window.FormValidator = FormValidator;
window.Storage = Storage;
window.Performance = Performance;
window.debounce = debounce;
window.throttle = throttle;
window.generateUUID = generateUUID;
window.copyToClipboard = copyToClipboard;

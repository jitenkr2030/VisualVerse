/**
 * VisualVerse Creator Portal - Main JavaScript
 * Handles common functionality across all pages
 */

class VisualVersePortal {
    constructor() {
        this.socket = null;
        this.currentUser = null;
        this.notifications = [];
        this.init();
    }

    init() {
        this.initializeSocket();
        this.setupEventListeners();
        this.initializeComponents();
        this.startAutoRefresh();
    }

    initializeSocket() {
        try {
            this.socket = io({
                transports: ['websocket', 'polling']
            });

            this.socket.on('connect', () => {
                console.log('Connected to VisualVerse Creator Portal');
                this.showNotification('Connected to server', 'success');
            });

            this.socket.on('disconnect', () => {
                console.log('Disconnected from server');
                this.showNotification('Connection lost. Attempting to reconnect...', 'warning');
            });

            this.socket.on('reconnect', () => {
                console.log('Reconnected to server');
                this.showNotification('Reconnected to server', 'success');
            });

            this.socket.on('error', (error) => {
                console.error('Socket error:', error);
                this.showNotification('Connection error', 'error');
            });

        } catch (error) {
            console.error('Failed to initialize socket:', error);
        }
    }

    setupEventListeners() {
        // Global keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Ctrl+N or Cmd+N for new lesson
            if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
                e.preventDefault();
                window.location.href = '/lesson-creator';
            }
            
            // Ctrl+D or Cmd+D for dashboard
            if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
                e.preventDefault();
                window.location.href = '/dashboard';
            }
        });

        // Handle browser back/forward
        window.addEventListener('popstate', (e) => {
            if (e.state && e.state.page) {
                this.navigateToPage(e.state.page);
            }
        });

        // Handle page visibility changes
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.pauseUpdates();
            } else {
                this.resumeUpdates();
            }
        });
    }

    initializeComponents() {
        // Initialize tooltips
        this.initializeTooltips();
        
        // Initialize modals
        this.initializeModals();
        
        // Initialize forms
        this.initializeForms();
        
        // Initialize progress bars
        this.initializeProgressBars();
    }

    initializeTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    initializeModals() {
        // Auto-focus first input in modals
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.addEventListener('shown.bs.modal', () => {
                const firstInput = modal.querySelector('input, textarea, select');
                if (firstInput) {
                    firstInput.focus();
                }
            });
        });
    }

    initializeForms() {
        // Auto-resize textareas
        const textareas = document.querySelectorAll('textarea');
        textareas.forEach(textarea => {
            textarea.addEventListener('input', this.autoResizeTextarea);
        });

        // Form validation
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', this.handleFormSubmit);
        });
    }

    initializeProgressBars() {
        // Animate progress bars on page load
        const progressBars = document.querySelectorAll('.progress-bar');
        progressBars.forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = width;
            }, 100);
        });
    }

    autoResizeTextarea(e) {
        e.target.style.height = 'auto';
        e.target.style.height = e.target.scrollHeight + 'px';
    }

    handleFormSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        }
    }

    // Notification System
    showNotification(message, type = 'info', duration = 5000) {
        const toast = document.getElementById('notificationToast');
        const toastMessage = document.getElementById('toastMessage');
        
        if (!toast || !toastMessage) {
            console.warn('Notification toast elements not found');
            return;
        }
        
        toastMessage.textContent = message;
        
        // Set toast color based on type
        const bgClass = type === 'error' ? 'danger' : 
                       type === 'success' ? 'success' : 
                       type === 'warning' ? 'warning' : 'info';
        
        toast.className = `toast bg-${bgClass} text-white`;
        
        const bsToast = new bootstrap.Toast(toast, {
            delay: duration
        });
        
        bsToast.show();
        
        // Store notification for history
        this.notifications.push({
            message,
            type,
            timestamp: new Date(),
            id: Date.now()
        });
    }

    // API Helper Methods
    async apiRequest(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            this.showNotification('Request failed: ' + error.message, 'error');
            throw error;
        }
    }

    async getLessons() {
        return this.apiRequest('/api/lessons');
    }

    async getSubjects() {
        return this.apiRequest('/api/subjects');
    }

    async createLesson(lessonData) {
        return this.apiRequest('/api/lessons', {
            method: 'POST',
            body: JSON.stringify(lessonData)
        });
    }

    async getLesson(lessonId) {
        return this.apiRequest(`/api/lessons/${lessonId}`);
    }

    async updateLesson(lessonId, lessonData) {
        return this.apiRequest(`/api/lessons/${lessonId}`, {
            method: 'PUT',
            body: JSON.stringify(lessonData)
        });
    }

    async deleteLesson(lessonId) {
        return this.apiRequest(`/api/lessons/${lessonId}`, {
            method: 'DELETE'
        });
    }

    async renderLesson(lessonId) {
        return this.apiRequest(`/api/lessons/${lessonId}/render`, {
            method: 'POST'
        });
    }

    // Progress Tracking
    trackProgress(action, data = {}) {
        const event = {
            action,
            data,
            timestamp: new Date(),
            userAgent: navigator.userAgent,
            url: window.location.href
        };
        
        // Store locally
        if (!localStorage.getItem('vv_progress')) {
            localStorage.setItem('vv_progress', JSON.stringify([]));
        }
        
        const progress = JSON.parse(localStorage.getItem('vv_progress'));
        progress.push(event);
        
        // Keep only last 100 events
        if (progress.length > 100) {
            progress.splice(0, progress.length - 100);
        }
        
        localStorage.setItem('vv_progress', JSON.stringify(progress));
        
        // Send to server (optional)
        if (this.socket && this.socket.connected) {
            this.socket.emit('track_progress', event);
        }
    }

    // Utility Methods
    formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    debounce(func, wait) {
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

    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // Navigation
    navigateToPage(page) {
        const url = page.startsWith('/') ? page : '/' + page;
        history.pushState({ page }, '', url);
        window.location.href = url;
    }

    // Auto-refresh functionality
    startAutoRefresh() {
        // Refresh data every 30 seconds when page is visible
        setInterval(() => {
            if (!document.hidden && this.isActivePage()) {
                this.refreshPageData();
            }
        }, 30000);
    }

    pauseUpdates() {
        // Pause auto-refresh when page is hidden
        this.updatesPaused = true;
    }

    resumeUpdates() {
        // Resume auto-refresh when page becomes visible
        this.updatesPaused = false;
        this.refreshPageData();
    }

    isActivePage() {
        // Check if this is the current active page
        const path = window.location.pathname;
        return path === '/' || path === '/dashboard' || path === '/lesson-manager';
    }

    refreshPageData() {
        // Override in specific page components
        console.log('Refreshing page data...');
    }

    // Error Handling
    handleError(error, context = '') {
        console.error(`Error in ${context}:`, error);
        
        const message = error.message || 'An unexpected error occurred';
        this.showNotification(`${context}: ${message}`, 'error');
        
        // Track error for analytics
        this.trackProgress('error', {
            message: message,
            context: context,
            stack: error.stack
        });
    }

    // Performance Monitoring
    startTimer(name) {
        performance.mark(`${name}-start`);
    }

    endTimer(name) {
        performance.mark(`${name}-end`);
        performance.measure(name, `${name}-start`, `${name}-end`);
        
        const measure = performance.getEntriesByName(name)[0];
        console.log(`${name} took ${measure.duration.toFixed(2)}ms`);
        
        return measure.duration;
    }

    // Theme Management
    toggleTheme() {
        const body = document.body;
        const isDark = body.classList.contains('dark-theme');
        
        if (isDark) {
            body.classList.remove('dark-theme');
            localStorage.setItem('vv-theme', 'light');
        } else {
            body.classList.add('dark-theme');
            localStorage.setItem('vv-theme', 'dark');
        }
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('vv-theme') || 'light';
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
        }
    }
}

// Initialize the portal when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Create global instance
    window.visualVersePortal = new VisualVersePortal();
    
    // Load saved theme
    window.visualVersePortal.loadTheme();
    
    // Add animation classes to elements
    const animateElements = document.querySelectorAll('.card, .stat-card, .feature-card');
    animateElements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.1}s`;
        el.classList.add('fade-in');
    });
    
    // Track page load
    window.visualVersePortal.trackProgress('page_load', {
        page: window.location.pathname,
        loadTime: performance.now()
    });
});

// Handle page unload
window.addEventListener('beforeunload', () => {
    if (window.visualVersePortal) {
        window.visualVersePortal.trackProgress('page_unload', {
            page: window.location.pathname,
            timeOnPage: Date.now() - window.visualVersePortal.pageStartTime
        });
    }
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VisualVersePortal;
}

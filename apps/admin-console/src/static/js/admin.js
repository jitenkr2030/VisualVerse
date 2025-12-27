/*
VisualVerse Admin Console - Main JavaScript
*/

// Global configuration
const CONFIG = {
    apiTimeout: 30000,
    maxRetries: 3,
    retryDelay: 1000,
    dateFormat: 'YYYY-MM-DD',
    datetimeFormat: 'YYYY-MM-DD HH:mm:ss'
};

// Toast notification system
const Toast = {
    show: function(message, type = 'info', duration = 3000) {
        const toastContainer = document.getElementById('notificationToast');
        const toastMessage = document.getElementById('toastMessage');
        const toastHeader = toastContainer.querySelector('.toast-header');
        
        if (!toastContainer || !toastMessage) {
            console.log(`[${type.toUpperCase()}] ${message}`);
            return;
        }
        
        // Set message
        toastMessage.textContent = message;
        
        // Set type styling
        const bgColors = {
            'success': 'bg-success',
            'error': 'bg-danger',
            'danger': 'bg-danger',
            'warning': 'bg-warning',
            'info': 'bg-info'
        };
        
        toastContainer.className = `toast ${bgColors[type] || 'bg-info'} text-white`;
        
        // Show toast
        const bsToast = new bootstrap.Toast(toastContainer, {
            delay: duration
        });
        bsToast.show();
    },
    
    success: function(message, duration) {
        this.show(message, 'success', duration);
    },
    
    error: function(message, duration) {
        this.show(message, 'error', duration);
    },
    
    warning: function(message, duration) {
        this.show(message, 'warning', duration);
    },
    
    info: function(message, duration) {
        this.show(message, 'info', duration);
    }
};

// Loading overlay
const Loading = {
    show: function(message = 'Processing...') {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.querySelector('p').textContent = message;
            overlay.classList.remove('d-none');
        }
    },
    
    hide: function() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.classList.add('d-none');
        }
    }
};

// API helper
const API = {
    baseUrl: '',
    
    async request(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            timeout: CONFIG.apiTimeout
        };
        
        const mergedOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };
        
        try {
            const response = await fetch(url, mergedOptions);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    get: function(url) {
        return this.request(url, { method: 'GET' });
    },
    
    post: function(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    put: function(url, data) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    
    delete: function(url) {
        return this.request(url, { method: 'DELETE' });
    }
};

// Chart utilities
const Charts = {
    defaults: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    usePointStyle: true,
                    padding: 20
                }
            }
        }
    },
    
    colors: [
        '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b',
        '#9b59b6', '#3498db', '#2ecc71', '#e67e22', '#34495e'
    ],
    
    createLine: function(ctx, labels, datasets, options = {}) {
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: datasets.map((ds, i) => ({
                    ...ds,
                    borderColor: ds.borderColor || this.colors[i % this.colors.length],
                    backgroundColor: ds.backgroundColor || this.colors[i % this.colors.length] + '20',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: ds.fill !== false
                }))
            },
            options: {
                ...this.defaults,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#e3e6f0'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                ...options
            }
        });
    },
    
    createBar: function(ctx, labels, datasets, options = {}) {
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: datasets.map((ds, i) => ({
                    ...ds,
                    backgroundColor: ds.backgroundColor || this.colors[i % this.colors.length] + '80',
                    borderColor: ds.borderColor || this.colors[i % this.colors.length],
                    borderWidth: 1
                }))
            },
            options: {
                ...this.defaults,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#e3e6f0'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                ...options
            }
        });
    },
    
    createDoughnut: function(ctx, labels, data, options = {}) {
        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: this.colors.slice(0, data.length),
                    borderWidth: 0
                }]
            },
            options: {
                ...this.defaults,
                cutout: '70%',
                ...options
            }
        });
    }
};

// DataTable helper
const DataTable = {
    create: function(tableId, options = {}) {
        const table = document.getElementById(tableId);
        if (!table) return null;
        
        return new DataTable(table, {
            responsive: true,
            pageLength: options.pageLength || 10,
            lengthMenu: [[10, 25, 50, -1], [10, 25, 50, 'All']],
            language: {
                search: '<i class="fas fa-search"></i> Search:',
                searchPlaceholder: 'Search...',
                lengthMenu: 'Show _MENU_ entries',
                info: 'Showing _START_ to _END_ of _TOTAL_ entries',
                infoEmpty: 'No entries available',
                infoFiltered: '(filtered from _MAX_ total entries)',
                paginate: {
                    first: '<i class="fas fa-angle-double-left"></i>',
                    previous: '<i class="fas fa-angle-left"></i>',
                    next: '<i class="fas fa-angle-right"></i>',
                    last: '<i class="fas fa-angle-double-right"></i>'
                }
            },
            ...options
        });
    }
};

// Utility functions
const Utils = {
    formatDate: function(date, format = CONFIG.dateFormat) {
        if (!date) return '-';
        
        const d = new Date(date);
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        
        return format.replace('YYYY', d.getFullYear())
                     .replace('MM', String(d.getMonth() + 1).padStart(2, '0'))
                     .replace('DD', String(d.getDate()).padStart(2, '0'))
                     .replace('MMM', months[d.getMonth()]);
    },
    
    formatDateTime: function(date) {
        return this.formatDate(date, CONFIG.datetimeFormat);
    },
    
    formatNumber: function(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    },
    
    formatDuration: function(seconds) {
        if (!seconds) return '-';
        
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        
        if (hours > 0) {
            return `${hours}h ${minutes}m`;
        }
        return `${minutes}m`;
    },
    
    getInitials: function(name) {
        if (!name) return '?';
        return name.split(' ')
                   .map(word => word[0])
                   .join('')
                   .toUpperCase()
                   .slice(0, 2);
    },
    
    getStatusClass: function(status) {
        const statusMap = {
            'active': 'success',
            'completed': 'success',
            'approved': 'success',
            'pending': 'warning',
            'in_progress': 'info',
            'processing': 'info',
            'inactive': 'secondary',
            'rejected': 'danger',
            'failed': 'danger',
            'error': 'danger'
        };
        return statusMap[status.toLowerCase()] || 'secondary';
    },
    
    truncate: function(str, length = 50) {
        if (!str) return '-';
        if (str.length <= length) return str;
        return str.substring(0, length) + '...';
    },
    
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text)
            .then(() => Toast.success('Copied to clipboard'))
            .catch(() => Toast.error('Failed to copy'));
    },
    
    confirm: function(message, onConfirm, onCancel) {
        if (confirm(message)) {
            if (onConfirm) onConfirm();
        } else if (onCancel) {
            onCancel();
        }
    }
};

// Initialize common functionality
document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Enable popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            if (bootstrap.Alert.getInstance(alert)) {
                bootstrap.Alert.getInstance(alert).close();
            } else {
                alert.style.display = 'none';
            }
        });
    }, 5000);
    
    // Handle active nav link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(function(link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Toast, Loading, API, Charts, DataTable, Utils };
}

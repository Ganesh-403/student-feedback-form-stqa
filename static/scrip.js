// Frontend JavaScript for the feedback portal

document.addEventListener('DOMContentLoaded', function() {
    // Form validation for login
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();
            
            if (!username || !password) {
                e.preventDefault();
                alert('Please fill in both username and password');
                return false;
            }
        });
    }
    
    // Form validation for feedback
    const feedbackForm = document.getElementById('feedbackForm');
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', function(e) {
            const feedbackText = document.getElementById('feedback_text').value.trim();
            const rating = document.getElementById('rating').value;
            
            if (!feedbackText) {
                e.preventDefault();
                alert('Please enter your feedback');
                return false;
            }
            
            if (!rating) {
                e.preventDefault();
                alert('Please select a rating');
                return false;
            }
            
            if (feedbackText.length < 10) {
                e.preventDefault();
                alert('Feedback must be at least 10 characters long');
                return false;
            }
        });
    }
    
    // Auto-hide flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 5000);
    });
    
    // Table sorting functionality for admin dashboard
    const table = document.getElementById('feedbackTable');
    if (table) {
        const headers = table.querySelectorAll('th');
        headers.forEach(function(header, index) {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                sortTable(table, index);
            });
        });
    }
});

// Simple table sorting function
function sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    const sortedRows = rows.sort(function(a, b) {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        // Try to parse as numbers
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return aNum - bNum;
        }
        
        // Sort as strings
        return aValue.localeCompare(bValue);
    });
    
    // Clear tbody and append sorted rows
    tbody.innerHTML = '';
    sortedRows.forEach(function(row) {
        tbody.appendChild(row);
    });
}
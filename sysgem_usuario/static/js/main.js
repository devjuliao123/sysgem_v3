document.addEventListener('DOMContentLoaded', function() {
    // Sidebar Toggle Logic
    const sidebarToggle = document.getElementById('sidebarToggle');
    const wrapper = document.getElementById('wrapper');
    const overlay = document.getElementById('sidebar-overlay');

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            wrapper.classList.toggle('toggled');
            console.log('Sidebar toggled. Wrapper classes:', wrapper.className);
        });
    }

    // Close sidebar on mobile when clicking the overlay
    if (overlay) {
        overlay.addEventListener('click', () => {
            wrapper.classList.remove('toggled');
        });
    }

    // Close sidebar on mobile when clicking a link
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth < 768) {
                wrapper.classList.remove('toggled');
            }
        });
    });

    // Handle window resize to clean up states
    window.addEventListener('resize', () => {
        if (window.innerWidth >= 768) {
            wrapper.classList.remove('toggled');
        }
    });

    // Global Automatic Uppercase Conversion
    function applyUppercase(element) {
        element.addEventListener('input', function() {
            const start = this.selectionStart;
            const end = this.selectionEnd;
            this.value = this.value.toUpperCase();
            this.setSelectionRange(start, end);
        });
    }

    const inputs = document.querySelectorAll('input[type="text"], textarea');
    inputs.forEach(applyUppercase);

    // Initial check for pre-filled inputs
    inputs.forEach(input => {
        if (input.value) {
            input.value = input.value.toUpperCase();
        }
    });

    // Success/Error Alert Auto-dismiss (optional)
    setTimeout(() => {
        const alerts = document.querySelectorAll('.custom-alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

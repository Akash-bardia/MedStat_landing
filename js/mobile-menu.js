// Mobile Menu Toggle Functionality
(function () {
    'use strict';

    // Wait for DOM to be ready
    function initMobileMenu() {
        const menuToggle = document.querySelector('.mobile-menu-toggle');
        const mobileOverlay = document.querySelector('.mobile-nav-overlay');
        const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
        const body = document.body;

        if (!menuToggle || !mobileOverlay) {
            return; // Elements not found, exit gracefully
        }

        // Toggle menu open/close
        function toggleMenu() {
            const isOpen = menuToggle.classList.contains('active');

            if (isOpen) {
                closeMenu();
            } else {
                openMenu();
            }
        }

        function openMenu() {
            menuToggle.classList.add('active');
            mobileOverlay.classList.add('active');
            body.style.overflow = 'hidden'; // Prevent background scrolling
        }

        function closeMenu() {
            menuToggle.classList.remove('active');
            mobileOverlay.classList.remove('active');
            body.style.overflow = ''; // Restore scrolling
        }

        // Event listeners
        menuToggle.addEventListener('click', toggleMenu);

        // Close menu when clicking on a link
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', () => {
                closeMenu();
            });
        });

        // Close menu when clicking outside (on overlay)
        mobileOverlay.addEventListener('click', (e) => {
            if (e.target === mobileOverlay) {
                closeMenu();
            }
        });

        // Close menu on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && menuToggle.classList.contains('active')) {
                closeMenu();
            }
        });

        // Close menu when window is resized to desktop size
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                if (window.innerWidth > 768 && menuToggle.classList.contains('active')) {
                    closeMenu();
                }
            }, 250);
        });
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMobileMenu);
    } else {
        initMobileMenu();
    }
})();

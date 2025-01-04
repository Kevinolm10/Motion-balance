document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.querySelector('.hamburger');
    const menu = document.querySelector('.menu');
    const ctaOverlay = document.querySelector('.cta-overlay');

    // Toggle menu visibility when the hamburger is clicked
    hamburger.addEventListener('click', function () {
        menu.classList.toggle('active');

        // Move the .cta-overlay down when the menu is active
        if (menu.classList.contains('active')) {
            ctaOverlay.classList.add('menu-open');
        } else {
            ctaOverlay.classList.remove('menu-open');
        }
    });
});
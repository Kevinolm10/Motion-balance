document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.querySelector('.hamburger');
    const menu = document.querySelector('.menu');

    // Toggle menu visibility when the hamburger is clicked
    hamburger.addEventListener('click', function () {
        menu.classList.toggle('active');
    });
});
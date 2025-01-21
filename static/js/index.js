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

    // Add event listeners to each dropdown for mobile
    const dropdownItems = document.querySelectorAll('.nav-item.dropdown');
    dropdownItems.forEach(item => {
        item.addEventListener('click', function (e) {
            // Prevent click event from bubbling up to parent elements
            e.stopPropagation();

            // Toggle the 'open' class on the clicked dropdown item
            item.classList.toggle('open');

            // Optionally, close other open dropdowns
            dropdownItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('open');
                }
            });
        });
    });
});

function initMap() {
    var location = {
        lat: 40.7128,
        lng: -74.0060
    }; // Set coordinates for your map location (example: New York)

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: location
    });

    var marker = new google.maps.Marker({
        position: location,
        map: map
    });
}
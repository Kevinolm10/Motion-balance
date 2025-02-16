document.addEventListener("DOMContentLoaded", function () {
    let e = document.querySelector(".hamburger"),
        t = document.querySelector(".menu"),
        n = document.querySelector(".cta-overlay");
    e.addEventListener("click", function () {
        t.classList.toggle("active"), t.classList.contains("active") ? n.classList.add("menu-open") : n.classList.remove("menu-open");
    });
    let a = document.querySelectorAll(".nav-item.dropdown");
    a.forEach(e => {
        e.addEventListener("click", function (t) {
            t.stopPropagation(), e.classList.toggle("open"), a.forEach(t => {
                t !== e && t.classList.remove("open");
            });
        });
    });
});
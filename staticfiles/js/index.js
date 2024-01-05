let menuToggle = document.getElementById("menu-toggle");
const navList = document.getElementById("nav-list");

if (menuToggle && navList) {
    menuToggle.addEventListener("click", onToggleMenu);
} else {
    console.error("Menu toggle or nav list element not found");
}

function onToggleMenu(e) {
    navList.classList.toggle("hidden");
}

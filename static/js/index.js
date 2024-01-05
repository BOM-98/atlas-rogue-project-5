document.addEventListener("DOMContentLoaded", function () {
  let menuToggle = document.getElementById("menu-toggle");
  const navList = document.getElementById("nav-list");
  const rentDropdown = document.getElementById("rent-menu-button");
  const rentDropdownMenu = document.getElementById("rent-dropdown-menu");

  if (menuToggle && navList) {
    menuToggle.addEventListener("click", () => onToggleMenu(navList));
  } else {
    console.error("Menu toggle or nav list element not found");
  }

  if (rentDropdown && rentDropdownMenu) {
    rentDropdown.addEventListener("click", () => onToggleMenu(rentDropdownMenu));
  }

  function onToggleMenu(element) {
    element.classList.toggle("hidden");
  }
});

/**
 * Initializes the dropdown functionality once the DOM content is fully loaded.
 * It sets up event listeners for the menu toggle and dropdown buttons.
 */
document.addEventListener("DOMContentLoaded", function () {
  let menuToggle = document.getElementById("menu-toggle");
  const navList = document.getElementById("nav-list");
  const dropdownButtons = document.querySelectorAll(".drop-down-button");
  const dropdownMenus = document.querySelectorAll(".drop-down-menu");

  // Add event listener for nav mobile-menu toggle
  if (menuToggle && navList) {
    menuToggle.addEventListener("click", () => onToggleMenu(navList));
  } else {
    console.error("Menu toggle or nav list element not found");
  }

  /**
   * Toggles the visibility of a specified element by adding or removing the 'hidden' class.
   * @param {HTMLElement} element - The element to toggle visibility for.
   */  
  function onToggleMenu(element) {
      element.classList.toggle("hidden");
      console.log("clicked")
    }
  
  // Setup event listeners for each dropdown button  
  dropdownButtons.forEach(button => {
      button.addEventListener('click', function(event) {
        // Close all dropdown menus excluding active one selected
        dropdownMenus.forEach(menu => {
          if (menu !== button.nextElementSibling) {
            menu.classList.add('hidden');
          }
        });

        // Toggle the current dropdown menu
        const dropdownMenu = button.nextElementSibling;
        dropdownMenu.classList.toggle('hidden');

        // Prevent the click event from propagating to the window
        event.stopPropagation();
      });
    });

    // Close all dropdowns when clicking outside
    window.addEventListener('click', function() {
      dropdownMenus.forEach(menu => {
        menu.classList.add('hidden');
      });
    });
});

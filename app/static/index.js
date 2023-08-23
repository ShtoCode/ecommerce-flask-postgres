 document.addEventListener("DOMContentLoaded", function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const menu = document.getElementById('menu');

    menuToggle.addEventListener('click', function() {
      menu.classList.toggle('show-menu');
    });
  });
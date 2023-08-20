const menuToggle = document.querySelector(".menu-toggle");
const navbarUl = document.querySelector(".navbar ul");

menuToggle.addEventListener("click", () => {
  navbarUl.classList.toggle("menu-hidden");
});

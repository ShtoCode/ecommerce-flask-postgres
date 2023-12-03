document.addEventListener("DOMContentLoaded", function() {
   const menuToggle = document.querySelector(".menu-toggle");
   const menu = document.getElementById("menu");

   menuToggle.addEventListener("click", function() {
      menu.classList.toggle("show-menu");
   });

   const loadCart = () => {
      const cartSaved = localStorage.getItem("carrito");
      if (cartSaved) {
         carrito = JSON.parse(cartSaved);
         refreshCounterCart();
      }
   };
   const refreshCounterCart = () => {
      const contadorCarrito = document.getElementById("contador-carrito");
      const totalItems = carrito.reduce((total, product) => total + product.cantidad, 0);
      contadorCarrito.textContent = totalItems.toString();
   };

   loadCart()





});

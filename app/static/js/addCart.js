let cart = [];


document.addEventListener("DOMContentLoaded", function() {
  const loadCart = () => {
    const cartSaved = localStorage.getItem("carrito");
    if (cartSaved) {
      cart = JSON.parse(cartSaved);
      refreshCounterCart();
    }
  };



  const refreshCounterCart = () => {
    const contadorCarrito = document.getElementById("contador-carrito");
    const totalItems = cart.reduce((total, product) => total + product.cantidad, 0);
    contadorCarrito.textContent = totalItems.toString();
  };

  loadCart();




  const addToCart = (id, nombre, precio, cantidad = 1) => {
    const existingProductIndex = cart.findIndex((product) => product.id === id);
    if (existingProductIndex !== -1) {
      cart[existingProductIndex].cantidad += cantidad;
    } else {
      const product = { id, nombre, precio, cantidad };
      cart.push(product);

    }



    refreshCart();
    saveCart();

    location.reload()
  };



  const refreshCart = () => {
    const cartList = document.getElementById("contador-carrito");
    cartList.textContent = cart.length.toString();
  };

  function saveCart() {
    localStorage.setItem("carrito", JSON.stringify(cart));
  }

  const botonesAgregar = document.querySelectorAll(".CartBtn");
  botonesAgregar.forEach((btn) => {
    btn.addEventListener("click", () => {
      const card = btn.closest(".card");
      const productId = card.id;
      const nombre = card.querySelector(".heading").textContent;
      const precio = parseFloat(
        card.querySelector(".price").textContent.slice(2)
      );
      addToCart(productId, nombre, precio);
      refreshCart();
    });
  });

  const botonComprar = document.querySelectorAll(".buyBtn");
  botonComprar.forEach((btn) => {
    btn.addEventListener("click", () => {
      const card = btn.closest(".card");
      const productId = card.id;
      const nombre = card.querySelector(".heading").textContent;
      const precio = parseFloat(
        card.querySelector(".price").textContent.slice(2)
      );
      addToCart(productId, nombre, precio);
      refreshCart();
    });
  });


});


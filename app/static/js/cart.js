const productos = JSON.parse(localStorage.getItem("carrito"));
const productImages = {};
const productQuantities = {};

const calculateTotal = () => {
  let total = 0;
  let cantidadTotal = 0;

  for (const product of productos) {
    total += product.precio * (productQuantities[product.id] || 0);
    cantidadTotal += product.cantidad;
  }

  return { total, cantidadTotal };
};

function formatearNumero(numero) {
  return numero.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

const updateTotal = () => {
  const totalElement = document.getElementById("total-price");
  const { total, cantidadTotal } = calculateTotal();
  const totalFormated = formatearNumero(total);
  totalElement.textContent = `TOTAL (${cantidadTotal} producto${
    cantidadTotal === 1 ? "" : "s"
  })  $${totalFormated}`;
};

if (productos.length > 0) {
  for (const product of productos) {
    const productId = product.id;

    if (!productQuantities[productId]) {
      productQuantities[productId] = product.cantidad;
    }

    if (!productImages[productId]) {
      const imageEndpoint = `http://localhost:8000/image/${productId}/principal`;

      fetch(imageEndpoint)
        .then((response) => {
          if (!response.ok) {
            throw new Error("La solicitud de imagen no tuvo éxito.");
          }
          return response.blob();
        })
        .then((blob) => {
          const url = URL.createObjectURL(blob);
          productImages[productId] = url;
          showProductsInCart();
        })
        .catch((error) => {
          console.error("Error al cargar la imagen:", error);
        });
    }
  }

  updateTotal();
} else {
  const mensaje = document.createElement("p");
  mensaje.textContent = "No hay productos en el carrito.";
  document.getElementById("cart-items").appendChild(mensaje);
}

const showProductsInCart = () => {
  const listaProductos = document.getElementById("cart-items");
  listaProductos.innerHTML = "";

  const groupedProducts = {};

  for (const product of productos) {
    const productId = product.id;
    if (!groupedProducts[productId]) {
      groupedProducts[productId] = {
        product: product,
        quantity: 0,
      };
    }
    groupedProducts[productId].quantity += product.cantidad;
  }

  for (const groupId in groupedProducts) {
    const group = groupedProducts[groupId];
    const product = group.product;
    const quantity = group.quantity;

    const item = document.createElement("li");
    item.className = "product-item";

    const productImage = document.createElement("img");

    const productId = product.id;
    const imageEndpoint = `http://localhost:8000/image/${productId}/principal`;

    fetch(imageEndpoint)
      .then((response) => {
        if (!response.ok) {
          throw new Error("La solicitud de imagen no tuvo éxito.");
        }
        return response.blob();
      })
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        productImage.src = url;
      })
      .catch((error) => {
        console.error("Error al cargar la imagen:", error);
      });

    const productInfo = document.createElement("div");
    productInfo.className = "product-info";
    productInfo.innerHTML = `
        <p class="nombre">Nombre: ${product.nombre}</p>
        <p class="precio">Precio: $${formatearNumero(product.precio)}</p>
        <label>Seleccionar Cantidad:</label>
        <select class="product-quantity" data-product-id="${productId}" onchange="actualizarPrecio(this)">
          ${generateQuantityOptions(quantity)}
        </select>
      `;

    const productActions = document.createElement("div");
    productActions.className = "product-actions";

    const removeButton = document.createElement("span");
    removeButton.className = "remove-button";
    removeButton.textContent = "X";
    removeButton.onclick = () => {
      removeFromCart(productId);
    };

    productActions.appendChild(removeButton);

    item.appendChild(productImage);
    item.appendChild(productInfo);
    item.appendChild(productActions);

    listaProductos.appendChild(item);
  }
};

const generateQuantityOptions = (selectedQuantity) => {
  let options = "";
  for (let i = 1; i <= 5; i++) {
    options += `<option value="${i}" ${
      i === selectedQuantity ? "selected" : ""
    }>${i}</option>`;
  }
  return options;
};

function removeFromCart(productId) {
  const productIndex = productos.findIndex(
    (product) => product.id === productId,
  );

  if (productIndex !== -1) {
    productos.splice(productIndex, 1);

    localStorage.setItem("carrito", JSON.stringify(productos));
    showProductsInCart();
    updateTotal();
    location.reload();
  }
}

function actualizarPrecio(select) {
  const newQuantity = parseInt(select.value, 10);
  const productId = select.getAttribute("data-product-id");
  const product = productos.find((product) => product.id === productId);

  if (product) {
    product.cantidad = newQuantity;

    const productIndex = productos.findIndex((prod) => prod.id === productId);
    if (productIndex !== -1) {
      productos[productIndex] = product;
      localStorage.setItem("carrito", JSON.stringify(productos));
    }

    updateTotal();
    location.reload();
  }
}

const enviarProductos = () => {
  const data = { carrito: productos };
  fetch("/carrito", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  }).catch((error) => {
    console.error("Error al enviar los datos a la ruta de carrito", error);
  });
};

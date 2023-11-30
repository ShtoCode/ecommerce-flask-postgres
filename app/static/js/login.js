document.addEventListener("DOMContentLoaded", function() {
  const form = document.querySelector(".form");
  const btnSubmit = document.getElementById("btn-submit");

  form.addEventListener("submit", async function(event) {
    btnSubmit.textContent = "Enviando...";
    btnSubmit.disabled = true;
    event.preventDefault();

    try {

      const response = await fetch("/user/login", {
        method: "POST",
        body: new FormData(form),
      });
      if (response.ok) {
        btnSubmit.textContent = "Ingresar";
        const rutaActual = window.location.href;
        const baseUrl = rutaActual.split("/").slice(0, 3).join("/");
        window.location.href = baseUrl;
      }
      else {
        btnSubmit.textContent = "Ingresar";
        Swal.fire({
          position: "top",
          icon: "error",
          title: "Usuario o contraseña incorrectos!",
          showConfirmButton: false,
          timer: 1500,
        }).then(() => {
          setTimeout(() => {
            window.location.reload();
          }, 600)
        });
      }

    }
    catch (error) {
      console.log(error);
    }


  })

});

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".form");
  const btnSubmit = document.getElementById("btn-submit");

  form.addEventListener("submit", async function (event) {
    btnSubmit.textContent = "Cargando...";

    btnSubmit.disabled = true;

    event.preventDefault();

    try {
      const response = await fetch("/user/register", {
        method: "POST",
        body: new FormData(form),
      });

      if (response.ok) {
        btnSubmit.textContent = "Enviar";

        Swal.fire({
          position: "top",
          icon: "success",
          title: "Usuario registrado con éxito!",
          showConfirmButton: false,
          timer: 1500,
        }).then(() => {
          form.reset();
          const rutaActual = window.location.href;
          const baseUrl = rutaActual.split("/").slice(0, 3).join("/");
          setTimeout(() => {
            window.location.href = baseUrl;
          }, 500);
        });
      } else {
        Swal.fire({
          position: "top",
          icon: "error",
          title: "Hubo un error al enviar el formulario :(",
          showConfirmButton: false,
          timer: 1500,
        });
      }
    } catch (error) {
      console.error("Error de solicitud:", error);
    }
  });
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.form');
    const btnSubmit = document.getElementById('btn-submit');

    form.addEventListener('submit', async function (event) {
      btnSubmit.textContent = 'Enviando...';
      btnSubmit.disabled = true
      
      event.preventDefault();

      try {
        const response = await fetch('/contacto/', {
          method: 'POST',
          body: new FormData(form),
        });

        if (response.ok) {
          btnSubmit.textContent = 'Enviar';

          Swal.fire({
            position: 'top',
            icon: 'success',
            title: 'Mensaje enviado con exito!',
            showConfirmButton: false,
            timer: 1500
          });
          form.reset()

        } else {
          Swal.fire({
            position: 'top',
            icon: 'error',
            title: 'Hubo un error al enviar el formulario :(', 
            showConfirmButton: false,
            timer: 1500
          });
        }
      } catch (error) {
        console.error('Error de solicitud:', error);
      }
    });
  });
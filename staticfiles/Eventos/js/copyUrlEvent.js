const urlIdButton = document.getElementById('url_event');
const urlId = document.getElementById('url_event_text');

urlIdButton.addEventListener('click', () => {
    const textToCopy = urlId.value;
    navigator.clipboard.writeText(textToCopy)
        .then(() => {
            Toast.fire({
                icon: 'success',
                title: '¡URL copiada exitosamente!'
            })
            // Aquí podemos mostrar un mensaje de éxito o realizar otras acciones.
        })
        .catch(error => {
            Toast.fire({
                icon: 'error',
                title: `Ocurrió un error. Intente de nuevo o copie con ctrl + c ${textToCopy}`
            })
            // Aquí podemos mostrar un mensaje de error o realizar otras acciones.
        });
});
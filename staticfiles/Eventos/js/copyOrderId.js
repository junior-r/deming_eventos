const orderIdButton = document.getElementById('copy-order-id-button');
const orderId = document.getElementById('order-id');

orderIdButton.addEventListener('click', () => {
    const textToCopy = orderId.innerText;
    navigator.clipboard.writeText(textToCopy)
        .then(() => {
            Toast.fire({
                icon: 'success',
                title: '¡ID de orden copiado exitosamente!'
            })
            // Aquí podemos mostrar un mensaje de éxito o realizar otras acciones.
        })
        .catch(error => {
            Toast.fire({
                icon: 'error',
                title: 'Ocurrió un error. Intente de nuevo o copie con ctrl + c'
            })
            console.log(error)
            // Aquí podemos mostrar un mensaje de error o realizar otras acciones.
        });
});
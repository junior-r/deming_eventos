function cancel_participant(route) {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¡Esperamos cambies de decisión!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Cancelar asistencia',
        cancelButtonText: 'Si asistiré'
    }).then((result) => {
        if (result.value) {
            window.location.href = route;
        }
    })
}
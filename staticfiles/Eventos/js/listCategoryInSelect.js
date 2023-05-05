function add_category_to_select(data) {
    const career = data.career
    const optionHtml = '<option value="' + career.id + '">' + career.name + '</option>';
    const select = $('select[name="career"]')
    if (select.length) {
        select.append(optionHtml);
    }
}

$("#createCareerForm").on('submit', function (e) {
    e.preventDefault();
    const serializedData = $('#createCareerForm').serialize();

    $.ajax({
        url: '/eventos/create_career_ajax/',
        type: "POST",
        dataType: "json",
        data: serializedData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: (data) => {
            $("#createCareerForm").trigger('reset');
            add_category_to_select(data)


            Toast.fire({
                icon: 'success',
                title: 'Categoría creada exitosamente',
            })
        },
        error: (data) => {
            console.log(data)
            Toast.fire({
                icon: 'error',
                title: 'Ocurrió un error. Revise e intente de nuevo.',
            })
        }
    });
})

$("#submit-btn-career").on('click', function (e) {
    e.preventDefault();
    const serializedData = $('#createCareerForm').serialize();

    $.ajax({
        url: '/eventos/create_career_ajax/',
        type: "POST",
        dataType: "json",
        data: serializedData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: function (data) {
            $("#createCareerForm").trigger('reset');
            add_category_to_select(data)

            Toast.fire({
                icon: 'success',
                title: 'Categoría creada exitosamente',
            })
        },
        error: (data) => {
            console.log(data)
            Toast.fire({
                icon: 'error',
                title: 'Ocurrió un error. Revise e intente de nuevo.',
            })
        }
    });
})
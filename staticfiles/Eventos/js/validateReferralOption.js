const select = document.getElementById('id_referral');
const textarea = document.getElementById('id_how_did_you_find_out');

select.addEventListener('change', function () {
    if (select.value === '') {
        textarea.required = true;
        textarea.readOnly = false;
    } else {
        textarea.required = false;
        textarea.readOnly = true;
    }
});
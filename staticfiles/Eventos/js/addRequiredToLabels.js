const form = document.querySelector('#register-participant-form');
const inputs = form.querySelectorAll('input, select, textarea');

inputs.forEach(input => {
    if (input.required) {
        const label = input.labels[0];
        if (label) {
            label.textContent += '*';
        }
    }
});
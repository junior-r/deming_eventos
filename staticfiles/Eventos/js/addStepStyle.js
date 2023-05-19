function agregarEstiloAlAfter(index, border, background) {
    const hojaEstilo = document.createElement('style');

    // Agregar una regla de estilo para el seudoelemento ::after del elemento seleccionado
    hojaEstilo.innerHTML = `.elemento-modificar:nth-child(${index})::after {
            border: ${border};
            background: ${background};
          }`;
    document.getElementsByTagName('head')[0].appendChild(hojaEstilo);
}

const slides = document.querySelectorAll('.tabs');
const elementosModificar = document.querySelectorAll('.steps');

slides.forEach((slide, index) => {
    const camposRequeridos = slide.querySelectorAll('.required-field[required]');

    camposRequeridos.forEach(campo => {
        campo.addEventListener('input', () => verificarEntrada(slide, index));
    });
});

function verificarEntrada(slide, index) {
    const camposRequeridos = slide.querySelectorAll('.required-field[required]');
    const todosLlenos = Array.from(camposRequeridos).every(campo => campo.value !== '');

    camposRequeridos.forEach(campo => {
        if (campo.value === '') {
            elementosModificar[index].classList.remove('text-blue-600', 'dark:text-blue-500', 'after:border-b', 'after:border-blue-100', 'after:border-4', 'after:inline-block', 'dark:after:border-blue-800');
            elementosModificar[index].innerHTML = '<span class="flex items-center justify-center w-8 h-8 bg-red-100 rounded-full lg:h-12 lg:w-12 dark:bg-red-800 shrink-0"><svg fill="#FFFFFF" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"></path></svg></span>'
        }
    });

    if (todosLlenos) {
        elementosModificar[index].classList.add('text-blue-600', 'dark:text-blue-500', 'after:border-b', 'after:border-blue-100', 'after:border-4', 'after:inline-block', 'dark:after:border-blue-800');
        elementosModificar[index].innerHTML = '<span class="flex items-center justify-center w-8 h-8 bg-blue-100 rounded-full lg:h-12 lg:w-12 dark:bg-blue-800 shrink-0"><svg aria-hidden="true" class="w-5 h-5 text-blue-600 lg:w-6 lg:h-6 dark:text-blue-300" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg></span>'
    } else {
        elementosModificar[index].classList.remove('text-blue-600', 'dark:text-blue-500', 'after:border-b', 'after:border-blue-100', 'after:border-4', 'after:inline-block', 'dark:after:border-blue-800');
        elementosModificar[index].innerHTML = '<span class="flex items-center justify-center w-8 h-8 bg-red-100 rounded-full lg:h-12 lg:w-12 dark:bg-red-800 shrink-0"><svg fill="#FFFFFF" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"></path></svg></span>'
    }
}
const navbarHome = document.getElementById('NavbarHome');
const navbarEventos = document.getElementById('NavbarEventos');
const navbarContactos = document.getElementById('NavbarContactos');
const navbarCarreras = document.getElementById('NavbarCarreras');

navbarContactos.removeAttribute('aria-current');
navbarCarreras.removeAttribute('aria-current');
navbarHome.removeAttribute('aria-current');
navbarEventos.setAttribute('aria-current', 'page');

navbarEventos.className = 'block py-2 pl-3 pr-4 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-white';

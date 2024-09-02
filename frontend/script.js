import { loadPage } from './router.js';

function setupEventListeners() {
    document.addEventListener('DOMContentLoaded', () => {
        const buttons = document.querySelectorAll('.navbar-nav .button');

        buttons.forEach(button => {
            button.addEventListener('click', (event) => {
                const page = event.target.getAttribute('data-page');
                loadPage(page);
            });
        });
        loadPage('login');
        
    });

    document.addEventListener('DOMContentLoaded', () => {
        const app = document.getElementById('app');
        app.addEventListener('click', (event) => {
            if (event.target.matches('.nav-link, #app[data-page]')) {
                const page = event.target.getAttribute('data-page');
                loadPage(page);
            }
        });
    });
}

setupEventListeners();

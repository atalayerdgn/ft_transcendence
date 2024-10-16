import { loadPage } from './router.js';
import { saveData } from './register/register.js';
import { /*handleRegisterData,*/ authenticateUser } from './login/login.js';

function setupEventListeners() {
    document.addEventListener('DOMContentLoaded', () => {
        /*const buttons = document.querySelectorAll('.navbar-nav, .button');
        buttons.forEach(button => {
            button.addEventListener('click', (event) => {
                const page = event.target.getAttribute('data-page');
                loadPage(page);
            });
        });*/
        loadPage('login');
    });

    /*document.addEventListener('DOMContentLoaded', () => {
        let i = 0;
        const app = document.getElementById('app');
        app.addEventListener('click', async (event) => {
            event.preventDefault();
            if (event.target.matches('.nav-link, #app[data-page]')) {
                const page = event.target.getAttribute('data-page');
                if (page === 'registerlogin')
                    while (await saveData('register-' + i++) == false); //geçici
                /*if (page === 'login')
                    for (let a = 0; a < i; a++)
                        handleRegisterData(localStorage.getItem('register-' + a));
                loadPage(page);
            }
        });
    });*/

    document.addEventListener('DOMContentLoaded', () => {
        const app = document.getElementById('app');
        app.addEventListener('click', async (event) => {
            event.preventDefault();
            
            if (event.target.matches('.nav-link, #app[data-page]')) {
                const page = event.target.getAttribute('data-page');
                
                if (page === 'registerlogin') {
                    const form = document.getElementById('registerForm'); // Formun ID'sini al
                    const formData = new FormData(form);
                    const data = {};
    
                    formData.forEach((value, key) => {
                        data[key] = value;
                    });
    
                    try {
                        const response = await fetch('http://localhost:8007/users/create/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(data),
                        });
    
                        if (response.ok) {
                            console.log('Başarılı');
                        } else {
                            console.log('Başarısız');
                        }
                    } catch (error) {
                        console.error('Hata:', error);
                    }
                }
    
                // Sayfayı yüklemeye devam et
                loadPage(page);
            }
        });
    });
    

    document.addEventListener('DOMContentLoaded', () => {
        document.addEventListener('click', (event) => {
            if (event.target.matches('.buttonLogin'/*form*/)) {
                event.preventDefault(); // Prevent default form submission
                //if (event.target.getAttribute('data-page') === 'login')
                authenticateUser();
            }
        });
    });
}

setupEventListeners();

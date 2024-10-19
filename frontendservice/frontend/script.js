import { loadPage } from './router.js';
import { saveData } from './register/register.js';
import { authenticateUser } from './login/login.js';
import { validateUser } from './validate/validate.js';

function setupEventListeners() {
    document.addEventListener('DOMContentLoaded', () => {
        loadPage('login');

        const app = document.getElementById('app');
        
        app.addEventListener('click', async (event) => {
            event.preventDefault();

            if (event.target.matches('.nav-link, #app[data-page]')) {
                const page = event.target.getAttribute('data-page');
                
                if (page === 'registerlogin') {
                    const form = document.getElementById('registerForm');
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
                
                loadPage(page);
            }
        });

        // Login butonuna tıklandığında
        document.addEventListener('click', (event) => {
            if (event.target.matches('.buttonLogin')) {
                event.preventDefault(); // Varsayılan form gönderimini engelle
                authenticateUser();
            }

            if (event.target.matches('.validateButton')) {
                event.preventDefault(); // Varsayılan davranışı engelle
                const validateButton = event.target;

                const form = document.getElementById('validateForm');
                const formData = new FormData(form);
                const validateCode = formData.get('twofa_code'); // İki faktörlü kodu al
                const email = localStorage.getItem('email'); // E-postayı localStorage'dan al
                const token = localStorage.getItem('token'); // Token'ı localStorage'dan al

                // Validate user fonksiyonunu çağır
                validateUser(validateCode, token, email);
            }
        });

        // Validate butonunun varlığını kontrol et
        
    });
}

setupEventListeners();

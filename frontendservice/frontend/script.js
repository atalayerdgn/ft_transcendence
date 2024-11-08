import { loadPage } from './router.js';
import { saveData } from './register/register.js';
import { authenticateUser } from './login/login.js';
import { validateUser } from './validate/validate.js';
import { updateUserInfo } from './profile/updateProfile.js';
import { updateProfilePicture } from './profile/updateProfile.js';

function setupEventListeners() {
    document.addEventListener('DOMContentLoaded', () => {

        //sayfa yeni yüklendiğinde token kontrolü yapıyor
        const cookies = document.cookie.split('; ');
        const tokenCookie = cookies.find(cookie => cookie.startsWith('token='));

        if (tokenCookie) {
            // Token mevcut, profile sayfasını yükle
            loadPage('profile');
        } else {
            // Token yok, login sayfasını yükle
            loadPage('login');
        }
        // burada token kontrolu bitiyor
        
        const app = document.getElementById('app');
        
        app.addEventListener('click', async (event) => {
            

            if (event.target.matches('.nav-link, #app[data-page]')) {
                event.preventDefault();
                let page = event.target.getAttribute('data-page');
                
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

                if(page === 'updateProfile') {
                   // console.log('updateProfile');
                    updateUserInfo();
                    return;
                }

                loadPage(page);
            }
        });
        /*const fileInput = document.getElementById('file-input');
                    if (fileInput) {
                        console.log('fileInput saaaa:', fileInput);
                        fileInput.click();
                    }*/
                
        // Login butonuna tıklandığında
        document.addEventListener('click', (event) => {

            if (event.target.matches('.buttonLogin')) {
                event.preventDefault(); // Varsayılan form gönderimini engelle
                authenticateUser();
            }

            if (event.target.matches('.buttonLogout')) {
                event.preventDefault(); // Varsayılan form gönderimini engelle
                localStorage.removeItem('user');
                document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'; // Token'ı sil
                loadPage('login');
            }

            /*if(event.target.matches('.buttonPpChange')) {
                event.preventDefault();
                updateProfilePicture();
            }*/

            if (event.target.matches('.validateButton')) {
                event.preventDefault(); // Varsayılan davranışı engelle
                const validateButton = event.target;

                const form = document.getElementById('validateForm');
                const formData = new FormData(form);
                const validateCode = formData.get('twofa_code'); // İki faktörlü kodu al
                const token = localStorage.getItem('token'); // Token'ı localStorage'dan al

                validateUser(validateCode, token);
            }

            if(event.target.matches('.updateProfileBtn')) {
                event.preventDefault();
                document.getElementById('updateProfileBtn').addEventListener('click', updateUserInfo);
                console.log('updateProfileBtn');
                // Kullanıcı bilgilerini güncelle
                updateUserInfo()
            }

            if(event.target.matches('.img-fluid')) {
               // event.preventDefault();
                updateProfilePicture();
            }
        });

        

        // Validate butonunun varlığını kontrol et
        
    });

    
}




// Sayfa yüklendiğinde kullanıcı bilgilerini yükle



setupEventListeners();

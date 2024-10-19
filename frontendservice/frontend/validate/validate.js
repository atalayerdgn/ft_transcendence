import { loadPage } from '../router.js';

export async function validateUser() {
    const form = document.getElementById('validateForm');

    if (form) {
        const formData = new FormData(form);
        const data = {};

        formData.forEach((value, key) => {
            data[key] = value;
        });

        const token = localStorage.getItem('token'); // Token'ı localStorage'dan al
        const email = localStorage.getItem('email'); // E-postayı localStorage'dan al
        const validateCode = data["twofa_code"]; // Formdan alınan iki faktörlü kod

        try {
            const response = await fetch('http://localhost:8007/users/validate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`, // Token'ı yetkilendirme başlığına ekle
                },
                body: JSON.stringify({
                    twofa_code: validateCode,
                    email: email
                }),
            });

            if (response.ok) {
                console.log('Başarılı validate');
                // İsteğe bağlı: validate sayfasını yükle
                loadPage('profile'); 
            } else {
                console.log('Başarısız validate');
                loadPage('login');
            }
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }
}
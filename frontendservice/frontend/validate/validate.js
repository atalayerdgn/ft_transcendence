
/*document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('validateForm');
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Varsayılan form gönderimini engelle

        const twofa_code = document.getElementById('twofa_code').value;
        const token = localStorage.getItem('token');
        const email = localStorage.getItem('email');

        try {
            const response = await fetch('http://localhost:8007/users/validate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`, // Token'ı yetkilendirme başlığına ekle
                },
                body: JSON.stringify({
                    email: email,
                    twofa_code: twofa_code
                }),
            });

            if (response.ok) {
                console.log('Başarılı validate'); // Başarılı olduğunda mesaj yazdır
            } else {
                console.log('Başarısız validate'); // Başarısız olduğunda mesaj yazdır
            }
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    });
});*/


document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('click', (event) => {
        if (event.target.matches('validateButton')) {
            event.preventDefault(); // Varsayılan buton davranışını engelle

            const validateCode = document.getElementById('twofa_code').value;
            const token = localStorage.getItem('token');
            const email = localStorage.getItem('email');

            if (!validateCode) {
                console.log('Lütfen validate kodunu girin.');
                return;
            }

            validateUser(email, validateCode, token);
        }
    });
});

async function validateUser(email, validateCode, token) {
    try {
        const response = await fetch('http://localhost:8007/users/validate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify({
                email: email,
                validateCode: validateCode
            }),
        });

        if (response.ok) {
            console.log('Başarılı validate'); // Başarılı olduğunda mesaj yazdır
        } else {
            console.log('Başarısız validate'); // Başarısız olduğunda mesaj yazdır
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

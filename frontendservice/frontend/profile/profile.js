export async function loadUserInfo() {

   /* const storedUser = localStorage.getItem('user');

    if (storedUser) {
        document.getElementById('username').textContent = user.username;
        document.getElementById('user-role').textContent = user.first_name;
        document.getElementById('user-location').textContent = user.email;
        //loadingMessage.style.display = 'none'; // Yükleniyor mesajını gizle
        return;
    }*/

    try {
        const token = document.cookie.split('; ').find(cookie => cookie.startsWith('token=')).split('=')[1]; // Token'ı al
        const response = await fetch('http://localhost:8007/users/username/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`, // Kullanıcının token'ını ekle
            },
        });

        if (response.ok) {
            const user = await response.json();
            
            document.getElementById('username').textContent = user.username; // Kullanıcı adını güncelle
            document.getElementById('user-role').textContent = user.first_name; // Kullanıcı rolünü güncelle
            document.getElementById('user-location').textContent = user.email; // Kullanıcı konumunu güncelle

            const usernameElem = document.getElementById('username');
            if (usernameElem) {
                usernameElem.textContent = user.username;
            } else {
                console.error('Username öğesi bulunamadı.');
            }

            localStorage.setItem('user', JSON.stringify(user)); // Kullanıcı bilgilerini local storage'a kaydet

        } else {
            console.error('Kullanıcı bilgileri yüklenemedi.');
        }
    } catch (error) {
        console.error('Hata:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadUserInfo);

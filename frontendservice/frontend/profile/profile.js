export async function loadUserInfo() {
    try {
        //localde user bilgileri var ise istek atmadan localden user bilgilerini al
        /*const storedUser = localStorage.getItem('user');
        if (storedUser) {
            const userr = JSON.parse(storedUser);

            //bu arada html sayfası yüklenmesi lazım çünkü html sayfası yüklenmeden elementler tanımlanamaz

            document.getElementById('username').textContent = userr.username;
            document.getElementById('user-role').textContent = userr.first_name;
            document.getElementById('user-location').textContent = userr.email;
            //loadingMessage.style.display = 'none'; // Yükleniyor mesajını gizle
            return;
        }*/

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
            
            document.getElementById('first-name').value = user.first_name; // Kullanıcı emailini güncelle
            document.getElementById('last-name').value = user.last_name; // Kullanıcı telefonunu güncelle
            document.getElementById('email').value = user.email; // Kullanıcı emailini güncelle
            document.getElementById('userrname').value = user.username; // Kullanıcı username'ini güncelle

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

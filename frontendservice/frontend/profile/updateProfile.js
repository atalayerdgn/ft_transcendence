export async function updateUserInfo() {
    const firstName = document.getElementById('first-name').value;
    const lastName = document.getElementById('last-name').value;
    const email = document.getElementById('email').value;
    const username = document.getElementById('userrname').value;
    const currentUserName = JSON.parse(localStorage.getItem('user')).username;
    const token = document.cookie.split('; ').find(cookie => cookie.startsWith('token=')).split('=')[1]; // Token'ı al
    console.log('token:', token);
    console.log('currentUserName:', currentUserName);
    const response = await fetch('http://localhost:8007/users/update/', {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token}`, // Kullanıcının token'ını ekle
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            current_username: currentUserName,
            first_name: firstName,
            last_name: lastName,
            email: email,
            username: username,
        }),
    });
    
    if (response.ok) {
        const result = await response.json();
        console.log('Profile updated:', result);
        
        // Assuming the new token is returned in the response
        const newToken = result.token;
        document.cookie = `token=${newToken}; path=/; max-age=1500`; 
        localStorage.setItem('user', JSON.stringify(result));

        document.getElementById('username').textContent = result.username; // Kullanıcı adını güncelle
        document.getElementById('user-role').textContent = result.first_name; // Kullanıcı rolünü güncelle
        document.getElementById('user-location').textContent = result.email; // Kullanıcı konumunu güncelle 
        document.getElementById('first-name').value = result.first_name; // Kullanıcı emailini güncelle
        document.getElementById('last-name').value = result.last_name; // Kullanıcı telefonunu güncelle
        document.getElementById('email').value = result.email; // Kullanıcı emailini güncelle
        document.getElementById('userrname').value = result.username; // Kullanıcı username'ini güncel
         // Kaydedilen veriyi kontrol et
        const storedUser = JSON.parse(localStorage.getItem('user'));
        console.log('Stored user:', storedUser); // Bu satırda veriyi kontrol edebilirsiniz

    } else {
        console.error('Profile update failed.');
    }
}


// Profil resmini güncelleme fonksiyonu
// Profil resmini güncelleme fonksiyonu
export async function updateProfilePicture() {
    console.log('updateProfilePicture function called');

    const fileInput = document.getElementById('file-input');
    
    // Dosya seçildiyse işlemi başlat
    fileInput.click(); // Dosya input'unu tetikle

    // Dosya input'unun değiştiğini kontrol et
    fileInput.addEventListener('change', async (event) => {
        const file = event.target.files[0];  // Seçilen dosya
        if (file) {
            const formData = new FormData();
            formData.append('profile_picture', file);  // Dosyayı formData'ya ekle

            // Bearer token (Örnek: localStorage'dan alınıyor)
            const token = localStorage.getItem('access_token'); // Token'ı buradan alıyoruz

            // Fetch ile dosyayı sunucuya gönder
            try {
                const response = await fetch('/upload-avatar/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Authorization': `Bearer ${token}`, // Bearer token'ı başlığa ekle
                    },
                });

                if (response.ok) {
                    const data = await response.json(); // Backend'den dönen yanıtı al
                    console.log('Başarıyla yüklendi:', data);
                    // Yeni profil resmini güncelle
                    document.getElementById('avatar-img').src = data.new_avatar_url;
                } else {
                    console.error('Yükleme başarısız:', response.status);
                }
            } catch (error) {
                console.error('Hata oluştu:', error);
            }
        }
    });
}



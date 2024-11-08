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


export async function updateProfilePicture() {
    console.log('updateProfilePicture function called');

    const fileInput = document.getElementById('file-input');
    const changePPButton = document.getElementById('change-pp-btn');

    console.log('fileInput:', fileInput);
    console.log('changePPButton:', changePPButton);
    
    // Dosya yüklendiğinde dosya seçme ekranını aç
    changePPButton.addEventListener('click', () => {
        console.log('changePPButton clicked2');
        console.log(fileInput.click());
        fileInput.click();
    });
}


// <!-- w---------------------------------------------------------- -->


// <!-- w---------------------------------------------------------- -->

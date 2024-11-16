import { loadUserInfo } from './profile/profile.js';
import { loadFriendList } from './profile/profile.js';

export async function loadPage(page) {
    const content = document.getElementById('content');
    const pageMap = new Map([
        ['login', 'login/login.html'],
        ['register', 'register/register.html'],
        ['validate', 'validate/validate.html'],
        ['registerlogin', 'login/login.html'],
        ['forgot', 'forgot/forgot.html'],
        ['profile', 'profile/profile.html'],
        ['about', 'about/about.html'],
        ['logout', 'login/login.html'],
        ['settings', 'settings/settings.html'],
        ['game', 'game/game.html'],
        ['send', 'forgot/forgot.html'],
    ]);

    // URL'yi al ve geçerli değilse 404 sayfasına yönlendir
    let pageUrl = pageMap.get(page) || '404/404.html';
    console.log('Page:', page, 'URL:', pageUrl);
    try {
        if (page === 'loginWith42') {
            return; // Bu durumda herhangi bir işlem yapılmaz
        }
        
        const response = await fetch(pageUrl);
        if (!response.ok) {
            throw new Error(`Failed to load page: ${response.statusText}`);
        }

        // Profil sayfası yükleniyorsa, kullanıcı bilgilerini yükle
        if (page === 'profile') {
            content.innerHTML = await response.text();
            loadUserInfo(); // Kullanıcı bilgilerini yükler
            loadFriendList();
            return;
        }

        // Diğer sayfalar için içerik yükle
        content.innerHTML = await response.text();
    } catch (error) {
        content.innerHTML = `<p>Error loading page: ${error.message}</p>`;
    }
}

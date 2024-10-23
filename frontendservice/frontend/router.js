import { loadUserInfo } from './profile/profile.js';

export async function loadPage(page) {
    let pageUrl = '';
    //let scriptUrl = '';
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

    pageUrl = pageMap.get(page);
    // Geçerli bir sayfa yoksa 404 sayfasını yükleyin
    if (!pageUrl) {
        pageUrl = '404/404.html';
    
}
    try {
        if (page == 'loginWith42') {

        } else {
            const response = await fetch(pageUrl);
            if (!response.ok) {
                throw new Error(`Failed to load page: ${response.statusText}`);
            }
            
            // Eğer profile sayfası yükleniyorsa html yüklendikten sonra js çalışır çünkü 3g hızında önce js çalışıyor ve html 
            // yüklenmeden js çalıştığı için html'de bulunan elementler tanımlanamıyor hata veriyor. Bu yüzden profile sayfası
            // yüklenirken kullanıcı bilgileri doldurulmuyor
            if (pageUrl === 'profile/profile.html') {
               // import('./profile/profile.js')
                content.innerHTML = await response.text();
                 // İçindeki fonksiyonu çağır
                //await module.loadUserInfo();
                loadUserInfo();
                return;
            }
            content.innerHTML = await response.text();
        }

        /*if (scriptUrl) {
            const script = document.createElement('script');
            script.src = scriptUrl;
            script.type = "module";
            document.body.appendChild(script);
        }*/
    } catch (error) {
        content.innerHTML = `<p>Error loading page: ${error.message}</p>`;
    }
}

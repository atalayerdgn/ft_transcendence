import { fetchMatchHistory, loadUserInfo } from './profile/profile.js';
import { loadFriendList } from './profile/profile.js';
import { game } from './game/game.js';

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
        
        const response = await fetch(pageUrl);
        if (!response.ok) {
            throw new Error(`Failed to load page: ${response.statusText}`);
        }
        
         // response.text() çağrısını yalnızca bir kez yapın
        
        // Profil sayfası yükleniyorsa, kullanıcı bilgilerini yükle
        if (page === 'profile') {
            const pageContent = await response.text();
            content.innerHTML = pageContent;
            await loadUserInfo(); // Kullanıcı bilgilerini yükler
            await loadFriendList();
            await fetchMatchHistory();
            return;
        }
        
        if (page === 'game') {
            const pageContent = await response.text();
            content.innerHTML = pageContent;

                // CSS dosyasını yükle
                const link = document.createElement('link');
                link.rel = 'stylesheet';
                link.href = './game/game.css'; // CSS dosyasının doğru yolunu belirtin
                document.head.appendChild(link);
        
                const script = document.createElement('script');
                script.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
                script.onload = () => {
                console.log('Three.js loaded');
        
                const script2 = document.createElement('script');
                script2.src = 'https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js';
                script2.onload = () => {
                    console.log('OrbitControls.js loaded');
        
                };
                document.head.appendChild(script2);
            };
            document.head.appendChild(script);

            // .startAgaintsAnotherPlayerGame butonunun tıklama dinleyicisini eklemeden önce kaldır
            const button = document.querySelector(".startAgaintsAnotherPlayerGame");
            button.removeEventListener("click", startGameWithPlayer);
            button.addEventListener("click", startGameWithPlayer);

            return;
        }
        //const pageContent = await response.text();

        // Diğer sayfalar için içerik yükle
        content.innerHTML = await response.text();
    } catch (error) {
        content.innerHTML = `<p>Error loading page: ${error.message}</p>`;
    }
}


export function startGameWithPlayer() {
    const existingCanvas = document.querySelectorAll('canvas');
    existingCanvas.forEach(canvas => canvas.remove());
    game();
    var button = document.querySelector(".startAgaintsAnotherPlayerGame");
    button.style.display = "none";
    document.querySelector(".startAgainstArtificalIntelligenceGame").style.display = "none";
}


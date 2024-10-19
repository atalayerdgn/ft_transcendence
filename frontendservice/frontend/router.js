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

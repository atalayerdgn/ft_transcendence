export async function loadPage(page) {
    const content = document.getElementById('content');
    let pageUrl = '';
    let scriptUrl = '';

    switch (page) {
        case 'login':
            pageUrl = '/static/login/login.html';  // Doğru yol
            scriptUrl = '/static/login/login.js';  // Doğru yol
            break;
        case 'register':
            pageUrl = '/static/register/register.html';
            scriptUrl = '/static/register/register.js';
            break;
        case 'registerlogin':
            pageUrl = '/static/login/login.html';
            scriptUrl = '/static/register/register.js';
            break;
        case 'forgot':
            pageUrl = '/static/forgot/forgot.html';
            break;
        case 'profile':
            pageUrl = '/static/profile/profile.html';
            break;
        case 'about':
            pageUrl = '/static/about/about.html';
            break;
        case 'logout':
            pageUrl = '/static/login/login.html';
            scriptUrl = '/static/login/login.js';
            break;
        case 'settings':
            pageUrl = '/static/settings/settings.html';
            break;
        case 'game':
            pageUrl = '/static/game/game.html';
            break;
        case 'send':
            pageUrl = '/static/forgot/forgot.html';
            break;
        default:
            pageUrl = '/static/404/404.html';
    }

    try {
        const response = await fetch(pageUrl);
        if (!response.ok) {
            throw new Error(`Failed to load page: ${response.statusText}`);
        }
        const html = await response.text();
        content.innerHTML = html;

        if (scriptUrl) {
            const script = document.createElement('script');
            script.src = scriptUrl;
            document.body.appendChild(script);
        }

    } catch (error) {
        content.innerHTML = `<p>Error loading page: ${error.message}</p>`;
    }
}

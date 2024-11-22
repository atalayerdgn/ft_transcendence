export class User {
    constructor(data) {
        this.id = data.id;
        this.username = data.username;
        this.firstName = data.first_name;
        this.lastName = data.last_name;
        this.email = data.email;
        this.avatar = data.avatar;
        this.isOnline = data.is_online;
        this.winCount = data.win_count;
        this.lossCount = data.loss_count;
    }
}

const quotes = [
    "Hayat, ne kadar uzun olursa olsun, anı yaşamakla güzelleşir.",
    "Her yeni başlangıç, eski bir sonu işaret eder.",
    "Düşe kalka yürürken, her adım bir ders bırakır.",
    "Zorluklar, gücün keşfidir.",
    "İleriye bakarken geçmişi unutma, çünkü geçmişten ders alırsın.",
    "Başarı, pes etmeyenlerin ödülüdür.",
    "Kimseyi olduğu gibi kabul et, kendini olduğun gibi sev.",
    "En karanlık an, en parlak ışığın doğduğu andır.",
    "Mutluluk, paylaşılınca artar.",
    "İnsan, sevdiği kadar değerli olur.",
    "Kendi yolunu çiz, başkalarının izinden gitme.",
    "Bazen kaybetmek, kazanmanın ilk adımıdır.",
    "Her şey zamanla güzelleşir, sabır her şeyin ilacıdır.",
    "Gerçek gücün, düşerken değil, kalkarken gösterilir.",
    "İyi bir insan olmak, her şeyden daha önemlidir.",
    "İnsan, ne düşündüğünü söyler; ama ne yaptığı, kim olduğunu gösterir.",
    "Sabır, acının içindeki huzurdur.",
    "Hata yapmak, öğrenmenin en güzel yoludur.",
    "Geçmişin yükünden kurtul, geleceği kucakla.",
    "Yalnızca düşünmek yetmez, eyleme geçmek gerekir.",
    "Başarı, ne kadar yükseğe tırmandığın değil, ne kadar sağlam durduğundur.",
    "Gerçek zenginlik, sahip olduklarında değil, paylaştıklarında gizlidir.",
    "Hayatta en değerli şey, kaybetmediklerin değil, kazandıklarındır.",
    "Ne olursa olsun, her zaman en iyi versiyonunu sergile.",
    "Bazen en güzel hikayeler, kelimelerle anlatılmaz.",
    "İyi insanlar, kalpleriyle konuşurlar.",
    "İç huzur, dış dünyadan bağımsızdır.",
    "Her son, yeni bir başlangıçtır.",
    "İnsanlar hatalarını sevdiklerinden öğrenir.",
    "Hayat, cesaret isteyen bir yolculuktur.",
    "Olumsuz düşünceler, ruhunu karartır.",
    "Sadece kendin ol, başkası olma.",
    "Bir insanın değeri, sahip olduğu değil, paylaştığı şeylerle ölçülür.",
    "Zihnin huzuru, kalbin özgürlüğüdür.",
    "Gözler, ne kadar uzağa bakarsa baksın, kalp her zaman en yakın olanı arar.",
    "Senin için yapabileceğim tek şey, kendi yolunu bulmana yardımcı olmaktır.",
    "Güzel bir şeyin değerini anlamadan önce, onu kaybetme.",
    "İnsan, ne kadar az ile yetinirse, o kadar çok mutlu olur.",
    "Asıl zenginlik, insanın içindedir.",
    "Kendini bilmek, dünyayı anlamanın başlangıcıdır.",
    "Gelişmek, geçmişi bırakıp geleceğe adım atabilmektir.",
    "Huzur, dış dünyada değil, iç dünyada bulunur.",
    "Zorluklar, güçlü insanları yaratır.",
    "Zamanın kıymetini, kaybetmeden önce anlayamazsınız.",
    "Hayatın en güzel anları, en basit olanlardır.",
    "Her şeyin bir zamanı vardır, sabırla bekle.",
    "En büyük başarı, içsel huzuru bulmaktır.",
    "İnsan, kalbiyle duyduğunu aklıyla anlamaya çalışır.",
    "Gerçek arkadaşlar, zor zamanlarda yanındakilerdir.",
    "Hayat, bir yolculuktur; her adım bir derstir.",
    "Kendine inan, her şey mümkün olur.",
    "En güçlü silah, sevgiyle dolu bir kalptir.",
    "Kendi değerini bil, başkalarının düşüncelerine göre yaşamayı bırak.",
    "Her gün, bir fırsattır.",
    "Zorluklar, cesur insanları bulur.",
    "Başarı, sabır ve azimle şekillenir.",
    "Güzel bir hayat, güzel bir bakış açısıyla başlar.",
    "En değerli şey, zamanını nereye harcadığındır.",
    "İnsan ne kadar basit yaşarsa, o kadar mutlu olur.",
    "Bazen, en büyük başarı sabırlı olmak ve beklemektir.",
    "İleriye doğru attığın her adım, seni bir adım daha yaklaştırır.",
    "Sevgiyi hissetmek, en büyük lüksdür.",
    "Kendine güven, dünya seninle olacaktır.",
    "Bir insanı anlayabilmek için, onun yerine koyarak düşünmelisin.",
    "Hayatta en önemli şey, başkalarına nasıl hissettirdiğindir.",
    "İçindeki gücü keşfet, seni kimse durduramaz.",
    "Zaman, en değerli hazinedir; ona dikkat et.",
    "Gerçek başarı, başkalarını mutlu etmekten gelir.",
    "Sevgi, bir insanın içindeki en güçlü kuvvettir.",
    "Başarı, sadece elde edilen sonuçlarla değil, verilen emekle ölçülür.",
    "Her şey geçer, ama anılar kalır.",
    "Kendi yolunu bulmak, en değerli yolculuktur.",
    "Hayatta kalmak yetmez, yaşamak gerekir.",
    "Başkalarına iyi davranmak, insanın kalbini hafifletir.",
    "Zihnindeki karışıklıklar, dünyanı karartır.",
    "Gerçek güç, sabır ve anlayışla gelir.",
    "Her gün bir adım daha at, ilerlemek için.",
    "Güçlü olmak, her zaman kolay olmasa da gereklidir.",
    "Olumsuzluklar, yalnızca geçici engellerdir.",
    "Hayatını başkaları için değil, kendin için yaşa.",
    "Sevgi ve hoşgörü, her şeyin ilacıdır.",
    "İnsan, hatalarıyla büyür.",
    "Gerçek dostluk, zorluklarda kendini gösterir.",
    "Mutluluk, her anı değerlendirebilmektir.",
    "Kendini olduğun gibi sev, dışarıdan onay bekleme.",
    "İçindeki iyiliği bul, dünya buna ihtiyaç duyuyor.",
    "Gerçek zafer, başkalarına yardım etmekle gelir.",
    "Her şeyin bir nedeni vardır, sabırlı ol.",
    "Kendini tanımadan, dünyayı tanıman mümkün değildir.",
    "Hayatta en değerli şey, doğru zamanda doğru yerde olmaktır.",
    "Düşüncelerini doğru yönlendir, hayatın değişsin.",
    "Kendi sınırlarını aşmak, en büyük başarıdır.",
    "Mutluluğun sırrı, küçük şeylerde saklıdır.",
    "Geçmişe takılmak, geleceği görmene engel olur.",
    "Hayat, bir seçimdir; her gün yeni bir fırsattır.",
    "Güçlü kalabilmek, her şeyin üstesinden gelmek demektir.",
    "Hatalar, insanı olgunlaştırır.",
    "Hayatını değiştirmek istiyorsan, önce düşüncelerini değiştir.",
    "Her şey zamanla gelir, sabırlı ol.",
    "Kendin ol, çünkü başkası olmanın bir anlamı yok."
];

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
        const user_id = localStorage.getItem('user_id'); // User id'yi al
        console.log('loaduserinfouserid:', user_id);
        const response = await fetch('http://localhost:8007/users/username/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`, // Kullanıcının token'ını ekle
                'id': user_id, // Kullanıcının id'sini ekle
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
            document.getElementById('avatar-img').src = `.${user.avatar}`; // Kullanıcı profil resmini güncelle

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
        return; // token olmadığında console.error hatası vermesin diye return ekledim	
        console.error('Hata:', error);
    }
}

export async function showRandomQuote() {
    const randomIndex = Math.floor(Math.random() * quotes.length);
    const randomQuote = quotes[randomIndex];
    document.getElementById('quote').textContent = randomQuote;
}

export async function loadFriendList() {
    const friendListContainer = document.getElementById('friend-list');
    const matchHistoryList = document.getElementById('match-history-list');
    const userId = JSON.parse(localStorage.getItem('user')).id;
    const friendListUrl = `http://localhost:8007/friend/friend-list/?user_id=${userId}`;
    const token = document.cookie.split('; ').find(cookie => cookie.startsWith('token=')).split('=')[1];

    let users;
    try {
        // İlk fetch işlemi
        const usersResponse = await fetch('http://localhost:8007/users/list/', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'id': userId
            }
        });
        const usersData = await usersResponse.json();
        users = usersData.map(user => new User(user));
        console.log('All users:', users);

        // İkinci fetch işlemi
        const friendResponse = await fetch(friendListUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'id': userId
            },
        });

        if (friendResponse.ok) {
            const friendList = await friendResponse.json();
            console.log('Friend list:', friendList);

            friendList.forEach(friend => {
                const friendUser = users.find(user => user.id === friend.second_user_id);
                console.log('Friend user:', friendUser);

                const friendListItem = document.createElement('li');
                friendListItem.classList.add('list-group-item', 'd-flex', 'align-items-center', 'friend-item');

                const avatar = document.createElement('img');
                avatar.src = friendUser.avatar; // User sınıfından gelen avatar URL'si
                avatar.className = 'rounded-circle me-3';
                avatar.style.width = '40px';
                avatar.style.height = '40px';


                const usernameSpan = document.createElement('span');
                usernameSpan.classList.add('fw-bold', 'ml-2');
                usernameSpan.textContent = friendUser.username;

                //kullanıcıların online durumunu belirten işareti ekle
                const onlineStatus = document.createElement('span');
                onlineStatus.className = friendUser.isOnline ? 'badge bg-success ms-auto' : 'badge bg-secondary ms-auto';
                onlineStatus.textContent = friendUser.isOnline ? 'Online' : 'Offline';


                friendListItem.appendChild(avatar);
                friendListItem.appendChild(usernameSpan);
                friendListItem.appendChild(onlineStatus);
                friendListContainer.appendChild(friendListItem);
            }
            );
        } else {
            console.error('Failed to fetch friend list:', friendResponse.status);
        }
    } catch (error) {
        console.error('Error occurred:', error);
    }
}

export async function fetchMatchHistory() {
    const token = document.cookie.split('; ').find(cookie => cookie.startsWith('token=')).split('=')[1]; // Token'ı al
    const username = JSON.parse(localStorage.getItem('user')).username; // User id'yi al
    const user_id = JSON.parse(localStorage.getItem('user')).id; // User id'yi al

    try {
        //const response = await fetch(`http://127.0.0.1:8005/game/list/?user_name=${userId}`);

        const response = await fetch(`http://localhost:8007/game/list/?user_name=${username}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'id': user_id,
            },
        });

        const matchHistory = await response.json();

        const matchHistoryList = document.getElementById('match-history-list');
        matchHistoryList.innerHTML = ''; // Önceki içeriği temizle

        matchHistory.forEach(match => {
            const listItem = document.createElement('li');
            listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
            listItem.style.marginTop = '4px';
            listItem.style.marginBottom = '2px';
            listItem.style.borderRadius = '20px'; // Köşeleri yuvarla
            listItem.style.backgroundColor = '#2c3e50'; // Arka plan rengini ayarla
            listItem.style.border = '1px solid #34495e'; // Kenarlık rengini ayarla
            const matchInfo = document.createElement('span');
            const userColor = match.player_one_score > match.player_two_score ? 'green' : 'red';
            const opponentColor = match.player_one_score > match.player_two_score ? 'red' : 'green';
            matchInfo.innerHTML = `<strong style="color: ${match.player_one_score > match.player_two_score ? 'green' : 'red'};">${username}</strong>: ${match.player_one_score},  -  ${match.player_two_score}, düşman <strong style="color: ${match.player_two_score > match.player_one_score ? 'green' : 'red'};">${match.user_two_name}</strong>`;

            const matchDate = document.createElement('span');
            matchDate.textContent = new Date(match.match_date).toLocaleString();
            matchDate.style.fontSize = '0.8em'; // Yazı boyutunu küçült
            matchDate.style.color = 'white'; // Metin rengini ayarla

            listItem.appendChild(matchInfo);
            listItem.appendChild(matchDate);
            matchHistoryList.appendChild(listItem);
        });
    } catch (error) {
        console.error('Error fetching match history:', error);
    }
}

// Sayfa yüklendiğinde maç geçmişini getir

document.addEventListener('DOMContentLoaded', loadUserInfo);

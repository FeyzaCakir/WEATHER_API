🌦️ Flask Weather App with Firebase Authentication

Bu proje, Flask tabanlı bir web uygulaması olarak geliştirilmiştir.
Kullanıcılar Firebase Authentication ile kayıt olup giriş yaptıktan sonra;

Ülke

Eyalet / Bölge

Şehir

seçimi yaparak OpenWeatherMap API üzerinden anlık hava durumu bilgilerini görüntüleyebilir.

Proje, staj sürecinin başında authentication, çoklu API entegrasyonu ve form tabanlı veri akışı konularını öğrenmek amacıyla geliştirilmiştir.

🎯 Projenin Amacı

Flask ile kullanıcı girişli bir web uygulaması geliştirmek

Firebase Authentication kullanarak register / login / logout akışını kurmak

Birden fazla harici API ile çalışmayı öğrenmek

Backend tarafında dinamik form zinciri (country → state → city) mantığını uygulamak

API’den gelen verileri template’lere güvenli şekilde aktarmak

🧩 Kullanılan Teknolojiler

Python

Flask

Flask-WTF (Form validation)

Firebase Admin SDK

Pyrebase

OpenWeatherMap API

Country State City API

HTML / Jinja2

dotenv

🔐 Authentication Yapısı (Firebase)

Bu projede kullanıcı kimlik doğrulama işlemleri Firebase Authentication ile yapılmıştır.

Register

Firebase Admin SDK kullanılarak kullanıcı oluşturulur

Login

Kullanıcı varlığı Firebase Admin ile kontrol edilir

Şifre doğrulaması Pyrebase üzerinden yapılır

Başarılı girişte kullanıcı email’i Flask session içinde tutulur

Logout

Session temizlenerek kullanıcı çıkış yapar

🌍 Ülke – Şehir Seçim Mantığı

Kullanıcı arayüzünde zincirleme seçim yapısı uygulanmıştır:

Ülke seçilir

Seçilen ülkeye göre eyaletler yüklenir

Seçilen eyalete göre şehirler yüklenir

Seçilen şehir için hava durumu getirilir

Bu yapı backend tarafında şu API’lerle sağlanır:

Country State City API

OpenWeatherMap API

🌤️ Hava Durumu Bilgisi

Şehir adı OpenWeatherMap API’ye gönderilir

API’den dönen veriler:

Sıcaklık

Hava durumu açıklaması

Nem, hissedilen sıcaklık vb.

Veriler metric birimde ve Türkçe olarak alınır

📂 Proje Dosya Yapısı
├── app.py
├── templates/
│   ├── login.html
│   ├── register.html
│   └── home.html
├── .env
└── requirements.txt

⚙️ Kurulum ve Çalıştırma
1️⃣ Gerekli Paketler
pip install flask flask-wtf firebase-admin pyrebase4 python-dotenv requests

2️⃣ Ortam Değişkenleri (.env)
SECRET_KEY=your_secret_key

API_KEY=firebase_api_key
AUTH_DOMAIN=...
PROJECT_ID=...
DATABASE_URL=...

WEATHER_API_KEY=openweather_api_key
COUNTRY_API_KEY=country_state_city_api_key

3️⃣ Firebase Ayarları

Firebase Console’dan Service Account JSON alınmalı

Bu dosya .gitignore içinde olmalı

credentials.Certificate() ile projeye tanıtılmalı

4️⃣ Uygulamayı Çalıştır
python app.py

🧠 Öğrenilen / Pekiştirilen Konular

Flask routing ve template rendering

Form validation (Flask-WTF)

Firebase Authentication mantığı

Session yönetimi

Çoklu API entegrasyonu

Dinamik form veri akışı

Backend → frontend veri aktarımı

🔮 Geliştirme Fikirleri

Kullanıcıya özel şehir favorileri

API çağrıları için caching

Yetkilendirme (login olmadan erişimi engelleme)

UI tarafında async (AJAX) form güncellemeleri

📌 Not:
Bu proje, staj sürecimin başında geliştirdiğim öğrenme odaklı bir çalışmadır.
Amaç, backend temellerini ve authentication + API entegrasyonlarını pratiğe dökmektir.

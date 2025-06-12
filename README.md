# Limon Forum Project 🍋

Limon Forum, Django 3.1.12 ile geliştirilmiş ve MongoDB ile çalışan, dört farklı kategoriden (oyun, film, dizi, kitap) içeriklerin harici API'den çekilip görüntülendiği ve kullanıcıların bu içeriklere yorum bırakabildiği bir forum uygulamasıdır.

## 🚀 Proje Amaçları

- API'den gelen medya içeriklerini dinamik olarak web arayüzünde listelemek.
- Kullanıcıların yorum yapabildiği, oturum açabildiği ve etkileşimde bulunabildiği bir sosyal yapı kurmak.
- Django ile MongoDB kullanarak klasik SQL yerine NoSQL altyapısı üzerinde çalışmak.

## 🌐 Öne Çıkan Özellikler

- ✨ Modern ve temiz arayüz (Django templates)
- 🔐 Giriş / Kayıt sistemi
- 🔍 Slug tabanlı içerik detay sayfaları
- 📃 Yorum ekleme ve listeleme
- 🪧 Resim yüklenebilir yorumlar

## 📚 Kullanım

### 1. Ana Sayfa
- Harici API'den gelen oyun, film, dizi ve kitaplar listelenir.

### 2. Detay Sayfası
- `/single/<kategori>/<slug>` formatında oluşan sayfalarda içerik detayları görüntülenir.
- Kullanıcı giriş yapmışsa yorum ekleyebilir.

### 3. Admin Paneli
- Yönetici kullanıcılar içerikleri ve yorumları yönetebilir.

## 🗂️ Proje Dizin Yapısı

```plaintext
limonforum/
├── accounts/         # Kullanıcı oturumu, giriş/ kayıt/ şifre işlemleri
├── forum/            # API'den gelen içeriklerin detayları ve yorumlar
├── static/           # Statik dosyalar (CSS/JS)
├── templates/        # Tüm HTML dosyaları
├── uploads/          # Kullanıcı yorumlarında yüklenmiş görseller
├── limonforum/       # Ana proje ayarları, URL routing
│   ├── settings.py   # .env ile ayarlar
│   ├── urls.py       # URL konfigürasyonu
│   └── wsgi.py       # WSGI uyumluluğu için
├── requirements.txt  # Tüm Python paketleri
└── .env              # Gizli ayarlar (gönderilmez)
```

## 📄 Önemli Paketler

- **Django 3.1.12** – Web framework
- **Djongo** – Django ORM ile MongoDB kullanabilme
- **Pillow** – Resim işlemleri
- **python-decouple** – Ortam değişkenleri yönetimi

## 🛠️ Geliştirici Notları

- API'den gelen veriler sadece frontend'de görüntülenir, veritabanında saklanmaz.
- `slug` yapısı kategoriye göre farklılaşır. Örnek: `/single/game/gta-v`, `/single/book/1984`

---

📑 Hazırlayan: **Alperen Aktaş, Bora Kalkan, Mehmet Miraç Özmen**  
🎓 Fırat Üniversitesi Bilgisayar Mühendisliği

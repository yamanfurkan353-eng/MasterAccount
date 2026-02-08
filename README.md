# MasterAccount — Masaüstü Muhasebe Uygulaması

Modern, şık ve kullanımı kolay; Windows 11 stili arayüzü ile Python tabanlı masaüstü muhasebe uygulaması.

## 📋 Özellikler

✅ **Dashboard** - Anlık gelir, gider ve bakiye gösterimi
✅ **Gelir/Gider Yönetimi** - Detaylı kayıt ekleme, listeleme ve silme
✅ **Müşteri Yönetimi** - Müşteri bilgilerini düzenle ve sakla
✅ **Koyu Tema** - Göz yormayan modern Windows 11 stil arayüz
✅ **Yerel Veritabanı** - Veriler güvenli şekilde lokal olarak saklanır
✅ **Portable** - Kurulum gerektirmez, direkt çalıştırılabilir

---

## 🖥️ Windows'ta Kurulum ve Çalıştırma

### ⚡ Hızlı Başlangıç (Önerilen)

**Portable Executable İndirme ve Çalıştırma:**
- Releases kısmından `MasterAccount.exe` dosyasını indirin
- Çift tıklayarak çalıştırın — başka bir şey gerekmez!

### 📦 Python ile Manuel Kurulum

**Gereksinimler:**
- Windows 10 / Windows 11
- Python 3.9+ (https://www.python.org/downloads/)

**Adım 1: Depoyu İndir**
```bash
git clone https://github.com/yamanfurkan353-eng/MasterAccount.git
cd MasterAccount
```

**Adım 2: Sanal Ortam Oluştur**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Adım 3: Bağımlılıkları Kur**
```bash
pip install -r requirements.txt
```

**Adım 4: Uygulamayı Başlat**
```bash
python main.py
```

---

## 💻 Kullanım Kılavuzu

### 📊 Dashboard
- Toplam gelir, gider ve hesap bakiyesini görüntüleyin
- Ekranı yenilemek için tıklayın (Gelir/Gider sayfasında değişiklik sonrası otomatik güncellenir)

### 💰 Gelir/Gider Sayfası
1. **Tür Seçin:** "Gelir" veya "Gider"
2. **Tarih Girin:** Varsayılan olarak bugün ayarlanmıştır
3. **Açıklama Ekleyin:** İşlem hakkında kısa not (örn: "Danışmanlık hizmeti")
4. **Tutar Girin:** Paranın miktarını Türk Lirası cinsinden yazın
5. **Kaydet:** Kaydı veritabanına ekler

**Kaydları Silme:**
- Silinecek kaydı tabloda seçin
- "Sil" butonuna tıklayın

### 👥 Müşteriler Sayfası
1. **Müşteri Adı Girin:** Şirket veya kişi adı
2. **İletişim Ekleyin:** Telefon numarası, e-mail vb.
3. **Notlar:** Opsiyonel ek bilgiler
4. **Ekle:** Müşteriyi kaydeder

**Müşteriyi Silme:**
- Müşteri seçin → "Sil" butonuna tıklayın

### ⚙️ Ayarlar
- Uygulamaya ait bilgileri görüntüleyin
- "Tüm Verileri Sil" butonuyla veritabanını sıfırlayabilirsiniz (dikkatli kullanın!)

---

## 📁 Dosya Yapısı

```
MasterAccount/
├── main.py                 # Ana uygulama dosyası
├── requirements.txt        # Python bağımlılıkları
├── data.db                 # Veritabanı (ilk çalıştırmada oluşturulur)
├── README.md              # Bu dosya
└── .gitignore             # Git tarafından görmezden gelinecek dosyalar
```

---

## 🔧 Taşınabilir EXE Oluşturma (PyInstaller)

Eğer Windows için portable `.exe` dosyası oluşturmak istiyorsanız:

**Adım 1: PyInstaller Yükle**
```bash
.venv\Scripts\activate
pip install pyinstaller
```

**Adım 2: Executable Oluştur**
```bash
pyinstaller --onefile --windowed --name MasterAccount main.py
```

Executable dosya `dist/` klasöründe `MasterAccount.exe` olarak oluşturulur.

---

## 📊 Veritabanı

Veriler `data.db` adlı SQLite veritabanında saklanır. Bu dosya uygulamanın bulunduğu dizinde otomatik olarak oluşturulur.

**Tablolar:**
- `incomes` — Gelir kayıtları (id, date, description, amount)
- `expenses` — Gider kayıtları (id, date, description, amount)
- `customers` — Müşteri bilgileri (id, name, contact, notes)

---

## 🐛 Sorun Giderme

### Python kurulu değil
→ https://www.python.org/downloads/ adresinden Python 3.9+ sürümünü indirin

### `ModuleNotFoundError: No module named 'customtkinter'`
```bash
pip install -r requirements.txt
```

### Uygulama açılmıyor
- Windows Defender güvenlik uyarısı alırsa "Diğine devam et" seçeneğini tıklayın
- Veritabanı kilit problemiyse `data.db` dosyasını silip yeniden çalıştırın

---

## 📝 Lisans

Tüm Hakları Saklıdır © 2026. Kişisel ve ticari kullanım için liberte.

---

## 📧 İletişim ve Destek

Herhangi bir sorunuz veya öneriniz varsa, lütfen issue oluşturunuz.

---

**Hoşça kalın! 🎉**
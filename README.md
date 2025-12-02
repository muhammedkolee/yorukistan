# 📡 Yörükistan — Pi Pico W Akıllı Sensör Ağı

Bu proje, **Dr. Ögr. Üyesi Hasan Serdar** hocanın **Kablosuz Ağ Teknolojileri** dersi kapsamında geliştirilmiştir.  
Amaç, **Raspberry Pi Pico W** kartı ile çeşitli sensörlerden alınan verileri **Telegram botu** aracılığıyla uzaktan izleyebilmek ve kontrol edebilmektir.

---

## 👩‍💻 Geliştirici Ekip

| Ad Soyad | Öğrenci No |
|-----------|-------------|
| Kübra Kolay | 22370031008 |
| Esra Abanoğlu | 22370031067 |
| Büşra Bozdoğan | 22370031054 |
| Yahya Kaya | 22370031036 |
| Deniz Erol | 22370031042 |
| Muhammed Köle | 22370031003 |
| Davut Balasar | 22370031004 |
| Fatih Arslanol | 20370031085 |

---

## ⚙️ Proje Özeti

Bu proje, **Raspberry Pi Pico W** mikrodenetleyicisi üzerinde çalışan bir **IoT tabanlı sensör ağı** uygulamasıdır.  
Pico W, bağlı olduğu sensörlerden verileri toplar ve Telegram botu üzerinden kullanıcıyla etkileşime geçer.

Telegram üzerinden gönderilen komutlar ile:
- Sensör verileri sorgulanabilir (sıcaklık, nem, gaz durumu, su algılama),
- LED kontrolü yapılabilir,
- Hareket, gaz veya su algılandığında otomatik bildirim alınabilir.

---

## 🔌 Kullanılan Donanımlar

| Donanım | Açıklama | GPIO Pin |
|----------|-----------|-----------|
| **DHT11** | Sıcaklık ve Nem Sensörü | 17 |
| **PIR Sensörü** | Hareket algılama | 16 |
| **MQ-2** | Gaz ve Duman Sensörü | 18 |
| **Yağmur / Su Sensörü** | Su algılama | 19 |
| **LED** | Uyarı ışığı | 20 |

---

## 🧠 Yazılım Bileşenleri

Proje aşağıdaki MicroPython modüllerini kullanmaktadır:

- `network` — Wi-Fi bağlantısı oluşturur  
- `urequests` — Telegram API üzerinden veri alışverişi yapar  
- `dht` — DHT11 sensöründen sıcaklık ve nem verisi okur  
- `machine` — GPIO pin kontrolü sağlar  
- `time` — Gecikme ve zamanlama işlemleri

---

## 💬 Telegram Bot Entegrasyonu

Proje, kullanıcı etkileşimi için Telegram Bot API’sini kullanır.

**Kullanıcı komutları:**
| Komut | Açıklama |
|--------|-----------|
| `Merhaba` | Selam mesajı gönderir |
| `Led yak` | Harici LED’i yakar |
| `Led söndür` | Harici LED’i kapatır |
| `Sicaklik` | Anlık sıcaklık ve nem değerini döndürür |
| `Gaz` | Gaz algılanıp algılanmadığını bildirir |
| `Komut` | Tüm komut listesini tekrar gönderir |

**Otomatik Bildirimler:**
- Gaz algılandığında uyarı mesajı gönderilir  
- Su/yağmur algılandığında bildirim yapılır  
- Hareket sensörü tetiklendiğinde LED yanıp söner ve Telegram’dan uyarı gider  

---

## 📶 Wi-Fi ve Telegram Ayarları

Aşağıdaki alanlar `main.py` içinde düzenlenmelidir:

```python
ssid = "your_wifi_name"
password = "your_wifi_password"

bot_token = "your_bot_token"
chat_id = "your_chat_id"

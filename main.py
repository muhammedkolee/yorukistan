'''
Kablosuz Ağ Teknolojileri

Kübra Kolay     -  22370031008
Esra Abanoğlu   -  22370031067
Büşra Bozdoğan  -  22370031054
Yahya Kaya      -  22370031036
Deniz Erol      -  22370031042
Muhammed Köle   -  22370031003
Davut Balasar   -  22370031004
Fatih Arslanol  -  20370031085
'''

# Gerekli kütüphanelerin içe aktarılması
import network           # Wifi bağlantısının sağlanması
import urequests         # İnternet üzerinden veri alış-verişinin sağlanması
import time              # Programın gerektiği zamanlarda gecikme verilmesi
import dht               # Sıcaklık ve Nem Sensörü'nün çalışabilmesi
from machine import Pin  # Yazılımın donanımla haberleşebilmesi

pir = Pin(16, Pin.IN)                    # PIR (Hareket sensörü)
tempNHum = dht.DHT11(Pin(17, Pin.OUT))   # Sıcaklık ve Nem Sensörü (DHT11)
mq2 = Pin(18, Pin.IN)                    # Gaz ve Duman Sensörü
su_sensoru = Pin(19, Pin.IN)             # Yağmur ve Su sensörü
led = Pin(20, Pin.OUT)                   # Harici Led

# Wifi bilgileri
ssid = "your_wifi_name"              # Wifi ismi (değiştirilebilir)
password = "your_wifi_password"      # Wifi şifresi (değiştirilebilir)

# Telegram bot bilgileri
bot_token = "your_bot_token"         # Bot ID'si (bot oluşturulduğunda değiştirilebilir!!!)
chat_id = "your_caht_id"             # Chat ID'si (kendi chatinize göre değiştirilebilir)

# Wifi'ya bağlan
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Wifi'ya bağlanılıyor...")

# Bağlantı kurulana kadar bağlanmaya çalış.
while not wlan.isconnected():
    time.sleep(0.5)
print("Bağlantı kuruldu!")

# Telegramdan son güncellemeleri getir.
def getUpdates(offset=False):
    url = "https://api.telegram.org/bot" + bot_token + "/getUpdates"
    if offset:
        url += "?offset=" + str(offset)
    response = urequests.get(url)
    updates = response.json()
    response.close()
    return updates

# Telegram'a mesaj gönderme fonksiyonu.
def sendMessage(msg):
    url = "https://api.telegram.org/bot" + bot_token + "/sendMessage"
    payload = "chat_id=" + chat_id + "&text=" + msg
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = urequests.post(url, data=payload, headers=headers)
        response.close()
    except Exception as error:
        print("Hata:", error)

def sendCommands():
    sendMessage("KOMUTLAR")
    sendMessage("Merhaba => Selam verir")
    sendMessage("Led yak => Harici ledi yakar")
    sendMessage("Led sondur => Harici ledi söndürür")
    sendMessage("Sicaklik => O anki sicakligi dondurur")
    sendMessage("Gaz => Evde gaz algilanip algilanmadigini dondurur")
    sendMessage("Komut => Komutları dondurur")
    
# Pico'nun çalıştığına dair mesajı telegram üzerinden ilet.
sendMessage("Pico W is running.")
sendCommands()

# Gelen mesaj kontrol ediliyor ve komuta göre gerekli cevaplar veriliyor.
def controlMessage(msg):
    if msg == "Merhaba":
        sendMessage("Selam")
        
    elif msg == "Led yak" or msg == "led yak":
        led.value(1)
        sendMessage("Led yaniyor!")
        
    elif msg == "Led söndür" or msg == "led söndür" or msg == "Led sondur" or msg == "led sondur":
        led.value(0)
        sendMessage("Led sonduruldu!")
        
    elif msg == "Sicaklik" or msg == "sicaklik" or msg == "Sıcaklık" or msg == "sıcaklık":
        sendMessage("Olcumun dogru yapilabilmesi icin en az 5 saniye bekleyiniz")
        tempNHum.measure()
        time.sleep(3)
        sicaklik = tempNHum.temperature()
        nem = tempNHum.humidity()
        sendMessage(f"Sicaklik: {str(sicaklik)} derece, Nem: {str(nem)}")
        
    elif msg == "Gaz" or msg == "gaz":
        sendMessage("Gaz algilandi" if mq2.value() == 1 else "Gaz algilanmadi")
        time.sleep(0.5)
        
    elif msg == "komut" or msg == "Komut" or msg == "command" or msg == "Command":
        sendCommands()
        
    else:
        sendMessage("Böyle bir komut bulunamadi, dogru yazdiginizdan emin olun!")    
 
# En son güncelleme ID’sini tut (aynı mesajı tekrar okumamak için)
last_update_id = 0

# Telegram'dan yeni mesajları çek
update = getUpdates()
if len(update['result']) != 0:
    last_update_id = update['result'][-1]['update_id']

counter = 8

while True:
    update = getUpdates(last_update_id)
    
    if su_sensoru.value() == 1:
        sendMessage("Su algilandi, yagmur basliyor olabilir")

    if mq2.value() == 1:
        sendMessage("Evde gaz algilandi!")

    if len(update['result']) != 0:
        if update['result'][-1]['update_id'] - 1 == last_update_id:
            last_update_id += 1
            controlMessage(update['result'][-1]['message']['text'])
    
    if counter == 20:    
        counter = 0
        if pir.value() == 1:
            sendMessage("Hareket algilandi")
            led.value(1)
            time.sleep(0.2)
            led.value(0)
            time.sleep(0.2)
            led.value(1)
            time.sleep(0.2)
            led.value(0)
            
    counter += 1
    time.sleep(0.5)
'''
Proje, Telegram'dan sürekli olarak yeni güncellemeleri getirir ve kontrol eder.
Uygulama ilk başlatıldığında Telegram üzerinden son mesajın ID numarasını değişkene atar.
Atanılan değişkenin ID numarası gelen verilerde son mesajın ID numarası ile karşılaştırılır eğer farklı ise son mesaja göre cevap vererek değişken
numarasını günceller.
'''
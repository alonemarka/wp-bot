import time
import logging
from whatsapp import WhatsApp  # Repodaki ana kütüphane
from chatgpt import get_ai_response  # AI fonksiyonumuz

# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Botu başlat
bot = WhatsApp()

print("✅ AloneBot aktif! QR kodunu okut...")

# QR kodunu okutma
bot.wait_for_login()

print("🎉 Bot başarıyla bağlandı! Mesajları dinliyor...")

# ===================== ANA DÖNGÜ =====================
while True:
    try:
        # Yeni mesajları al
        messages = bot.get_unread_messages()

        for msg in messages:
            phone = msg['phone']
            text = msg['message'].strip()

            if not text:
                continue

            print(f"\n📨 Yeni mesaj → {phone}: {text}")

            # AI ile yanıt üret
            yanit = get_ai_response(text)

            # Yanıtı gönder
            bot.send_message(phone, yanit)
            print(f"✅ Yanıt gönderildi → {phone}")

        time.sleep(2)  # 2 saniyede bir kontrol et

    except Exception as e:
        print(f"⚠️ Hata: {e}")
        time.sleep(5)

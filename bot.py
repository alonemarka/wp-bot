import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from chatgpt import get_ai_response

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WhatsAppBot:
    def __init__(self):
        options = Options()
        options.add_argument("--user-data-dir=./whatsapp-profile")  # QR bir kere okut, sonra kalır
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--headless=new")  # Test için kapat, QR için açık olsun

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("https://web.whatsapp.com")
        self.wait_for_login()

    def wait_for_login(self):
        print("WhatsApp Web açıldı. QR kodunu telefonundan okut...")
        while True:
            try:
                self.driver.find_element(By.XPATH, '//div[@data-testid="chat-list"]')
                print("✅ Giriş başarılı!")
                break
            except:
                time.sleep(3)

    def listen_and_reply(self):
        print("Bot dinleme modunda... (Ctrl+C ile durdur)")
        last_message = ""

        while True:
            try:
                # Son gelen mesajı bul
                message_elements = self.driver.find_elements(By.XPATH, '//div[@data-testid="msg-container"]//span[@data-testid="msg-content"]')
                
                if message_elements:
                    latest_message = message_elements[-1].text.strip()
                    
                    if latest_message and latest_message != last_message and latest_message.startswith("!"):
                        last_message = latest_message
                        command = latest_message[1:].strip()  # !komut

                        print(f"Komut alındı: {command}")

                        # AI'den cevap al
                        ai_response = get_ai_response(command)
                        
                        # Cevabı gönder
                        self.send_message(ai_response)
                        print(f"Cevap gönderildi: {ai_response[:50]}...")

                time.sleep(3)  # 3 saniyede bir kontrol et

            except Exception as e:
                time.sleep(5)

    def send_message(self, message):
        try:
            input_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true" and @data-testid="conversation-compose-box-input"]')
            input_box.click()
            input_box.clear()
            input_box.send_keys(message)
            input_box.send_keys(Keys.ENTER)
            time.sleep(1)
        except:
            print("Mesaj gönderilemedi.")


if __name__ == "__main__":
    bot = WhatsAppBot()
    bot.listen_and_reply()

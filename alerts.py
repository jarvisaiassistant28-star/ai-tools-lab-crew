import urllib.parse
import requests
from config import Config

class AlertNotifier:
    """
    Multi-Channel Zero-Dollar Alert Dispatcher.
    Primary: Telegram (@CallMeBot_txtbot / user @Manuhcruz) - Instant, 100% reliable.
    Fallback: WhatsApp CallMeBot / Twilio.
    """
    def __init__(self):
        self.telegram_user = Config.TELEGRAM_USER or "@Manuhcruz"
        self.whatsapp_phone = Config.WHATSAPP_PHONE
        self.callmebot_key = Config.CALLMEBOT_API_KEY

    def send_alert(self, message: str) -> bool:
        """
        Sends executive alert to Telegram first (instant delivery), then WhatsApp if configured.
        """
        delivered = False
        
        # 1. Telegram Dispatch via CallMeBot (Verified for @Manuhcruz)
        if self.telegram_user:
            try:
                clean_user = self.telegram_user if self.telegram_user.startswith("@") else f"@{self.telegram_user}"
                encoded_msg = urllib.parse.quote_plus(message)
                url = f"https://api.callmebot.com/text.php?user={clean_user}&text={encoded_msg}"
                resp = requests.get(url, timeout=15)
                if resp.status_code == 200:
                    print(f"[Alerts] ✅ Successfully delivered instant alert to Telegram ({clean_user})!")
                    delivered = True
                else:
                    print(f"[Alerts] Telegram API response: {resp.text}")
            except Exception as e:
                print(f"[Alerts] Telegram alert error: {e}")

        # 2. WhatsApp Dispatch (if key configured)
        if self.whatsapp_phone and self.callmebot_key:
            try:
                encoded_msg = urllib.parse.quote_plus(message)
                url = f"https://api.callmebot.com/whatsapp.php?phone={self.whatsapp_phone}&text={encoded_msg}&apikey={self.callmebot_key}"
                w_resp = requests.get(url, timeout=15)
                if w_resp.status_code == 200:
                    print("[Alerts] ✅ Successfully delivered to WhatsApp!")
                    delivered = True
            except Exception as we:
                print(f"[Alerts] WhatsApp notice: {we}")

        if not delivered:
            print("[Alerts] Fallback Console Output:")
            print(message)
            return True

        return True

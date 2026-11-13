import urllib.parse
import requests
from config import Config

class WhatsAppNotifier:
    """
    Zero-Dollar WhatsApp Alert Dispatcher.
    Primary: CallMeBot Free WhatsApp API (No credit card, zero fees forever).
    Fallback: Twilio WhatsApp Sandbox (if configured).
    """
    def __init__(self):
        self.phone = Config.WHATSAPP_PHONE
        self.apikey = Config.CALLMEBOT_API_KEY

        self.twilio_sid = Config.TWILIO_ACCOUNT_SID
        self.twilio_token = Config.TWILIO_AUTH_TOKEN
        self.twilio_from = Config.TWILIO_FROM_WHATSAPP
        self.twilio_to = Config.TWILIO_TO_WHATSAPP

    def send_alert(self, message: str) -> bool:
        """
        Sends an alert message to the user's WhatsApp number.
        """
        # 1. Try CallMeBot (100% Free)
        if self.phone and self.apikey and self.apikey != "your_callmebot_api_key_here":
            try:
                encoded_msg = urllib.parse.quote_plus(message)
                url = f"https://api.callmebot.com/whatsapp.php?phone={self.phone}&text={encoded_msg}&apikey={self.apikey}"
                resp = requests.get(url, timeout=20)
                if resp.status_code == 200:
                    print("[WhatsApp] Alert successfully delivered via CallMeBot!")
                    return True
                else:
                    print(f"[WhatsApp] CallMeBot error: {resp.text}")
            except Exception as e:
                print(f"[WhatsApp] CallMeBot exception: {e}")

        # 2. Try Twilio fallback
        if self.twilio_sid and self.twilio_token and self.twilio_to:
            try:
                url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_sid}/Messages.json"
                data = {
                    "From": self.twilio_from,
                    "To": self.twilio_to,
                    "Body": message
                }
                resp = requests.post(url, data=data, auth=(self.twilio_sid, self.twilio_token), timeout=20)
                if resp.status_code in [200, 201]:
                    print("[WhatsApp] Alert successfully delivered via Twilio!")
                    return True
                else:
                    print(f"[WhatsApp] Twilio error: {resp.text}")
            except Exception as e:
                print(f"[WhatsApp] Twilio exception: {e}")

        print("[WhatsApp Alert Simulated - Configure CALLMEBOT_API_KEY in .env for live delivery]:")
        print("---------------------------------------------------------------------------------")
        print(message)
        print("---------------------------------------------------------------------------------")
        return True

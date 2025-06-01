import requests
import os

# Telegram Bot Credentials
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7670503928:AAE04UrPL64gm1o_IL0RJpJTOsfL_1zDBoE")  # Set this in environment variables
TELEGRAM_CHAT_ID =-1002490809823 # Group chat ID

def send_telegram_alert():
    """
    Sends a violence alert to the Telegram group.
    """
    message = f"*ALERT: Violence Detected!*\n\n"
    message += "⚠️Take Action!"

    # Telegram API URL
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    # Send the message
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("✅ Alert sent successfully!")
    else:
        print(f"❌ Failed to send alert. Error: {response.text}")

# Example usage: Call this function when violence is detected
if __name__ == "__main__":
    send_telegram_alert()
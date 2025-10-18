import requests

# --- Double-check these values are correct ---
BOT_TOKEN = "8250266471:AAFV5nwTGrSHt7xRvABkrt-KATtKY-6cgWM"
CHAT_ID = "1191531453"

def send_test_message():
    """A simple function to test the Telegram connection."""
    message = "This is a direct test message from the script! ✅"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = { "chat_id": CHAT_ID, "text": message }

    print("Attempting to send a test message to Telegram...")

    try:
        response = requests.post(url, json=payload, timeout=10)
        # Raise an exception if the request failed (e.g., 401, 404)
        response.raise_for_status()
        print("Success! Message sent to Telegram.")
        print("Check your phone!")

    except requests.exceptions.HTTPError as err:
        print("\n--- HTTP ERROR ---")
        print(f"The request failed. Status code: {err.response.status_code}")
        print(f"Reason: {err.response.text}")
        print("\nCommon fixes:")
        print(" - 401 Unauthorized: Your BOT_TOKEN is incorrect.")
        print(" - 400 Bad Request (Chat not found): Your CHAT_ID is incorrect, or you haven't started the bot yet.")

    except Exception as e:
        print(f"\n--- An Error Occurred ---")
        print(e)
        print("\nThis might be a network issue. Check your internet connection.")

if __name__ == '__main__':
    send_test_message()

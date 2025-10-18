# honeypot_with_geolocation.py

import socket
import threading
import logging
import requests

# --- Configuration ---
HOST = '0.0.0.0'
PORT = 2222
LOG_FILE = 'honeypot.log'
TELEGRAM_BOT_TOKEN = "8262015049:AAHdG6PDaBp-ugOT_YwLvdwnS7r_FPpWaV4"
TELEGRAM_CHAT_ID = "1191531453"

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# --- NEW: Function to get Geolocation Data ---
def get_ip_geolocation(ip_address):
    """Fetches geolocation data for a given IP address."""
    # We ignore private IPs like 127.0.0.1 as they can't be geolocated
    if ip_address == '127.0.0.1':
        return {"country": "Localhost", "city": "N/A", "isp": "Local Machine"}
    
    try:
        # Query the free IP geolocation API
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url, timeout=5) # Added a timeout
        if response.status_code == 200:
            return response.json() # Return the location data as a dictionary
        else:
            return {"country": "Error", "city": "Error", "isp": "Error"}
    except requests.RequestException:
        return {"country": "Timeout", "city": "Timeout", "isp": "Timeout"}

# --- UPDATED: Function to Send Telegram Alert ---
def send_telegram_alert(username, password, ip_address):
    """Sends a formatted message with geolocation to Telegram."""
    if "YOUR_TELEGRAM_BOT_TOKEN_HERE" in TELEGRAM_BOT_TOKEN or "YOUR_CHAT_ID_HERE" in TELEGRAM_CHAT_ID:
        logging.warning("Telegram settings are not configured. Skipping alert.")
        return

    # --- NEW: Get geolocation data first ---
    location_data = get_ip_geolocation(ip_address)
    country = location_data.get('country', 'Unknown')
    city = location_data.get('city', 'Unknown')
    isp = location_data.get('isp', 'Unknown')

    # Construct the message text with the new location info
    message_text = (
        f"🚨 *SSH Honeypot Alert!* 🚨\n\n"
        f"🌍 *Location:* {city}, {country}\n"
        f"🌐 *ISP:* {isp}\n"
        f"💻 *Attacker IP:* `{ip_address}`\n\n"
        f"👤 *Username:* `{username}`\n"
        f"🔑 *Password:* `{password}`"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message_text,
        'parse_mode': 'Markdown'
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logging.info("Successfully sent alert with geo-data to Telegram.")
        else:
            logging.error(f"Failed to send Telegram alert. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logging.error(f"Error sending Telegram alert: {e}")

# --- Main Honeypot Logic (No changes needed here) ---
def handle_connection(client_socket, addr):
    ip_address = addr[0]
    logging.info(f"New connection from: {ip_address}")
    try:
        client_socket.send(b'SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n')
        data = client_socket.recv(1024).decode(errors='ignore').strip()
        username = "test_user"
        password = data if data else "no_password_sent"
        log_message = f"Failed login from {ip_address} - User: '{username}', Pass: '{password}'"
        logging.warning(log_message)
        send_telegram_alert(username, password, ip_address)
        client_socket.send(b'Permission denied, please try again.\r\n')
    except Exception as e:
        logging.error(f"Error during connection with {ip_address}: {e}")
    finally:
        client_socket.close()
        logging.info(f"Connection from {ip_address} closed.")

def start_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    logging.info(f"Honeypot listening on {HOST}:{PORT}")
    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_connection, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    start_honeypot()

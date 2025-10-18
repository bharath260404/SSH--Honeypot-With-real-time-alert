# Python SSH Honeypot with Real-Time Telegram Alerts

A simple but effective SSH honeypot written in Python. This project is designed to detect and log brute-force attempts on an SSH server and provide instant notifications with IP geolocation data via Telegram. It serves as a lightweight intrusion detection tool to gather basic threat intelligence.

---

## Features ✨

- **Real-Time Alerts:** Get instant notifications on your phone via the Telegram Bot API the moment an attacker tries to connect.
- **Geolocation Data:** Each alert is enriched with the attacker's approximate country, city, and ISP.
- **Credential Logging:** Captures and logs the password combinations that attackers use in their attempts.
- **Lightweight & Simple:** Easy to set up and run on any machine with Python installed, including a Raspberry Pi or a small cloud server.

---

## How It Works

The script opens a TCP socket on a specified port (e.g., 2222) and simulates a basic SSH server. When a connection is detected, the script:
1.  Sends a fake SSH server banner to appear legitimate.
2.  Captures the first data packet sent by the client, logging it as the password attempt.
3.  Logs the full attempt (Timestamp, IP, Username, Password) to a local `honeypot.log` file.
4.  Queries the `ip-api.com` service to get geolocation data for the attacker's IP address.
5.  Constructs and sends a formatted alert to a specified Telegram chat.
6.  Closes the connection.

---

## Setup & Usage 🛠️

Follow these steps to get your honeypot up and running.

#### 1. Clone the Repository
```bash
# TODO: Replace this URL with your own repository URL
git clone [https://github.com/your-username/Python-SSH-Honeypot.git](https://github.com/your-username/Python-SSH-Honeypot.git)
cd Python-SSH-Honeypot
```

#### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
All required packages are listed in `requirements.txt`.
```bash
pip install requests
```

#### 4. Configure Your Credentials
Open the Python script (`honeypot_with_geolocation.py`) and replace the placeholder values for your Telegram Bot Token and Chat ID.

```python
# ... inside the script ...
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"
```

#### 5. Run the Honeypot
```bash
python3 honeypot_with_geolocation.py
```
Your honeypot is now active and listening for connections!

---

## Future Enhancements

This project can be expanded with more advanced features, such as:
- **Fake Interactive Shell:** Keep the session open after a "login" to log the commands an attacker tries to run.
- **Data Visualization Dashboard:** Create a separate script to parse the log file and generate a world map of attack origins.
- **Dockerization:** Package the application into a Docker container for easy, isolated deployment.

- 
![Telegram Alert Demo]--



project developed by
Jella Bharath Kumar
- 

import subprocess
import json
import requests
import time

# Your working Telegram credentials
BOT_TOKEN = "8250266471:AAFV5nwTGrSHt7xRvABkrt-KATtKY-6cgWM"
CHAT_ID = "1191531453"

def send_telegram_alert(message):
    """Sends a message to your Telegram bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def monitor_honeypot_logs():
    """Monitors the honeypot's JSON log file by polling it."""
    print("✅ Monitoring for new attacks... Press Ctrl+C to stop.")
    processed_lines = 0

    while True:
        try:
            # This command dumps the entire log file
            command = ["docker", "exec", "my-honeypot", "cat", "/cowrie/var/log/cowrie.json"]
            result = subprocess.run(command, capture_output=True, text=True, check=True)

            # Split the output into lines and filter out any empty ones
            all_lines = [line for line in result.stdout.strip().split('\n') if line]

            # Figure out which lines are new
            new_lines = all_lines[processed_lines:]

            if new_lines:
                for line in new_lines:
                    try:
                        log_data = json.loads(line)
                        if log_data.get("eventid") == "cowrie.login.failed":
                            attacker_ip = log_data.get("src_ip", "N/A")
                            username = log_data.get("username", "N/A")
                            password = log_data.get("password", "N/A")

                            message = (
                                f"🚨 *Honeypot Alert!* 🚨\n\n"
                                f"*Attacker IP:* `{attacker_ip}`\n"
                                f"*Username Tried:* `{username}`\n"
                                f"*Password Tried:* `{password}`"
                            )
                            print("--- Attack Detected! Sending Alert! ---")
                            print(message)
                            send_telegram_alert(message)
                    except json.JSONDecodeError:
                        pass # Ignore lines that aren't valid JSON

            # Update the count of processed lines
            processed_lines = len(all_lines)

        except subprocess.CalledProcessError:
            # This happens if the log file doesn't exist yet, which is okay
            pass
        except KeyboardInterrupt:
            print("\nStopping monitor...")
            break

        # Wait for 2 seconds before checking again
        time.sleep(2)

if __name__ == '__main__':
    monitor_honeypot_logs()

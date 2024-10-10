import os
import time
import re
import requests
from datetime import datetime, timedelta
from colorama import Fore, Style

username = os.getenv("USERNAME")
log_file_path = fr"C:\Users\{username}\AppData\Roaming\.minecraft\logs\latest.log" # theres probably a better way to do this
webhook_url = "webhook_url"
incremental = True  # whether it notifies for every position update or just when the position is 1
discord_id = "0"  # ID it should ping when the queue is 1
last_position = None
first_position_time = {} 
wait_time = 20
check_interval = 2 # interval to check log file
wait_alert_interval = 20 # when to alert when file isnt being updated

def send_webhook(position, estimated_time=None, file_stopped=False):
    embed = {}
    ping_message = None

    if file_stopped:
        embed = {
            "title": "Waiting for file...",
            "description": "File stopped updating...",
            "color": 0xff5c5c
        }
    elif position == 1:
        embed = {
            "title": "Queue Update",
            "description": f"Queue position is {position}",
            "color": 0x6fff5c
        }
        ping_message = f"<@{discord_id}>"
    else:
        embed = {
            "title": "Queue Update",
            "description": f"Queue position: {position}\nEstimated time: {estimated_time}",
            "color": 0xffe95c
        }

    data = {"embeds": [embed]}
    if ping_message:
        data["content"] = ping_message

    requests.post(webhook_url, json=data)

def estimate_time(current_time, previous_time, positions_left):
    time_diff = (current_time - previous_time).total_seconds()
    estimated_remaining_seconds = time_diff * positions_left
    estimated_time = timedelta(seconds=estimated_remaining_seconds)

    hours, remainder = divmod(estimated_time.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours} Hours and {minutes} Minutes" if estimated_remaining_seconds > 0 else "0 Hours and 0 Minutes"

def monitor_log():
    global last_position, first_position_time
    file_last_updated = os.path.getmtime(log_file_path)
    last_alert_time = time.time()

    while True:
        try:
            current_file_update_time = os.path.getmtime(log_file_path) # check the update intervals
            time_since_last_update = time.time() - current_file_update_time

            if current_file_update_time > file_last_updated:
                file_last_updated = current_file_update_time

                with open(log_file_path, "r") as log_file:
                    log_lines = log_file.readlines()

                for line in reversed(log_lines):
                    match = re.search(r"Position in queue: (\d+)", line)
                    if match:
                        current_position = int(match.group(1))
                        current_time = datetime.strptime(re.search(r"\[(\d+:\d+:\d+)\]", line).group(1), "%H:%M:%S")

                        print(f"Queue position: {current_position}")
                        if current_position == 1:
                            print(Fore.GREEN + "Queue position is 1" + Style.RESET_ALL)
                        else:
                            print(f"Queue position: {current_position}")

                        if last_position is not None and current_position != last_position:
                            if last_position in first_position_time:
                                previous_time = first_position_time[last_position]
                                positions_left = current_position - 1
                                estimated_time = estimate_time(current_time, previous_time, positions_left)
                                print(f"Estimated time: {estimated_time}")

                                if incremental or current_position == 1:
                                    send_webhook(current_position, estimated_time)

                        if current_position not in first_position_time: # record the first time that POS appears
                            first_position_time[current_position] = current_time

                        last_position = current_position # updating the last position
                        break

            elif time_since_last_update > wait_alert_interval:
                if time.time() - last_alert_time >= wait_alert_interval: # alert if log file stops updating
                    print(Fore.RED + "Waiting... File stopped updating" + Style.RESET_ALL)
                    send_webhook(None, file_stopped=True)
                    last_alert_time = time.time()

            time.sleep(check_interval)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(check_interval)

if __name__ == "__main__":
    monitor_log()

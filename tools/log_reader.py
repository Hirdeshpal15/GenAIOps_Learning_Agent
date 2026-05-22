import os

def read_latest_log():

    log_folder = "logs"

    files = os.listdir(log_folder)

    if not files:
        return "No log files found."

    files.sort(reverse=True)

    latest_file = files[0]

    log_path = os.path.join(log_folder, latest_file)

    with open(log_path, "r", encoding="utf-8") as file:
        content = file.read()

    return f"Latest Log File: {latest_file}\n\n{content[:3000]}"
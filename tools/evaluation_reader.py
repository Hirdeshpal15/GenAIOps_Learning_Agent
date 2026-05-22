import os

def read_latest_evaluation():

    log_folder = "logs"

    files = [
        file for file in os.listdir(log_folder)
        if "evaluation" in file
    ]

    if not files:
        return "No evaluation logs found."

    files.sort(reverse=True)

    latest_file = files[0]

    log_path = os.path.join(log_folder, latest_file)

    with open(log_path, "r", encoding="utf-8") as file:
        content = file.read()

    return f"Latest Evaluation File: {latest_file}\n\n{content[:3000]}"
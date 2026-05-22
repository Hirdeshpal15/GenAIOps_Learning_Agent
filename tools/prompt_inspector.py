import os

def list_prompt_versions():

    prompt_folder = "prompts"

    files = os.listdir(prompt_folder)

    prompt_files = [
        file for file in files
        if file.endswith(".txt")
    ]

    return "\n".join(prompt_files)
def load_prompt(version="v1"):
    prompt_path = f"prompts/system_prompt_{version}.txt"

    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()
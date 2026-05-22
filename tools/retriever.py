import os

KNOWLEDGE_FOLDER = "knowledge_base"

def retrieve_context(user_query):

    combined_context = ""

    files = os.listdir(KNOWLEDGE_FOLDER)

    for file_name in files:

        file_path = os.path.join(KNOWLEDGE_FOLDER, file_name)

        with open(file_path, "r", encoding="utf-8") as file:

            content = file.read()

            # Very simple keyword matching
            if any(
                keyword.lower() in content.lower()
                for keyword in user_query.split()
            ):

                combined_context += f"\n--- {file_name} ---\n"
                combined_context += content + "\n"

    if not combined_context:
        return "No relevant context found."

    return combined_context
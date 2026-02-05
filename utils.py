import os

def get_saved_chats():
    if os.path.exists("chats.txt"):
        with open("chats.txt", "r+") as f:
            return f.readlines()
    return []

def save_chat(id):
    with open("chats.txt", "a") as f:
        f.write(str(id))

def remove_chat(id):
    lines=""
    with open("chats.txt", "r") as f:
        lines = f.readlines()
    with open("chats.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != str(id):
                f.write(line)
    
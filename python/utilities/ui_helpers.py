import os

# UI helpers
def clear():
    os.system("cls")

def error(msg: str):
    clear()
    print(f" Error: {msg}")
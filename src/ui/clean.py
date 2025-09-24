import os


def clear_screen():
    # Check the operating system
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')
    else:  # For Linux, macOS, and other Unix-like systems
        _ = os.system('clear')

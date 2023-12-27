import os
import subprocess


OS = "Windows" if os.name == "nt" else subprocess.check_output("uname", shell=True).decode("utf-8").strip()
GREEN = "0;32"
RED = "0;31"


def print_message(color, message, end="\n"):
    reset = "\033[0m"
    print(f"\033[{color}m{message}{reset}", end=end)

def generate_help():
    print_message(GREEN, "Running on {}".format(OS))
    print_message(GREEN, "")
    print_message(GREEN, "Usage: make [target]")
    print_message(GREEN, "")
    print_message(GREEN, "Available targets:")
    print_message(GREEN, "  install : install dependencies.")
    print_message(GREEN, "  run     : run the app.")
    print_message(GREEN, "  clean   : clean up the logs and figures.")
    print_message(GREEN, "  stop    : stop the app.")
    print_message(GREEN, "  boot    : boot the emulator.", end="")
    print_message(RED, "!!! modify the emulator name in Makefile.")
    print_message(GREEN, "  reload  : reload the appium server.")
    print_message(GREEN, "")
    print_message(GREEN, "Normally, run make install first, then run make run to start the app.")

if __name__ == "__main__":
    generate_help()

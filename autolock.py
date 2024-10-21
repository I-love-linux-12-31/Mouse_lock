import subprocess
import sys
import time
import os
import backend

CALLS_PEER_SECOND = int(os.getenv("CALLS_PEER_SECOND", 200))
SLEEP_INTERVAL = 1 / CALLS_PEER_SECOND


def check_display_server():
    session_type = os.getenv("XDG_SESSION_TYPE")
    if session_type == "wayland":
        print("\033[33mWarning: The program is running under Wayland. Mouse locking might not work correctly.\033[0m")
    elif session_type != "x11":
        print("\033[33mWarning: Unsupported display server. The program is designed to work with X11.\033[0m")


def run_game_and_lock(command):
    try:
        process = subprocess.Popen(command, shell=True)

        lock_mouse_process = subprocess.Popen([sys.executable, "-c", """
import time
from backend import is_mouse_on_target_display, move_mouse_to_center
CALLS_PEER_SECOND = 200
SLEEP_INTERVAL = 1 / CALLS_PEER_SECOND
while True:
    if not is_mouse_on_target_display():
        move_mouse_to_center()
    time.sleep(SLEEP_INTERVAL)
"""])

        while process.poll() is None:
            time.sleep(1)

    finally:
        lock_mouse_process.terminate()
        backend.display.close()


if __name__ == "__main__":
    if len(sys.argv) < 2 or "--help" in sys.argv:
        print("Usage: python3 autolock.py <command>")
        sys.exit(1)

    check_display_server()

    game_command = ' '.join(sys.argv[1:])
    run_game_and_lock(game_command)

#!/usr/bin/env python3
import keyboard
import subprocess
import time
import json
import os
import sys
import shutil
if os.geteuid() != 0:
    print("🔒 This tool needs root. Re-running with sudo...")
    os.execvp("sudo", ["sudo"] + ["python3"] + sys.argv)

CONFIG_PATH = os.path.expanduser("~/.quicktarget_hotkeys.json")

target_ip = ""

def open_hotkey_config():
    editor = os.environ.get("EDITOR", "nano")  # Uses $EDITOR or defaults to nano
    try:
        subprocess.call(["sudo", editor, CONFIG_PATH])
    except Exception as e:
        print(f"Failed to open config: {e}")

def run_nmap_scan():
    if not target_ip:
        print(" No target IP set.")
        return
    print("🛰️  Launching Nmap...")
    subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"nmap -sV {target_ip}; exec bash"])

def run_enum4linux():
    if not target_ip:
        print(" No target IP set.")
        return
    if not shutil.which("enum4linux"):
        print("⚠️  enum4linux not found. Is it installed?")
        return
    print("Running enum4linux...")
    subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"enum4linux -a {target_ip}; exec bash"])

#---------------------ARGV--------------------------

if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg.lower() in [ "-help", "-h"]:
        print("\n📖 Project-002 Usage:")
        print("  project-002                Launch normally")
        print("  project-002 [IP]           Set target IP directly")
        print("  project-002 modify         Modify hotkeys")
        print("  project-002 -help         Show this menu")
        print(f"\n Hotkey config file: {CONFIG_PATH}\n")
        sys.exit()
    elif "." in arg:
        target_ip = arg
        print(f" Target IP set from CLI: {target_ip}")
    elif arg.lower() == "modify":
   	 open_hotkey_config()
   	 sys.exit(0)
    else:
        print(f"⚠️ Unknown argument: {arg}")

# ---------------- Hotkey Config Loader ----------------

def load_hotkeys():
    default_hotkeys = {
        "set_ip": "alt+s",
        "inject_ip": "insert"
    }

    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f:
            json.dump(default_hotkeys, f, indent=4)
        print(f"[+] Created default config at {CONFIG_PATH}")
        return default_hotkeys

    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
            print(f"[+] Loaded hotkey config from {CONFIG_PATH}")
            return config
    except Exception as e:
        print(f"[!] Failed to load config. Using defaults. Error: {e}")
        return default_hokeys

# ---------------- Window Detection ----------------

def get_active_window_id():
    try:
        return subprocess.check_output(['xdotool', 'getwindowfocus'], text=True).strip()
    except Exception as e:
        print(f"Error getting window ID: {e}")
        return None

def get_window_class(win_id):
    try:
        xprop_output = subprocess.check_output(['xprop', '-id', win_id], text=True)
        for line in xprop_output.splitlines():
            if "WM_CLASS" in line:
                return line.split('=')[1].strip().lower()
    except Exception as e:
        print(f"Error getting window class: {e}")
    return ""

def is_terminal_active():
    win_id = get_active_window_id()
    if not win_id:
        return False

    win_class = get_window_class(win_id)
    known_terminals = [
        "gnome-terminal", "xterm", "tilix", "konsole", "xfce4-terminal", "alacritty", "terminal"
    ]

    return any(term in win_class for term in known_terminals)

# ---------------- Core Actions ----------------

def set_target_ip():
    global target_ip
    print("\n Enter target IP:")
    target_ip = input(">> ").strip()
    print(f"Target IP set to: {target_ip}")

def inject_target_ip():
    global target_ip
    if not target_ip:
        print("No target IP set.")
        return

    if is_terminal_active():
        print(" Injecting target IP...")
        time.sleep(0.2)
        keyboard.write(target_ip, delay=0.05)
        time.sleep(0.3)

        # Fix stuck modifier keys
        for key in ['ctrl', 'alt', 'shift']:
            keyboard.release(key)

        print("Injection complete.")
    else:
        print("⚠️  Injection skipped. Not a terminal.")

# ---------------- Setup ----------------

def main():
    hotkeys = load_hotkeys()

    keyboard.add_hotkey(hotkeys.get('set_ip', 'ctrl+alt+shift+t'), set_target_ip)
    keyboard.add_hotkey(hotkeys.get('inject_ip', 'ctrl+alt+shift+i'), inject_target_ip)
    keyboard.add_hotkey('ctrl+alt+n', run_nmap_scan)
    keyboard.add_hotkey('ctrl+alt+e', run_enum4linux)

    try:
        # Clean launch banner
        print("\n╔═══════════════════════════════════════╗")
        print("║        🚀 Project-002 Beta Ready       ║")
        print("╚═══════════════════════════════════════╝")
        print(f"Current target IP: {target_ip if target_ip else '[not set]'}")
        print(f"Set target IP:      {hotkeys.get('set_ip')}")
        print(f"Inject target IP:   {hotkeys.get('inject_ip')}")
        print(f"Run Nmap:          {hotkeys.get('nmap_scan')}")
        print(f"Run Enum4linux:     {hotkeys.get('enum_scan')}")
        print("Exit:                Ctrl+C\n")

        keyboard.wait()

    except KeyboardInterrupt:
        print("\n Project-002 terminated by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()

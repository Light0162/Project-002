#Project-002

A hotkey-driven recon launcher designed for red teamers, CTF players, and penetration testers.  
Speed up your workflow by setting target IPs, injecting them instantly, and launching recon tools — all from the keyboard.

---

##Features

- Global hotkeys to:
  - Set a target IP
  - Inject the IP into any active terminal
  - Launch `nmap` and `enum4linux` automatically
-  Works across terminal windows (detects if a terminal is active)
-  Customizable hotkeys (`~/.quicktarget_hotkeys.json`)
-  Target IP history (stores last 20 IPs)
-  Clean CLI interface with optional GUI version coming soon
-  Modular design — more tools coming!

---

##Installation

```bash
git clone https://github.com/light0162/project-002.git
cd project-002
chmod +x project-002
sudo ln -s $PWD/project-002 /usr/local/bin/project-002


## Usage
project-002                # Launch the app normally
project-002 192.168.1.10   # Set the IP directly from command
project-002 history        # View target IP history
project-002 modify         # Edit hotkeys (opens config)
project-002 --help         # View help menu
project-002 --version      # Show version info

import subprocess
import time
import os
import threading
import json
from tabulate import tabulate
from termcolor import colored
from colorama import init, Fore

init(autoreset=True)

# Konfigurasi Path
ADB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'adb', 'adb.exe')

# File Konfigurasi
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"game_id": "", "ports": [], "private_links": {}}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def launch_game(port, game_url):
    """Fungsi utama yang terbukti berhasil membuka game langsung"""
    try:
        # Langkah 1: Pastikan Roblox tertutup
        subprocess.run([ADB_PATH, '-s', f'127.0.0.1:{port}', 'shell', 'am', 'force-stop', 'com.roblox.client'],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Langkah 2: Gunakan intent khusus untuk langsung ke game
        result = subprocess.run([
            ADB_PATH, '-s', f'127.0.0.1:{port}',
            'shell', 'am', 'start',
            '-a', 'android.intent.action.VIEW',
            '-d', game_url,
            '-n', 'com.roblox.client/com.roblox.client.ActivityProtocolLaunch'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Debugging: Tampilkan output jika diperlukan
        if result.returncode != 0:
            print(colored(f"Error on port {port}: {result.stderr}", 'red'))
            return False
        
        time.sleep(3)  # Waktu tunggu minimal
        return True
        
    except Exception as e:
        print(colored(f"Critical error on port {port}: {str(e)}", 'red'))
        return False

def monitor_and_restart(port, config, status_dict):
    """Fungsi monitoring dengan interval"""
    game_id = config["game_id"]
    private_link = config["private_links"].get(str(port), "")
    
    while True:
        game_url = private_link if private_link else f"roblox://placeID={game_id}"
        
        # Update status
        status_dict[port] = "Launching..."
        update_status(status_dict)
        
        if launch_game(port, game_url):
            status_dict[port] = "In Game"
        else:
            status_dict[port] = "Failed"
        
        update_status(status_dict)
        
        # Cek status game setiap 30 detik
        for _ in range(30):
            if not check_running(port):
                status_dict[port] = "Crashed"
                update_status(status_dict)
                break
            time.sleep(1)

def check_running(port):
    try:
        result = subprocess.run(
            [ADB_PATH, '-s', f'127.0.0.1:{port}', 'shell', 'pidof', 'com.roblox.client'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return bool(result.stdout.strip())
    except Exception:
        return False

def update_status(status_dict):
    os.system('cls' if os.name == 'nt' else 'clear')
    rows = []
    for port, status in status_dict.items():
        color = {
            "In Game": "green",
            "Launching...": "yellow",
            "Failed": "red",
            "Crashed": "magenta"
        }.get(status, "white")
        rows.append([f"Port {port}", colored(status, color)])
    
    print(tabulate(rows, headers=["Emulator", "Status"], tablefmt="grid"))
    print(colored("ROBLOX DIRECT LAUNCH", 'cyan', attrs=['bold']).center(50))

def main():
    config = load_config()
    
    if not config["ports"]:
        print(colored("No ports configured! Add ports first.", 'yellow'))
        return
    
    # Connect all ports
    for port in config["ports"]:
        subprocess.run([ADB_PATH, 'connect', f'127.0.0.1:{port}'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    status = {port: "Initializing" for port in config["ports"]}
    update_status(status)
    
    # Start monitoring threads
    threads = []
    for port in config["ports"]:
        t = threading.Thread(target=monitor_and_restart, args=(port, config, status))
        t.daemon = True
        t.start()
        threads.append(t)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(colored("\nStopping all instances...", 'red'))

if __name__ == "__main__":
    main()

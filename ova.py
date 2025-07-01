import subprocess
import time
import os
import threading
import json
from tabulate import tabulate
from termcolor import colored
from colorama import init, Fore

# Inisialisasi
init(autoreset=True)

# Konfigurasi Path
ADB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'adb', 'adb.exe')
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"game_id": "", "ports": [], "private_links": {}}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def direct_launch(port, game_id):
    """Fungsi khusus untuk membuka game langsung (default)"""
    try:
        # Force stop dulu untuk memastikan fresh start
        subprocess.run([ADB_PATH, '-s', f'127.0.0.1:{port}', 'shell', 'am', 'force-stop', 'com.roblox.client'],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Gunakan intent khusus untuk default launch
        game_url = f"roblox://placeID={game_id}"
        result = subprocess.run([
            ADB_PATH, '-s', f'127.0.0.1:{port}',
            'shell', 'am', 'start',
            '-a', 'android.intent.action.VIEW',
            '-d', game_url,
            '-n', 'com.roblox.client/com.roblox.client.ActivityProtocolLaunch'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        time.sleep(3)  # Waktu tunggu minimal
        return True if result.returncode == 0 else False
        
    except Exception as e:
        print(colored(f"Error on port {port}: {str(e)}", 'red'))
        return False

def private_server_launch(port, private_link):
    """Fungsi original untuk private server (tidak diubah)"""
    try:
        subprocess.run([
            ADB_PATH, '-s', f'127.0.0.1:{port}',
            'shell', 'am', 'start',
            '-n', 'com.roblox.client/com.roblox.client.ActivityProtocolLaunch',
            '-d', private_link
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        return True
    except Exception:
        return False

def game_launcher(port, config, status_dict):
    """Fungsi utama pengeksekusi"""
    game_id = config["game_id"]
    private_link = config["private_links"].get(str(port))
    
    while True:
        status_dict[port] = "Launching..."
        update_status(status_dict)
        
        # Gunakan private server jika ada, jika tidak gunakan default
        if private_link:
            success = private_server_launch(port, private_link)
        else:
            success = direct_launch(port, game_id)
        
        status_dict[port] = "In Game" if success else "Failed"
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
    print(colored("ROBLOX DIRECT LAUNCHER", 'cyan', attrs=['bold']).center(50))
    print(colored("Default launch modified | Private server unchanged", 'yellow'))

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
        t = threading.Thread(target=game_launcher, args=(port, config, status))
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

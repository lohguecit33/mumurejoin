import subprocess
import time
import os
import threading
import json
from tabulate import tabulate
from termcolor import colored
from colorama import init, Fore

# Inisialisasi Colorama untuk pewarnaan teks
init(autoreset=True)

# Dapatkan jalur ADB saat dijalankan sebagai EXE
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

ADB_PATH = os.path.join(base_path, 'adb', 'adb.exe')

# File konfigurasi
config_file = "roblox_config.txt"
port_file = "adb_ports.txt"
PRIVATE_LINK_FILE = "private_links.json"

def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            return file.read().strip()
    return None

def save_config(game_id):
    with open(config_file, 'w') as file:
        file.write(game_id)
    print(colored(f"Game ID saved to {config_file}", 'green'))

def load_ports():
    if os.path.exists(port_file):
        with open(port_file, 'r') as file:
            return [port.strip() for port in file.readlines()]
    return []

def save_ports(ports):
    with open(port_file, 'w') as file:
        file.write('\n'.join(ports))
    print(colored(f"ADB ports saved to {port_file}", 'green'))

def load_private_links():
    try:
        if os.path.exists(PRIVATE_LINK_FILE):
            with open(PRIVATE_LINK_FILE, 'r') as file:
                return json.load(file)
        return {}
    except Exception as e:
        print(colored(f"Error loading private links: {e}", "red"))
        return {}

def save_private_link(device_id, link):
    try:
        links = load_private_links()
        links[device_id] = link
        with open(PRIVATE_LINK_FILE, 'w') as file:
            json.dump(links, file, indent=4)
        print(colored(f"Private link saved for emulator {device_id}", "green"))
    except Exception as e:
        print(colored(f"Error saving private link: {e}", "red"))

def auto_connect_adb(ports):
    for port in ports:
        subprocess.run([ADB_PATH, 'connect', f'127.0.0.1:{port}'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def launch_game_directly(device_id, game_url):
    try:
        # Langsung buka game tanpa melalui ActivitySplash
        subprocess.run([
            ADB_PATH, '-s', f'127.0.0.1:{device_id}', 
            'shell', 'am', 'start', 
            '-n', 'com.roblox.client/com.roblox.client.ActivityGame', 
            '-d', game_url
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        return True
    except Exception as e:
        print(colored(f"Failed to launch game directly on {device_id}: {e}", 'red'))
        return False

def auto_join_game(device_id, game_id, private_link, status):
    status[device_id] = "Launching Game"
    update_table(status)
    
    game_url = private_link if private_link else f"roblox://placeID={game_id}"
    
    if not launch_game_directly(device_id, game_url):
        status[device_id] = "Failed to Launch"
        update_table(status)
        return
    
    status[device_id] = "In Game"
    update_table(status)

def check_roblox_running(device_id):
    try:
        result = subprocess.run(
            [ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'pidof', 'com.roblox.client'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return bool(result.stdout.strip())
    except Exception:
        return False

def force_close_roblox(device_id):
    subprocess.run(
        [ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'force-stop', 'com.roblox.client'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(3)

def ensure_roblox_running_with_interval(device_id, game_id, private_link, status, interval_minutes):
    interval_seconds = interval_minutes * 60 if interval_minutes > 0 else None
    last_restart = time.time()

    while True:
        if not check_roblox_running(device_id):
            status[device_id] = "Restarting (crashed)"
            update_table(status)
            force_close_roblox(device_id)
            auto_join_game(device_id, game_id, private_link, status)
            last_restart = time.time()
        
        if interval_seconds and (time.time() - last_restart) >= interval_seconds:
            status[device_id] = "Restarting (interval)"
            update_table(status)
            force_close_roblox(device_id)
            auto_join_game(device_id, game_id, private_link, status)
            last_restart = time.time()
        
        time.sleep(5)

def update_table(status):
    os.system('cls' if os.name == 'nt' else 'clear')
    rows = []
    for device_id, game_status in status.items():
        color = {
            "In Game": "green",
            "Launching Game": "yellow",
            "Restarting (crashed)": "red",
            "Restarting (interval)": "magenta",
            "Failed to Launch": "red"
        }.get(game_status, "white")
        
        rows.append({
            "Emulator": f"127.0.0.1:{device_id}",
            "Status": colored(game_status, color)
        })
    
    print(tabulate(rows, headers="keys", tablefmt="grid"))
    print(colored("ROBLOX AUTO JOIN", 'blue', attrs=['bold']).center(50))

def run_all_instances(ports, game_id, private_codes, interval_minutes):
    status = {port: "Initializing" for port in ports}
    update_table(status)

    threads = []
    for port in ports:
        thread = threading.Thread(
            target=ensure_roblox_running_with_interval,
            args=(port, game_id, private_codes.get(port), status, interval_minutes)
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def menu():
    game_id = load_config()
    ports = load_ports()
    private_codes = load_private_links()

    if ports:
        auto_connect_adb(ports)
    else:
        print(colored("No ADB ports configured", 'yellow'))

    if game_id:
        print(colored(f"Loaded Game ID: {game_id}", 'green'))

    while True:
        print("\nMenu Options:")
        print("1. Start Auto Join")
        print("2. Set Game ID")
        print("3. Set ADB Ports")
        print("4. Set Private Server Code (All)")
        print("5. Set Private Server Code (Single)")
        print("6. Exit")

        choice = input("Select option (1-6): ").strip()

        if choice == '1':
            if not game_id:
                print(colored("Please set Game ID first", 'red'))
                continue
            interval = int(input("Restart interval in minutes (0 to disable): "))
            run_all_instances(ports, game_id, private_codes, interval)
        elif choice == '2':
            game_id = input("Enter new Game ID: ").strip()
            save_config(game_id)
        elif choice == '3':
            ports = input("Enter ADB ports (comma separated): ").split(',')
            ports = [port.strip() for port in ports if port.strip()]
            save_ports(ports)
            auto_connect_adb(ports)
        elif choice == '4':
            code = input("Enter private server link for all instances: ").strip()
            for port in ports:
                save_private_link(port, code)
            private_codes = load_private_links()
        elif choice == '5':
            port = input("Enter emulator port: ").strip()
            if port in ports:
                code = input(f"Enter private server link for {port}: ").strip()
                save_private_link(port, code)
                private_codes = load_private_links()
            else:
                print(colored("Invalid port number", 'red'))
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print(colored("Invalid option", 'red'))

if __name__ == "__main__":
    menu()

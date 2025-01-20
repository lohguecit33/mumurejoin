import subprocess
import time
import os
import threading
import json
from tabulate import tabulate
from termcolor import colored
from colorama import init

# Inisialisasi Colorama untuk pewarnaan teks
init(autoreset=True)

# Dapatkan jalur ADB saat dijalankan sebagai EXE
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # Jalur sementara untuk file EXE
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

ADB_PATH = os.path.join(base_path, 'adb', 'adb.exe')

# Nama file untuk menyimpan User ID, Game ID, Port ADB, dan Private Code
config_file = "roblox_config.txt"
port_file = "adb_ports.txt"
PRIVATE_LINK_FILE = "private_links.json"

# Fungsi untuk menyimpan dan memuat konfigurasi
def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                user_id = lines[0].strip()
                game_id = lines[1].strip()
                return user_id, game_id
    return None, None

# Fungsi untuk menyimpan User ID dan Game ID ke file
def save_config(user_id, game_id):
    with open(config_file, 'w') as file:
        file.write(f"{user_id}\n{game_id}\n")
    print(colored(f"User ID dan Game ID telah disimpan di {config_file}", 'green'))

# Fungsi untuk memuat Port ADB dari file
def load_ports():
    if os.path.exists(port_file):
        with open(port_file, 'r') as file:
            ports = file.readlines()
            return [port.strip() for port in ports]
    return []

# Fungsi untuk menyimpan Port ADB ke file
def save_ports(ports):
    with open(port_file, 'w') as file:
        for port in ports:
            file.write(f"{port}\n")
    print(colored(f"Port ADB telah disimpan di {port_file}", 'green'))

# Fungsi untuk memuat private links dari file
def load_private_links():
    try:
        if os.path.exists(PRIVATE_LINK_FILE):
            with open(PRIVATE_LINK_FILE, "r") as file:
                return json.load(file)
        else:
            return {}
    except Exception as e:
        print(colored(f"Error memuat private link: {e}", "red"))
        return {}

# Fungsi untuk menyimpan private link ke file
def save_private_link(device_id, link):
    try:
        links = load_private_links()
        links[device_id] = link
        with open(PRIVATE_LINK_FILE, "w") as file:
            json.dump(links, file, indent=4)
        print(colored(f"Private link for emulator {device_id} successfully saved: {link}", "green"))
    except Exception as e:
        print(colored(f"Error saving private link: {e}", "red"))

# Fungsi untuk menyambungkan ke ADB
def auto_connect_adb(ports):
    for port in ports:
        subprocess.run([ADB_PATH, 'connect', f'127.0.0.1:{port}'])
        time.sleep(2)

# Fungsi untuk memeriksa koneksi internet dalam game
def check_internet_connection(device_id):
    try:
        result = subprocess.run(
            [ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'ping', '-c', '1', '8.8.8.8'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        return False

# Fungsi untuk menjalankan Private Server
def start_private_server(device_id, private_link):
    try:
        subprocess.run(
            [ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'start', '-n', 'com.roblox.client/com.roblox.client.startup.ActivitySplash', '-d', private_link],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(15)
        # Membuka game di Roblox setelah ActivitySplash
        subprocess.run([ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'start', '-n', 'com.roblox.client/com.roblox.client.ActivityProtocolLaunch', '-d', private_link],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(10)                               
        print(colored(f"Private link dijalankan di emulator {device_id}.", "green"))
    except Exception as e:
        print(colored(f"Gagal menjalankan Private Server di emulator {device_id}: {e}", "red"))

# Fungsi untuk menjalankan Default Server
def start_default_server(device_id, game_id):
    try:
        game_url = f"roblox://placeID={game_id}"
        subprocess.run(
            [ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'start', '-n', 'com.roblox.client/com.roblox.client.startup.ActivitySplash', '-d', game_url],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(15)
        # Membuka game di Roblox setelah ActivitySplash
        subprocess.run([ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'start', '-n', 'com.roblox.client/com.roblox.client.ActivityProtocolLaunch', '-d', game_url],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(10)
        print(Fore.GREEN + f"Membuka game menggunakan server: {game_url}.")       
    except Exception as e:
        print(colored(f"Failed to start Default Server: {e}", 'red'))

# Fungsi untuk auto join game
def auto_join_game(device_id, game_id, private_link, status):
    status[device_id] = "Opening the Game"
    update_table(status)

    if private_link:
        start_private_server(device_id, private_link)
    else:
        start_default_server(device_id, game_id)

    status[device_id] = "In Game"
    update_table(status)

# Fungsi untuk memastikan Roblox berjalan
def ensure_roblox_running_with_interval(ports, game_id, private_codes, interval_minutes):
    status = {port: "waiting" for port in ports}
    update_table(status)

    interval_seconds = interval_minutes * 60
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        for port in ports:
            private_link = private_codes.get(port)

            if not check_roblox_running(port):
                print(colored(f"Roblox not running on emulator {port}. Restart...", 'red'))
                force_close_roblox(port)
                auto_join_game(port, game_id, private_link, status)

            if not check_internet_connection(port):
                print(colored(f"Emulator {port} lost internet connection. Force close Roblox.", 'red'))
                force_close_roblox(port)
                auto_join_game(port, game_id, private_link, status)

        if interval_minutes > 0 and elapsed_time >= interval_seconds:
            for port in ports:
                private_link = private_codes.get(port)
                force_close_roblox(port)
                auto_join_game(port, game_id, private_link, status)
            start_time = time.time()
        time.sleep(10)

# Fungsi untuk memeriksa apakah Roblox sedang berjalan
def check_roblox_running(device_id):
    try:
        result = subprocess.run(
            [ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'pidof', 'com.roblox.client'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return bool(result.stdout.strip())
    except subprocess.SubprocessError:
        return False

# Fungsi untuk force close jika game tidak terhubung
def force_close_roblox(device_id):
    # Cek koneksi internet setiap detik selama 10 detik
    for _ in range(10):
        if check_internet_connection(device_id):
            return  # Jika terhubung, keluar dari fungsi
        time.sleep(1)

    # Jika selama 10 detik tidak terhubung, force close aplikasi Roblox
    print(f"Tidak ada koneksi internet di emulator {device_id}, force close Roblox...")
    subprocess.run(
        [ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'force-stop', 'com.roblox.client'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(10)  # Tunggu 10 detik setelah force-close

# Fungsi untuk menjalankan setiap instance
def start_instance_in_thread(ports, game_id, private_codes, status):
    threads = []
    for port in ports:
        thread = threading.Thread(target=auto_join_game, args=(port, game_id, private_codes.get(port), status))
        thread.start()
        threads.append(thread)

    for port in ports:
        internet_thread = threading.Thread(target=ensure_roblox_running_with_interval, args=([port], game_id, private_codes, 1))
        internet_thread.start()
        threads.append(internet_thread)

    for thread in threads:
        thread.join()

# Fungsi untuk memperbarui tabel
def update_table(status):
    os.system('cls' if os.name == 'nt' else 'clear')
    rows = []
    for device_id, game_status in status.items():
        if game_status == "In Game":
            color = 'green'
        elif game_status == "Opening the Game":
            color = 'yellow'
        else:
            color = 'red'
        rows.append({"NAME": f"emulator:{device_id}", "Proses": colored(game_status, color)})
    
    print(tabulate(rows, headers="keys", tablefmt="grid"))
    print(colored("BANG OVA", 'blue', attrs=['bold', 'underline']).center(50))

# Menu utama
def menu():
    user_id, game_id = load_config()
    ports = load_ports()
    private_codes = load_private_links()

    if ports:
        auto_connect_adb(ports)
    else:
        print(colored("ADB port not found. Please set it first..", 'yellow'))

    if user_id and game_id:
        print(colored(f"User ID: {user_id}, Game ID: {game_id} has been loaded from configuration.", 'green'))
    else:
        print(colored("User ID dan Game ID not set yet. Please set it first.", 'yellow'))

    while True:
        print("\nMenu:")
        print("1. Auto join")
        print("2. Set User ID dan Game ID")
        print("3. Set Port ADB")
        print("4. Set private code for all instances")
        print("5. Set private code for 1 instance")
        print("6. Exit")

        choice = input("Select number (1/2/3/4/5/6): ")

        if choice == '1':
            if not user_id or not game_id:
                print(colored("User ID or Game ID has not been set. Please set it first.", 'red'))
                continue
            interval_minutes = int(input("Enter the time interval (in minutes, enter 0 for no interval).: "))
            ensure_roblox_running_with_interval(ports, game_id, private_codes, interval_minutes)
        elif choice == '2':
            user_id = input("Enter User ID: ")
            game_id = input("Enter Game ID: ")
            save_config(user_id, game_id)
        elif choice == '3':
            new_ports = input("Enter the ADB port (separate with commas if more than one).: ").split(',')
            save_ports([port.strip() for port in new_ports])
            ports = new_ports
            auto_connect_adb(ports)
        elif choice == '4':
            code = input("Enter private code for all instances: ").strip()
            for port in ports:
                save_private_link(port, code)
        elif choice == '5':
            instance = input("Enter the instance port: ").strip()
            code = input("Enter the private code for this instance.: ").strip()
            save_private_link(instance, code)
        elif choice == '6':
            print("Exit the program...")
            break
        else:
            print("Invalid selection!")

# Eksekusi utama
menu()

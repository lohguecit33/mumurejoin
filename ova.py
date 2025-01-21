import subprocess
import time
import os
import threading
import json
import requests
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
CACHE_FILE = "roblox_cache.json"

# Cache untuk menyimpan mapping username ke user ID
username_to_user_id_cache = {}

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

def load_cache_from_file(filepath="username_cache.json"):
    global username_to_user_id_cache
    try:
        with open(filepath, "r") as file:
            username_to_user_id_cache = json.load(file)
        print(colored("Cache berhasil dimuat dari file.", 'green'))
    except FileNotFoundError:
        print(colored("File cache tidak ditemukan, membuat cache baru.", 'yellow'))
    except Exception as e:
        print(colored(f"Error saat memuat cache dari file: {e}", 'red'))

def save_cache_to_file(filepath="username_cache.json"):
    try:
        with open(filepath, "w") as file:
            json.dump(username_to_user_id_cache, file)
        print(colored("Cache berhasil disimpan ke file.", 'green'))
    except Exception as e:
        print(colored(f"Error saat menyimpan cache ke file: {e}", 'red'))


# Fungsi untuk mendapatkan Roblox User ID dari API
def get_roblox_user_id_from_username(username):
    # Periksa cache terlebih dahulu
    if username in username_to_user_id_cache:
        print(colored(f"Username '{username}' ditemukan di cache.", 'green'))
        return username_to_user_id_cache[username]

    # Jika tidak ditemukan di cache, ambil dari API
    url = f"https://users.roblox.com/v1/users/search?keyword={username}"
    try:
        response = requests.get(url)
        
        # Jika status code 429 (Too Many Requests), tunggu 10 detik dan coba lagi
        if response.status_code == 429:
            print(colored("Terlalu banyak permintaan, mencoba lagi dalam 10 detik...", 'yellow'))
            time.sleep(10)  # Tunggu selama 10 detik
            return get_roblox_user_id_from_username(username)  # Coba lagi
        
        if response.status_code == 200:
            data = response.json()
            if "data" in data and data["data"]:
                roblox_user_id = data["data"][0]["id"]
                
                # Simpan hasil ke cache
                username_to_user_id_cache[username] = roblox_user_id
                
                return roblox_user_id
            else:
                print(colored(f"Tidak ada data yang ditemukan untuk username {username}", 'yellow'))
        else:
            print(colored(f"Error: Status Code {response.status_code}", 'red'))
    except Exception as e:
        print(colored(f"Error saat mencoba mendapatkan Roblox User ID: {e}", 'red'))
    return None

# Fungsi untuk menjalankan perintah ADB dan mendapatkan output
def run_adb_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    return result.stdout

# Fungsi untuk memastikan ADB root telah diaktifkan untuk semua device
def enable_adb_root_for_all(ports):
    for port in ports:
        adb_command = [ADB_PATH, "-s", f"127.0.0.1:{port}", "root"]
        result = subprocess.run(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error enabling adb root for emulator {port}: {result.stderr}")
        # Tidak ada output yang dicetak jika perintah sukses

# Fungsi untuk mendapatkan username dari prefs.xml
def get_username_from_prefs(device_id):
    # Perintah ADB untuk menarik file prefs.xml dari emulator
    adb_command = [ADB_PATH, "-s", f'127.0.0.1:{device_id}', "shell", "cat", "/data/data/com.roblox.client/shared_prefs/prefs.xml"]
    # Menjalankan perintah ADB
    xml_content = run_adb_command(adb_command)

    if xml_content:
        # Mencari username dari tag <string name="username">
        start_tag = '<string name="username">'
        end_tag = '</string>'

        start_index = xml_content.find(start_tag)
        if start_index != -1:
            start_index += len(start_tag)
            end_index = xml_content.find(end_tag, start_index)
            if end_index != -1:
                username = xml_content[start_index:end_index]
                return username
    return None

# Fungsi untuk mengecek status online menggunakan User ID
def check_online_status_by_user_id(user_id):
    url = f"https://presence.roblox.com/v1/presence/users"
    payload = {"userIds": [user_id]}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "userPresences" in data and data["userPresences"]:
                user_presence = data["userPresences"][0]
                online_status = user_presence.get("userPresenceType", 0)
                if online_status == 2:
                    return "Online in game"
                elif online_status == 1:
                    return "Online (website/app)"
                else:
                    return "Offline"
            else:
                return "Unknown"
        else:
            print(colored(f"Gagal mengecek status online. Status Code: {response.status_code}", "red"))
            return "Error"
    except Exception as e:
        print(colored(f"Error saat mengecek status online: {e}", "red"))
        return "Error"
    
# Fungsi untuk memuat Port ADB dari file
def load_ports():
    if os.path.exists(port_file):
        with open(port_file, 'r') as file:
            ports = file.readlines()
            return [port.strip() for port in ports]
    return []

# Fungsi untuk menyimpan Port ADB ke file
def save_ports(ports):
    # Menyimpan port-port ADB
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
        result = subprocess.run([ADB_PATH, 'connect', f'127.0.0.1:{port}'], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            enable_adb_root_for_all([port])  # Panggil enable_adb_root_for_all langsung setelah port terhubung
        else:
            print(f"Failed to connect to port {port}: {result.stderr}")

# Fungsi untuk menjalankan Private Server
def start_private_server(device_id, private_link):
    try:
        subprocess.run(
            [ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'start', '-n', 'com.roblox.client/com.roblox.client.startup.ActivitySplash', '-d', private_link],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(20)
        # Membuka game di Roblox setelah ActivitySplash
        subprocess.run([ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'start', '-n', 'com.roblox.client/com.roblox.client.ActivityProtocolLaunch', '-d', private_link],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(8)                               
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
        time.sleep(20)
        # Membuka game di Roblox setelah ActivitySplash
        subprocess.run([ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'start', '-n', 'com.roblox.client/com.roblox.client.ActivityProtocolLaunch', '-d', game_url],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(8)
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
    subprocess.run([ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'force-stop', 'com.roblox.client'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(8)

# Fungsi untuk menjalankan setiap instance
def start_instance_in_thread(ports, game_id, private_codes, status):
    def process_instance(port):
        private_link = private_codes.get(port)
        username = get_username_from_prefs(port)
        
        if username:
            roblox_user_id = username_to_user_id_cache(username)
            if not roblox_user_id:
                roblox_user_id = get_roblox_user_id_from_username(username)
                if roblox_user_id:
                    username_to_user_id_cache(username, roblox_user_id)

            if roblox_user_id:
                online_status = check_online_status_by_user_id(user_id)
                print(colored(f"Status {username}: {online_status}", "blue"))

                if online_status == "Online in game":
                    status[port] = "In Game"
                else:
                    auto_join_game(port, game_id, private_link, status)

    threads = []

    # Buat thread untuk setiap port
    for port in ports:
        thread = threading.Thread(target=process_instance, args=(port,))
        thread.start()
        threads.append(thread)

    # Pastikan semua thread selesai
    for thread in threads:
        thread.join()

    # Tambahkan thread untuk memastikan Roblox terus berjalan
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
    for device_id, roblox_user_id in status.items():
        username = get_username_from_prefs(device_id)  # Mendapatkan username dari prefs.xml
        online_status = check_online_status_by_user_id(user_id) if roblox_user_id else 'Unknown'

        # Menentukan warna berdasarkan status online
        if online_status == 'Online in game':
            color = 'green'
        elif online_status == 'Online (website/app)':
            color = 'yellow'
        elif online_status == 'Offline':
            color = 'red'
        else:
            color = 'magenta'

        rows.append({
            "NAME": f"emulator:{device_id}",
            "Username": username or "Not Found",
            "Online Status": colored(online_status, color)
        })
    
    print(tabulate(rows, headers="keys", tablefmt="grid"))
    print(colored("BANG OVA", 'blue', attrs=['bold', 'underline']).center(50))

# Menu utama
def menu():
    user_id, game_id = load_config()
    ports = load_ports()
    private_codes = load_private_links()
    load_cache_from_file()
    save_cache_to_file()
    
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

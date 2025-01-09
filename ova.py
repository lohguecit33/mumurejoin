import subprocess
import time
import os
import threading
from tabulate import tabulate
from termcolor import colored
from colorama import init
import re

# Inisialisasi Colorama untuk pewarnaan teks
init(autoreset=True)

# Nama file untuk menyimpan User ID, Game ID, Port ADB, dan Private Code
config_file = "roblox_config.txt"
port_file = "adb_ports.txt"
private_codes_file = "private_codes.txt"

# Fungsi untuk memuat User ID dan Game ID dari file
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

# Fungsi untuk memperbarui tabel status emulator
def update_table(status):
    os.system('cls' if os.name == 'nt' else 'clear')
    rows = []
    for device_id, game_status in status.items():
        # Menentukan warna berdasarkan status game
        if game_status == "In Game":
            color = 'green'
        elif game_status == "Membuka Game":
            color = 'yellow'
        else:
            color = 'red'
        rows.append({"NAME": f"emulator:{device_id}", "Proses": colored(game_status, color)})
    
    print(tabulate(rows, headers="keys", tablefmt="grid"))
    print(colored("BANG OVA", 'blue', attrs=['bold', 'underline']).center(50))

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

# Fungsi untuk memuat private codes dari file
def load_private_codes():
    if os.path.exists(private_codes_file):
        with open(private_codes_file, 'r') as file:
            codes = file.readlines()
            return {line.strip(): line.strip() for line in codes}
    return {}

# Fungsi untuk menyimpan private codes ke file
def save_private_codes(codes):
    with open(private_codes_file, 'w') as file:
        for device_id, code in codes.items():
            file.write(f"{device_id}:{code}\n")
    print(colored(f"Private codes telah disimpan di {private_codes_file}", 'green'))

# Fungsi untuk menyambungkan ke ADB
def auto_connect_adb(ports):
    for port in ports:
        subprocess.run(['adb', 'connect', f'127.0.0.1:{port}'])
        time.sleep(2)

# Fungsi untuk memproses dan menyimpan private code
def process_and_save_private_code(code, device_id=None):
    try:
        # Cek apakah kode adalah URL dan ambil kode private dari URL
        if "https://www.roblox.com/share?code=" in code:
            match = re.search(r"code=([a-f0-9]{32})", code)
            if match:
                code = match.group(1)  # Ambil kode private dari URL
            else:
                print(colored("URL does not contain valid private code.", 'red'))
                return

        if len(code) == 32:  # Panjang kode yang valid
            private_codes = load_private_codes()
            if device_id:
                private_codes[device_id] = code
                print(f"Private code is saved for device {device_id}: {code}")
            else:
                private_codes["default"] = code
                print(f"Private code disimpan untuk default: {code}")
            save_private_codes(private_codes)
            print(colored("Private code successfully saved.", 'green'))
        else:
            print(colored("Kode private tidak valid.", 'red'))
    except Exception as e:
        print(colored(f"An error occurred while saving the private code: {e}", 'red'))

# Fungsi untuk menjalankan Private Server
def start_private_server(device_id, game_id, private_code):
    try:
        game_private = f"https://www.roblox.com/share?code={private_code}&type=Server"
        subprocess.run(
            ['adb', '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'start', '-a', 'android.intent.action.VIEW', '-d', game_private],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(8)
    except Exception as e:
        print(colored(f"Failed to start Private Server: {e}", 'red'))

# Fungsi untuk menjalankan Default Server
def start_default_server(device_id, game_id):
    try:
        game_url = f"roblox://placeID={game_id}"
        subprocess.run(
            ['adb', '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'start', '-a', 'android.intent.action.VIEW', '-d', game_url],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(8)
    except Exception as e:
        print(colored(f"Failed to start Default Server: {e}", 'red'))


# Fungsi untuk auto join game, memilih apakah akan menggunakan private code atau default link
def auto_join_game(device_id, game_id, private_code, status):
    status[device_id] = "Opening the Game"
    update_table(status)

    if private_code:
        start_private_server(device_id, game_id, private_code)  # Jalankan private server
    else:
        start_default_server(device_id, game_id)  # Jalankan default server

    status[device_id] = "In Game"
    update_table(status)

# Fungsi untuk memastikan Roblox berjalan dengan interval waktu tertentu
def ensure_roblox_running_with_interval(ports, game_id, private_codes, interval_minutes):
    status = {port: "waiting" for port in ports}
    update_table(status)

    interval_seconds = interval_minutes * 60
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        for port in ports:
            private_code = private_codes.get(port)
            if not check_roblox_running(port):
                print(colored(f"Roblox not running on emulator {port}. Restart...", 'red'))
                force_close_roblox(port)
                auto_join_game(port, game_id, private_code, status)

        if interval_minutes > 0 and elapsed_time >= interval_seconds:
            for port in ports:
                private_code = private_codes.get(port)
                force_close_roblox(port)
                auto_join_game(port, game_id, private_code, status)
            start_time = time.time()
        time.sleep(10)

# Fungsi untuk memeriksa koneksi internet dalam game
def check_internet_connection(device_id):
    try:
        result = subprocess.run(
            ['adb', '-s', f'127.0.0.1:{device_id}', 'shell', 'ps'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return "com.roblox.client" in result.stdout
    except subprocess.SubprocessError:
        return False
    
# Fungsi untuk force close jika game tidak terhubung
def force_close_roblox(device_id):
    subprocess.run(['adb', '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'force-stop', 'com.roblox.client'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)

# Fungsi untuk memeriksa apakah Roblox sedang berjalan
def check_roblox_running(device_id):
    try:
        result = subprocess.run(
            ['adb', '-s', f'127.0.0.1:{device_id}', 'shell', 'pidof', 'com.roblox.client'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return bool(result.stdout.strip())
    except subprocess.SubprocessError:
        return False

# Fungsi untuk menjalankan setiap instance secara paralel
def start_instance_in_thread(ports, game_id, private_codes, status):
    threads = []
    for port in ports:
        thread = threading.Thread(target=auto_join_game, args=(port, game_id, private_codes.get(port), status))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

# Menu utama
def menu():
    user_id, game_id = load_config()
    ports = load_ports()
    private_codes = load_private_codes()

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
        print("3. set Port ADB")
        print("4. Set private code for all instances")
        print("5. Set private code for 1 instance")
        print("6. exit")

        choice = input("Select number (1/2/3/4/5/6): ")

        if choice == '1':
            if not user_id or not game_id:
                print(colored("User ID or Game ID has not been set. Please set it first.", 'red'))
                continue
            interval_minutes = int(input("Enter the time interval (in minutes, enter 0 for no interval).): "))
            ensure_roblox_running_with_interval(ports, game_id, private_codes, interval_minutes)
        elif choice == '2':
            user_id = input("Enter User ID: ")
            game_id = input("Enter Game ID: ")
            save_config(user_id, game_id)
        elif choice == '3':
            new_ports = input("Enter the ADB port (separate with commas if more than one).): ").split(',')
            save_ports([port.strip() for port in new_ports])
            ports = new_ports
            auto_connect_adb(ports)
        elif choice == '4':
            code = input("Enter private code for all instances: ").strip()
            process_and_save_private_code(code)
        elif choice == '5':
            instance = input("Enter the instance port: ").strip()
            code = input("Enter the private code for this instance.: ").strip()
            process_and_save_private_code(code, device_id=instance)
        elif choice == '6':
            print("Exit the program...")
            break
        else:
            print("Invalid selection!")

# Eksekusi utama
menu()

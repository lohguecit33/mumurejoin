import subprocess
import time
import os
from tabulate import tabulate
from termcolor import colored
from colorama import init

# Inisialisasi Colorama untuk pewarnaan teks
init(autoreset=True)

# Nama file untuk menyimpan User ID, Game ID, dan Port ADB
config_file = "roblox_config.txt"
port_file = "adb_ports.txt"

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

# Fungsi untuk menyambungkan ke ADB
def auto_connect_adb(ports):
    for port in ports:
        print(f"Mencoba sambungkan ke port {port}...")
        subprocess.run(['adb', 'connect', f'127.0.0.1:{port}'])
        time.sleep(2)

# Fungsi untuk memperbarui tabel status emulator
def update_table(status):
    os.system('cls' if os.name == 'nt' else 'clear')
    rows = [{"Emulator": f"emulator:{key}", "Proses": value} for key, value in status.items()]
    print(tabulate(rows, headers="keys", tablefmt="grid"))
    # Menambahkan teks "BANG OVA" di samping kanan tabel
    print(colored("BANG OVA", 'blue', attrs=['bold', 'underline']).center(50))  # Teks dengan ukuran besar dan diberi gaya

# Fungsi untuk menjalankan Roblox pada perangkat tertentu dan menyembunyikan output ADB
def run_roblox(device_id, status):
    status[device_id] = "Memulai Roblox"
    update_table(status)
    # Menyembunyikan output dari perintah adb
    subprocess.run(['adb', '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'start', '-n', 'com.roblox.client/.startup.ActivitySplash'], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(9)

# Fungsi untuk auto join game Blox Fruits dan mengganti nama proses
def auto_join_blox_fruits(device_id, game_id, status):
    status[device_id] = "Membuka blox fruits"
    update_table(status)
    subprocess.run(['adb', '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'start', '-n', 'com.roblox.client/.ActivityProtocolLaunch', 
                    '-d', f'https://www.roblox.com/games/{game_id}'], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(8)
    ensure_game_started(device_id, status)

# Fungsi untuk memastikan game Blox Fruits sudah mulai dan siap dimainkan
def ensure_game_started(device_id, status):
    status[device_id] = "Menunggu Game Dimulai"
    update_table(status)
    press_start_button_multiple_times(device_id)
    status[device_id] = "Blox Fruits Dimulai"
    update_table(status)

# Fungsi untuk menekan tombol Start di game Blox Fruits (menggunakan ADB) beberapa kali
def press_start_button_multiple_times(device_id):
    
    # Koordinat pertama
    x1, y1 = 550, 481
    # Koordinat kedua
    x2, y2 = 550, 380

    for _ in range(5):  # Menekan tombol sebanyak 5 kali
        subprocess.run(['adb', '-s', f'127.0.0.1:{device_id}', 'shell', 'input', 'tap', str(x1), str(y1)], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)  # Jeda 1 detik
        
        subprocess.run(['adb', '-s', f'127.0.0.1:{device_id}', 'shell', 'input', 'tap', str(x2), str(y2)], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)  # Jeda 1 detik

# Fungsi untuk force close Roblox
def force_close_roblox(device_id):
    
    subprocess.run(['adb', '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'force-stop', 'com.roblox.client'], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(8)

# Fungsi untuk memeriksa apakah Roblox sedang berjalan
def is_roblox_running(device_id):
    try:
        result = subprocess.run(
            ['adb', '-s', f'127.0.0.1:{device_id}', 'shell', 'pidof', 'com.roblox.client'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.stdout.strip():
            return True  # Roblox sedang berjalan
        else:
            return False  # Roblox tidak berjalan
    except subprocess.SubprocessError:
        return False  # Jika terjadi error saat menjalankan perintah

# Fungsi untuk memeriksa apakah Roblox masih berjalan
def check_roblox_running(device_id):
    result = subprocess.run(['adb', '-s', f'127.0.0.1:{device_id}', 'shell', 'pidof', 'com.roblox.client'], 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

# Fungsi untuk memeriksa teks "Leave" atau "Reconnect" di log
def check_leave_or_reconnect(device_id):
    result = subprocess.run(['adb', '-s', f'127.0.0.1:{device_id}', 'logcat', '-d', 'com.roblox.client:*'], 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logs = result.stdout.decode('utf-8')

    if "Leave" in logs or "Reconnect" in logs:
        return True
    return False    

# Fungsi utama untuk memastikan Roblox tetap berjalan dan restart sesuai interval waktu yang ditentukan
def ensure_roblox_running_with_interval(ports, game_id, interval_minutes):
    status = {port: "Menunggu" for port in ports}  # Status awal
    update_table(status)

    for port in ports:
        run_roblox(port, status)
        auto_join_blox_fruits(port, game_id, status)

    interval_seconds = interval_minutes * 60
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time

        # Periksa apakah Roblox masih berjalan setiap detik
        for port in ports:
            if not check_roblox_running(port):  # Jika Roblox tidak berjalan
                print(colored(f"Roblox tidak berjalan di emulator {port}, Memulai ulang roblox...", 'red'))
                force_close_roblox(port)  # Force close aplikasi
                run_roblox(port, status)  # Jalankan ulang Roblox
                auto_join_blox_fruits(port, game_id, status)  # Mulai game Blox Fruits lagi

        # Periksa setiap detik apakah "Leave" atau "Reconnect" muncul
        for port in ports:
            if check_leave_or_reconnect(port):  # Jika ada teks Leave atau Reconnect
                print(colored(f"di kick atau disconect{port}, memulai ulang roblox...", 'red'))
                force_close_roblox(port)  # Force close aplikasi
                run_roblox(port, status)  # Jalankan ulang Roblox
                auto_join_blox_fruits(port, game_id, status)  # Mulai game Blox Fruits lagi

        if elapsed_time >= interval_seconds:
            # Force close Roblox sebelum membuka ulang
            for port in ports:
                force_close_roblox(port)
                status[port] = "Restarting Roblox"
                update_table(status)
                run_roblox(port, status)
                auto_join_blox_fruits(port, game_id, status)
            start_time = time.time()

        time.sleep(5)  # Cek setiap detik

# Fungsi utama untuk menjalankan aplikasi
def menu():
    user_id, game_id = load_config()
    ports = load_ports()

    if user_id and game_id:
        print(colored(f"User ID: {user_id}, Game ID: {game_id} telah dimuat dari konfigurasi.", 'green'))
    else:
        print(colored("User ID dan Game ID belum diset. Silakan set terlebih dahulu.", 'yellow'))

    while True:
        print("\nMenu:")
        print("1. Atur interval restart dan jalankan ulang Roblox")
        print("2. Set User ID dan Game ID")
        print("3. Atur Port ADB")
        print("4. Keluar")

        choice = input("Pilih nomor (1/2/3/4): ")

        if choice == '1':
            if not user_id or not game_id:
                print(colored("User ID atau Game ID belum diset. Silakan set terlebih dahulu.", 'red'))
                continue
            interval_minutes = int(input("Masukkan interval waktu (dalam menit, masukkan 0 untuk tidak ada interval): "))
            ensure_roblox_running_with_interval(ports, game_id, interval_minutes)
        elif choice == '2':
            user_id = input("Masukkan User ID: ")
            game_id = input("Masukkan Game ID: ")
            save_config(user_id, game_id)
        elif choice == '3':
            new_ports = input("Masukkan port ADB (pisahkan dengan koma jika lebih dari satu): ").split(',')
            save_ports([port.strip() for port in new_ports])
            ports = new_ports
            auto_connect_adb(ports)
        elif choice == '4':
            print("Keluar dari program...")
            break
        else:
            print("Pilihan tidak valid!")

# Eksekusi utama
menu()
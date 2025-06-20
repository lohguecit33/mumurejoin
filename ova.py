import subprocess
import time
import os
import threading
import json
import re
from tabulate import tabulate
from termcolor import colored
from colorama import init, Fore
import sys
import xml.etree.ElementTree as ET

# Initialize colorama
init(autoreset=True)

# Get ADB path
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

ADB_PATH = os.path.join(base_path, 'adb', 'adb.exe')

# Configuration files
config_file = "roblox_config.txt"
port_file = "adb_ports.txt"
PRIVATE_LINK_FILE = "private_links.json"
COOKIE_FILE = "roblox_cookies.txt"
USER_DATA_FILE = "user_data.json"

# Status tracking
current_status = {}

def is_valid_cookie(cookie):
    """Validate Roblox cookie format"""
    return bool(re.match(r'^_\|WARNING:-DO-NOT-SHARE-THIS\.--', cookie))

def load_config():
    """Load game ID configuration"""
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            lines = file.readlines()
            if lines:
                return lines[0].strip()
    return None

def save_config(game_id):
    """Save game ID configuration"""
    with open(config_file, 'w') as file:
        file.write(f"{game_id}")
    print(colored(f"Game ID saved to {config_file}", 'green'))

def load_ports():
    """Load ADB ports"""
    if os.path.exists(port_file):
        with open(port_file, 'r') as file:
            return [port.strip() for port in file.readlines() if port.strip()]
    return []

def save_ports(ports):
    """Save ADB ports"""
    with open(port_file, 'w') as file:
        for port in ports:
            file.write(f"{port}\n")
    print(colored(f"ADB ports saved to {port_file}", 'green'))

def load_private_links():
    """Load private server links"""
    try:
        if os.path.exists(PRIVATE_LINK_FILE):
            with open(PRIVATE_LINK_FILE, "r") as file:
                return json.load(file)
        return {}
    except Exception as e:
        print(colored(f"Error loading private links: {e}", "red"))
        return {}

def save_private_link(device_id, link):
    """Save private server link"""
    try:
        links = load_private_links()
        links[device_id] = link
        with open(PRIVATE_LINK_FILE, "w") as file:
            json.dump(links, file, indent=4)
        print(colored(f"Private link saved for emulator {device_id}", "green"))
    except Exception as e:
        print(colored(f"Error saving private link: {e}", "red"))

def load_cookies():
    """Load saved cookies"""
    cookies = []
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, 'r') as file:
            for line in file:
                line = line.strip()
                if is_valid_cookie(line):
                    cookies.append(line)
    return cookies

def save_cookies(cookies):
    """Save cookies to file"""
    valid_cookies = [c for c in cookies if is_valid_cookie(c)]
    with open(COOKIE_FILE, 'w') as file:
        for cookie in valid_cookies:
            file.write(f"{cookie}\n")
    print(colored(f"{len(valid_cookies)} cookies saved", "green"))
    return valid_cookies

def load_user_data():
    """Load user data"""
    try:
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'r') as file:
                return json.load(file)
        return {}
    except Exception as e:
        print(colored(f"Error loading user data: {e}", "red"))
        return {}

def save_user_data(device_id, user_id, username):
    """Save user data"""
    try:
        data = load_user_data()
        data[device_id] = {"user_id": user_id, "username": username}
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(colored(f"Error saving user data: {e}", "red"))

def enable_adb_root(ports):
    """Enable ADB root for all ports"""
    for port in ports:
        result = subprocess.run([ADB_PATH, "-s", f"127.0.0.1:{port}", "root"], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Error enabling root for {port}: {result.stderr}")

def auto_connect_adb(ports):
    """Connect to all ADB ports"""
    for port in ports:
        result = subprocess.run([ADB_PATH, 'connect', f'127.0.0.1:{port}'], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Failed to connect to {port}: {result.stderr}")
    enable_adb_root(ports)

def extract_user_info(cookie):
    """Extract user ID from cookie (basic implementation)"""
    # Note: In a real implementation, you would need to make an API call to Roblox
    # with the cookie to get the actual user info. This is just a placeholder.
    return "12345678", "RobloxUser"  # Placeholder values

def login_with_cookie(device_id, cookie):
    """Login to Roblox using cookie"""
    try:
        # Clear previous session
        subprocess.run([ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'pm', 'clear', 'com.roblox.client'],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)

        # Create shared_prefs directory
        subprocess.run([ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'mkdir', '-p',
                      '/data/data/com.roblox.client/shared_prefs'],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Create XML file
        xml_content = f'''<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<map>
    <string name=".ROBLOSECURITY">{cookie}</string>
</map>'''
        
        # Push to device
        temp_file = "temp_prefs.xml"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        subprocess.run([ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'push', temp_file,
                      '/data/data/com.roblox.client/shared_prefs/com.roblox.client.xml'],
                     stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        
        # Set permissions
        subprocess.run([ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'chmod', '600',
                      '/data/data/com.roblox.client/shared_prefs/com.roblox.client.xml'],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        os.remove(temp_file)
        
        # Extract and save user info
        user_id, username = extract_user_info(cookie)
        save_user_data(device_id, user_id, username)
        
        # Launch Roblox
        subprocess.run([ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'start',
                      '-n', 'com.roblox.client/com.roblox.client.startup.ActivitySplash'],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        current_status[device_id] = {
            'status': 'Logged In',
            'user_id': user_id,
            'username': username
        }
        
        print(colored(f"Login successful on {device_id}", "green"))
        return True
        
    except Exception as e:
        print(colored(f"Login failed on {device_id}: {str(e)}", "red"))
        return False

def start_private_server(device_id, private_link):
    """Start private server"""
    try:
        subprocess.run(
            [ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'start', '-n', 
             'com.roblox.client/com.roblox.client.startup.ActivitySplash', '-d', private_link],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        
        current_status[device_id]['status'] = 'In Private Server'
        print(colored(f"Private server started on {device_id}", "green"))
    except Exception as e:
        print(colored(f"Failed to start private server on {device_id}: {e}", "red"))

def start_default_server(device_id, game_id):
    """Start default server"""
    try:
        game_url = f"roblox://placeID={game_id}"
        subprocess.run(
            [ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'start', '-n', 
             'com.roblox.client/com.roblox.client.startup.ActivitySplash', '-d', game_url],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        
        current_status[device_id]['status'] = 'In Default Server'
        print(colored(f"Default server started on {device_id}", "green"))
    except Exception as e:
        print(colored(f"Failed to start default server on {device_id}: {e}", "red"))

def check_roblox_running(device_id):
    """Check if Roblox is running"""
    try:
        result = subprocess.run(
            [ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'pidof', 'com.roblox.client'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return bool(result.stdout.strip())
    except Exception as e:
        print(colored(f"Error checking Roblox on {device_id}: {e}", 'red'))
        return False

def force_close_roblox(device_id):
    """Force close Roblox"""
    subprocess.run([ADB_PATH, '-s', f'127.0.0.1:{device_id}', 'shell', 'am', 'force-stop', 'com.roblox.client'],
                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    current_status[device_id]['status'] = 'Stopped'

def update_table():
    """Update and display status table"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    rows = []
    for device_id, data in current_status.items():
        status_color = {
            'Logged In': 'green',
            'In Private Server': 'cyan',
            'In Default Server': 'blue',
            'Stopped': 'red',
            'Offline': 'yellow'
        }.get(data['status'], 'magenta')
        
        rows.append({
            "Port": device_id,
            "User ID": data.get('user_id', 'N/A'),
            "Username": data.get('username', 'N/A'),
            "Status": colored(data['status'], status_color)
        })
    
    print(tabulate(rows, headers="keys", tablefmt="grid"))
    print(colored("ROBLOX EMULATOR MANAGER", 'blue', attrs=['bold', 'underline']).center(80))

def main_menu():
    """Main menu interface"""
    game_id = load_config()
    ports = load_ports()
    private_links = load_private_links()
    cookies = load_cookies()
    user_data = load_user_data()

    # Initialize status
    for port in ports:
        current_status[port] = user_data.get(port, {
            'status': 'Offline',
            'user_id': 'N/A',
            'username': 'N/A'
        })

    if ports:
        auto_connect_adb(ports)
    else:
        print(colored("No ADB ports configured", 'yellow'))

    while True:
        update_table()
        print("\nMain Menu:")
        print("1. Auto join game")
        print("2. Set Game ID")
        print("3. Manage ADB ports")
        print("4. Manage private servers")
        print("5. Cookie management")
        print("6. Exit")

        choice = input("Select option: ")

        if choice == '1':
            if not game_id:
                print(colored("Game ID not set", "red"))
                continue
                
            interval = int(input("Check interval in minutes (0 for no auto-restart): "))
            
            # Start monitoring thread
            monitor_thread = threading.Thread(
                target=monitor_instances,
                args=(ports, game_id, private_links, interval)
            monitor_thread.daemon = True
            monitor_thread.start()
            
        elif choice == '2':
            game_id = input("Enter new Game ID: ")
            save_config(game_id)
            
        elif choice == '3':
            print("\nPort Management:")
            print("1. Add ports")
            print("2. Clear all ports")
            port_choice = input("Select: ")
            
            if port_choice == '1':
                new_ports = input("Enter ports (comma separated): ").split(',')
                new_ports = [p.strip() for p in new_ports if p.strip()]
                save_ports(load_ports() + new_ports)
                ports = load_ports()
                auto_connect_adb(ports)
                
            elif port_choice == '2':
                save_ports([])
                ports = []
                
        elif choice == '4':
            print("\nPrivate Server Management:")
            print("1. Set for all instances")
            print("2. Set for specific instance")
            print("3. Clear all")
            priv_choice = input("Select: ")
            
            if priv_choice == '1':
                link = input("Enter private server link: ")
                for port in ports:
                    save_private_link(port, link)
                private_links = load_private_links()
                
            elif priv_choice == '2':
                port = input("Enter port: ")
                if port in ports:
                    link = input("Enter private server link: ")
                    save_private_link(port, link)
                    private_links = load_private_links()
                else:
                    print(colored("Invalid port", "red"))
                    
            elif priv_choice == '3':
                save_private_link({})
                private_links = {}
                
        elif choice == '5':
            cookie_menu(cookies, ports)
            cookies = load_cookies()
            
        elif choice == '6':
            print("Exiting...")
            break

def cookie_menu(cookies, ports):
    """Cookie management menu"""
    while True:
        update_table()
        print("\nCookie Management:")
        print("1. Add cookies")
        print("2. View cookies")
        print("3. Delete all cookies")
        print("4. Login all instances")
        print("5. Login specific instance")
        print("6. Back to main menu")
        
        choice = input("Select option: ")
        
        if choice == '1':
            print("Paste cookies (one per line, empty line to finish):")
            new_cookies = []
            while True:
                line = input()
                if not line and new_cookies:
                    break
                if is_valid_cookie(line):
                    new_cookies.append(line)
                elif line:
                    print(colored("Invalid cookie format", "red"))
            
            if new_cookies:
                save_cookies(cookies + new_cookies)
                
        elif choice == '2':
            print("\nSaved Cookies:")
            for i, cookie in enumerate(cookies, 1):
                print(f"{i}. {cookie[:50]}...")
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            if os.path.exists(COOKIE_FILE):
                os.remove(COOKIE_FILE)
                print(colored("All cookies deleted", "green"))
            else:
                print(colored("No cookies found", "yellow"))
            time.sleep(1)
            
        elif choice == '4':
            if not cookies:
                print(colored("No cookies available", "red"))
                time.sleep(1)
                continue
                
            for i, port in enumerate(ports):
                if i < len(cookies):
                    login_with_cookie(port, cookies[i])
                else:
                    print(colored(f"No cookie for port {port}", "yellow"))
            time.sleep(2)
            
        elif choice == '5':
            if not cookies:
                print(colored("No cookies available", "red"))
                time.sleep(1)
                continue
                
            port = input("Enter port: ")
            if port not in ports:
                print(colored("Invalid port", "red"))
                time.sleep(1)
                continue
                
            print("Available cookies:")
            for i, cookie in enumerate(cookies, 1):
                print(f"{i}. {cookie[:50]}...")
                
            try:
                idx = int(input("Select cookie: ")) - 1
                if 0 <= idx < len(cookies):
                    login_with_cookie(port, cookies[idx])
                else:
                    print(colored("Invalid selection", "red"))
            except ValueError:
                print(colored("Invalid input", "red"))
            time.sleep(2)
            
        elif choice == '6':
            break

def monitor_instances(ports, game_id, private_links, interval_minutes):
    """Monitor and maintain game instances"""
    interval_seconds = interval_minutes * 60 if interval_minutes > 0 else None
    last_restart = time.time()
    
    while True:
        try:
            for port in ports:
                if not check_roblox_running(port):
                    current_status[port]['status'] = 'Offline'
                    force_close_roblox(port)
                    
                    if private_links.get(port):
                        start_private_server(port, private_links[port])
                    else:
                        start_default_server(port, game_id)
                
            # Auto-restart logic
            if interval_seconds and (time.time() - last_restart) >= interval_seconds:
                for port in ports:
                    force_close_roblox(port)
                    if private_links.get(port):
                        start_private_server(port, private_links[port])
                    else:
                        start_default_server(port, game_id)
                last_restart = time.time()
                
            update_table()
            time.sleep(10)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(colored(f"Monitor error: {e}", "red"))
            time.sleep(10)

if __name__ == "__main__":
    main_menu()

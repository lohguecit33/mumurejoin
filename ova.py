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

# Initialize colorama
init(autoreset=True)

# Configuration
CONFIG = {
    'adb_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'adb', 'adb.exe'),
    'config_file': 'roblox_config.txt',
    'port_file': 'adb_ports.txt',
    'cookie_file': 'roblox_cookies.txt',
    'user_data_file': 'user_data.json',
    'private_links_file': 'private_links.json'
}

# Check if running as executable
if getattr(sys, 'frozen', False):
    CONFIG['adb_path'] = os.path.join(sys._MEIPASS, 'adb', 'adb.exe')

class RobloxManager:
    def __init__(self):
        self.status = {}
        self.load_all_data()

    def load_all_data(self):
        """Load all configuration data"""
        self.game_id = self.load_config()
        self.ports = self.load_ports()
        self.cookies = self.load_cookies()
        self.user_data = self.load_user_data()
        self.private_links = self.load_private_links()
        
        # Initialize status
        for port in self.ports:
            self.status[port] = self.user_data.get(port, {
                'status': 'Offline',
                'user_id': 'N/A',
                'username': 'N/A'
            })

    # File operations
    def load_config(self):
        """Load game ID from config file"""
        try:
            if os.path.exists(CONFIG['config_file']):
                with open(CONFIG['config_file'], 'r') as f:
                    return f.read().strip()
        except Exception as e:
            print(colored(f"Error loading config: {e}", "red"))
        return None

    def save_config(self, game_id):
        """Save game ID to config file"""
        try:
            with open(CONFIG['config_file'], 'w') as f:
                f.write(game_id)
            return True
        except Exception as e:
            print(colored(f"Error saving config: {e}", "red"))
            return False

    def load_ports(self):
        """Load ADB ports from file"""
        try:
            if os.path.exists(CONFIG['port_file']):
                with open(CONFIG['port_file'], 'r') as f:
                    return [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(colored(f"Error loading ports: {e}", "red"))
        return []

    def save_ports(self, ports):
        """Save ADB ports to file"""
        try:
            with open(CONFIG['port_file'], 'w') as f:
                for port in ports:
                    f.write(f"{port}\n")
            return True
        except Exception as e:
            print(colored(f"Error saving ports: {e}", "red"))
            return False

    def load_cookies(self):
        """Load cookies from file"""
        try:
            if os.path.exists(CONFIG['cookie_file']):
                with open(CONFIG['cookie_file'], 'r') as f:
                    return [line.strip() for line in f if self.is_valid_cookie(line.strip())]
        except Exception as e:
            print(colored(f"Error loading cookies: {e}", "red"))
        return []

    def save_cookies(self, cookies):
        """Save cookies to file"""
        try:
            valid_cookies = [c for c in cookies if self.is_valid_cookie(c)]
            with open(CONFIG['cookie_file'], 'w') as f:
                for cookie in valid_cookies:
                    f.write(f"{cookie}\n")
            return True
        except Exception as e:
            print(colored(f"Error saving cookies: {e}", "red"))
            return False

    def load_user_data(self):
        """Load user data from file"""
        try:
            if os.path.exists(CONFIG['user_data_file']):
                with open(CONFIG['user_data_file'], 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(colored(f"Error loading user data: {e}", "red"))
        return {}

    def save_user_data(self):
        """Save user data to file"""
        try:
            with open(CONFIG['user_data_file'], 'w') as f:
                json.dump(self.user_data, f, indent=4)
            return True
        except Exception as e:
            print(colored(f"Error saving user data: {e}", "red"))
            return False

    def load_private_links(self):
        """Load private server links"""
        try:
            if os.path.exists(CONFIG['private_links_file']):
                with open(CONFIG['private_links_file'], 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(colored(f"Error loading private links: {e}", "red"))
        return {}

    def save_private_links(self):
        """Save private server links"""
        try:
            with open(CONFIG['private_links_file'], 'w') as f:
                json.dump(self.private_links, f, indent=4)
            return True
        except Exception as e:
            print(colored(f"Error saving private links: {e}", "red"))
            return False

    # Utility functions
    @staticmethod
    def is_valid_cookie(cookie):
        """Validate Roblox cookie format"""
        return bool(re.match(r'^_\|WARNING:-DO-NOT-SHARE-THIS\.--', cookie))

    def run_adb_command(self, port, command, timeout=10):
        """Run ADB command with error handling"""
        try:
            full_command = [CONFIG['adb_path'], '-s', f'127.0.0.1:{port}'] + command
            result = subprocess.run(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout
            )
            if result.returncode != 0:
                raise Exception(result.stderr)
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            raise Exception("Command timed out")
        except Exception as e:
            raise Exception(f"ADB command failed: {str(e)}")

    # Core functionality
    def connect_all(self):
        """Connect to all ADB ports"""
        for port in self.ports:
            try:
                # Check if emulator is connected
                devices = subprocess.run(
                    [CONFIG['adb_path'], 'devices'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                ).stdout

                if f'127.0.0.1:{port}' not in devices:
                    # Connect if not already connected
                    subprocess.run(
                        [CONFIG['adb_path'], 'connect', f'127.0.0.1:{port}'],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    time.sleep(1)

                # Enable root
                self.run_adb_command(port, ['root'])
                self.status[port]['status'] = 'Connected'
            except Exception as e:
                self.status[port]['status'] = f'Error: {str(e)[:20]}...'
                print(colored(f"Error connecting to {port}: {e}", "red"))

    def login_with_cookie(self, port, cookie):
        """Login to Roblox using cookie"""
        try:
            # Clear previous session
            self.run_adb_command(port, ['shell', 'pm', 'clear', 'com.roblox.client'])
            time.sleep(2)

            # Create shared_prefs directory
            self.run_adb_command(port, ['shell', 'mkdir', '-p', '/data/data/com.roblox.client/shared_prefs'])

            # Create XML file
            xml_content = f'''<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<map>
    <string name=".ROBLOSECURITY">{cookie}</string>
</map>'''

            # Push to device
            temp_file = 'temp_roblox_prefs.xml'
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(xml_content)

            self.run_adb_command(port, ['push', temp_file, '/data/data/com.roblox.client/shared_prefs/com.roblox.client.xml'])
            os.remove(temp_file)

            # Set permissions
            self.run_adb_command(port, ['shell', 'chmod', '600', '/data/data/com.roblox.client/shared_prefs/com.roblox.client.xml'])

            # Extract user info (placeholder - in reality you'd call Roblox API)
            user_id = str(hash(cookie) % 100000000)  # Simulated user ID
            username = f"User_{user_id[:4]}"

            # Update user data
            self.user_data[port] = {
                'user_id': user_id,
                'username': username
            }
            self.save_user_data()

            # Update status
            self.status[port].update({
                'status': 'Logged In',
                'user_id': user_id,
                'username': username
            })

            # Launch Roblox
            self.run_adb_command(port, ['shell', 'am', 'start', '-n', 'com.roblox.client/com.roblox.client.startup.ActivitySplash'])
            
            print(colored(f"Login successful on {port}", "green"))
            return True

        except Exception as e:
            self.status[port]['status'] = f'Login Failed'
            print(colored(f"Login failed on {port}: {e}", "red"))
            return False

    def start_game(self, port, game_id=None, private_link=None):
        """Start Roblox game"""
        try:
            if private_link:
                self.run_adb_command(port, [
                    'shell', 'am', 'start', '-n',
                    'com.roblox.client/com.roblox.client.startup.ActivitySplash',
                    '-d', private_link
                ])
                self.status[port]['status'] = 'In Private Server'
            elif game_id:
                game_url = f"roblox://placeID={game_id}"
                self.run_adb_command(port, [
                    'shell', 'am', 'start', '-n',
                    'com.roblox.client/com.roblox.client.startup.ActivitySplash',
                    '-d', game_url
                ])
                self.status[port]['status'] = 'In Game'
            else:
                raise Exception("No game ID or private link provided")

            time.sleep(5)
            return True
        except Exception as e:
            self.status[port]['status'] = 'Start Failed'
            print(colored(f"Failed to start game on {port}: {e}", "red"))
            return False

    def check_roblox_running(self, port):
        """Check if Roblox is running"""
        try:
            pid = self.run_adb_command(port, ['shell', 'pidof', 'com.roblox.client'])
            return bool(pid)
        except Exception:
            return False

    def force_close_roblox(self, port):
        """Force close Roblox"""
        try:
            self.run_adb_command(port, ['shell', 'am', 'force-stop', 'com.roblox.client'])
            self.status[port]['status'] = 'Stopped'
            time.sleep(2)
            return True
        except Exception as e:
            print(colored(f"Error closing Roblox on {port}: {e}", "red"))
            return False

    # UI functions
    def show_status(self):
        """Display current status table"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        rows = []
        for port, data in self.status.items():
            status_color = {
                'Connected': 'blue',
                'Logged In': 'green',
                'In Game': 'cyan',
                'In Private Server': 'magenta',
                'Stopped': 'yellow',
                'Offline': 'red'
            }.get(data['status'].split(':')[0], 'white')
            
            rows.append([
                port,
                data.get('user_id', 'N/A'),
                data.get('username', 'N/A'),
                colored(data['status'], status_color)
            ])
        
        print(tabulate(rows, headers=["Port", "User ID", "Username", "Status"], tablefmt="grid"))
        print(colored("ROBLOX EMULATOR MANAGER", 'blue', attrs=['bold', 'underline']).center(80))

    def main_menu(self):
        """Main menu interface"""
        while True:
            self.show_status()
            print("\nMain Menu:")
            print("1. Start/Restart All Instances")
            print("2. Set Game ID")
            print("3. Manage ADB Ports")
            print("4. Manage Cookies")
            print("5. Manage Private Servers")
            print("6. Exit")

            choice = input("Select option: ").strip()

            if choice == '1':
                self.start_all_instances()
            elif choice == '2':
                self.set_game_id()
            elif choice == '3':
                self.manage_ports()
            elif choice == '4':
                self.manage_cookies()
            elif choice == '5':
                self.manage_private_servers()
            elif choice == '6':
                print("Exiting...")
                break
            else:
                print(colored("Invalid choice", "red"))
                time.sleep(1)

    def start_all_instances(self):
        """Start all instances with current configuration"""
        if not self.ports:
            print(colored("No ports configured", "red"))
            time.sleep(1)
            return

        if not self.game_id and not self.private_links:
            print(colored("No game ID or private links configured", "red"))
            time.sleep(1)
            return

        # Connect first
        self.connect_all()
        time.sleep(2)

        # Login with cookies if available
        for i, port in enumerate(self.ports):
            if i < len(self.cookies):
                self.login_with_cookie(port, self.cookies[i])
                time.sleep(2)

        # Start games
        for port in self.ports:
            private_link = self.private_links.get(port)
            if private_link:
                self.start_game(port, private_link=private_link)
            elif self.game_id:
                self.start_game(port, game_id=self.game_id)
            time.sleep(2)

        print(colored("All instances started", "green"))
        time.sleep(2)

    def set_game_id(self):
        """Set the game ID"""
        self.show_status()
        game_id = input("Enter Game ID: ").strip()
        if game_id:
            if self.save_config(game_id):
                self.game_id = game_id
                print(colored("Game ID saved successfully", "green"))
            else:
                print(colored("Failed to save Game ID", "red"))
        time.sleep(1)

    def manage_ports(self):
        """Manage ADB ports"""
        while True:
            self.show_status()
            print("\nPort Management:")
            print("1. Add Ports")
            print("2. Remove Port")
            print("3. Clear All Ports")
            print("4. Back to Main Menu")

            choice = input("Select option: ").strip()

            if choice == '1':
                ports_input = input("Enter ports (comma separated): ").strip()
                new_ports = [p.strip() for p in ports_input.split(',') if p.strip()]
                
                if new_ports:
                    current_ports = set(self.ports)
                    current_ports.update(new_ports)
                    if self.save_ports(list(current_ports)):
                        self.ports = self.load_ports()
                        print(colored("Ports updated successfully", "green"))
                    else:
                        print(colored("Failed to save ports", "red"))
                time.sleep(1)
                
            elif choice == '2':
                if not self.ports:
                    print(colored("No ports to remove", "yellow"))
                    time.sleep(1)
                    continue
                    
                port_to_remove = input("Enter port to remove: ").strip()
                if port_to_remove in self.ports:
                    updated_ports = [p for p in self.ports if p != port_to_remove]
                    if self.save_ports(updated_ports)):
                        self.ports = updated_ports
                        if port_to_remove in self.status:
                            del self.status[port_to_remove]
                        print(colored("Port removed successfully", "green"))
                    else:
                        print(colored("Failed to save ports", "red"))
                else:
                    print(colored("Port not found", "red"))
                time.sleep(1)
                
            elif choice == '3':
                if self.save_ports([])):
                    self.ports = []
                    self.status = {}
                    print(colored("All ports cleared", "green"))
                else:
                    print(colored("Failed to clear ports", "red"))
                time.sleep(1)
                
            elif choice == '4':
                break
            else:
                print(colored("Invalid choice", "red"))
                time.sleep(1)

    def manage_cookies(self):
        """Manage Roblox cookies"""
        while True:
            self.show_status()
            print("\nCookie Management:")
            print("1. Add Cookies")
            print("2. View Cookies")
            print("3. Remove Cookie")
            print("4. Clear All Cookies")
            print("5. Back to Main Menu")

            choice = input("Select option: ").strip()

            if choice == '1':
                print("Paste cookies (one per line, empty line to finish):")
                new_cookies = []
                while True:
                    line = input().strip()
                    if not line and new_cookies:
                        break
                    if self.is_valid_cookie(line):
                        new_cookies.append(line)
                    elif line:
                        print(colored("Invalid cookie format", "red"))
                
                if new_cookies:
                    if self.save_cookies(self.cookies + new_cookies):
                        self.cookies = self.load_cookies()
                        print(colored(f"{len(new_cookies)} cookies added", "green"))
                    else:
                        print(colored("Failed to save cookies", "red"))
                time.sleep(1)
                
            elif choice == '2':
                if not self.cookies:
                    print(colored("No cookies available", "yellow"))
                else:
                    print("\nSaved Cookies:")
                    for i, cookie in enumerate(self.cookies, 1):
                        print(f"{i}. {cookie[:50]}...")
                input("\nPress Enter to continue...")
                
            elif choice == '3':
                if not self.cookies:
                    print(colored("No cookies to remove", "yellow"))
                    time.sleep(1)
                    continue
                    
                try:
                    print("\nSelect cookie to remove:")
                    for i, cookie in enumerate(self.cookies, 1):
                        print(f"{i}. {cookie[:50]}...")
                    
                    index = int(input("Enter cookie number: ")) - 1
                    if 0 <= index < len(self.cookies):
                        updated_cookies = [c for i, c in enumerate(self.cookies) if i != index]
                        if self.save_cookies(updated_cookies):
                            self.cookies = updated_cookies
                            print(colored("Cookie removed successfully", "green"))
                        else:
                            print(colored("Failed to save cookies", "red"))
                    else:
                        print(colored("Invalid selection", "red"))
                except ValueError:
                    print(colored("Please enter a valid number", "red"))
                time.sleep(1)
                
            elif choice == '4':
                if os.path.exists(CONFIG['cookie_file']):
                    os.remove(CONFIG['cookie_file'])
                    self.cookies = []
                    print(colored("All cookies cleared", "green"))
                else:
                    print(colored("No cookie file found", "yellow"))
                time.sleep(1)
                
            elif choice == '5':
                break
            else:
                print(colored("Invalid choice", "red"))
                time.sleep(1)

    def manage_private_servers(self):
        """Manage private server links"""
        while True:
            self.show_status()
            print("\nPrivate Server Management:")
            print("1. Set Private Server for All")
            print("2. Set Private Server for Specific Port")
            print("3. View Private Servers")
            print("4. Clear Private Servers")
            print("5. Back to Main Menu")

            choice = input("Select option: ").strip()

            if choice == '1':
                link = input("Enter private server link: ").strip()
                if link:
                    for port in self.ports:
                        self.private_links[port] = link
                    if self.save_private_links():
                        print(colored("Private server set for all ports", "green"))
                    else:
                        print(colored("Failed to save private links", "red"))
                time.sleep(1)
                
            elif choice == '2':
                if not self.ports:
                    print(colored("No ports available", "yellow"))
                    time.sleep(1)
                    continue
                    
                port = input("Enter port: ").strip()
                if port in self.ports:
                    link = input("Enter private server link: ").strip()
                    if link:
                        self.private_links[port] = link
                        if self.save_private_links():
                            print(colored(f"Private server set for port {port}", "green"))
                        else:
                            print(colored("Failed to save private links", "red"))
                else:
                    print(colored("Port not found", "red"))
                time.sleep(1)
                
            elif choice == '3':
                if not self.private_links:
                    print(colored("No private servers configured", "yellow"))
                else:
                    print("\nPrivate Server Links:")
                    for port, link in self.private_links.items():
                        print(f"Port {port}: {link[:50]}...")
                input("\nPress Enter to continue...")
                
            elif choice == '4':
                self.private_links = {}
                if self.save_private_links():
                    print(colored("All private servers cleared", "green"))
                else:
                    print(colored("Failed to clear private links", "red"))
                time.sleep(1)
                
            elif choice == '5':
                break
            else:
                print(colored("Invalid choice", "red"))
                time.sleep(1)

if __name__ == "__main__":
    try:
        manager = RobloxManager()
        manager.main_menu()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(colored(f"Fatal error: {e}", "red"))
        input("Press Enter to exit...")

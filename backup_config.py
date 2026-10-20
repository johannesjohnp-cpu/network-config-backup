import os
import datetime
from netmiko import ConnectHandler

# Define the network device details
# (Replace with your actual router/switch IP and credentials)
cisco_device = {
    'device_type': 'cisco_ios',
    'host':   '192.168.1.1',
    'username': 'admin',
    'password': 'password123',
    'secret':   'cisco123',  # Enable password if required
}

def backup_device_config(device):
    today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_folder = "backups"
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        
    print(f"[*] Connecting to {device['host']}...")
    try:
        # Establish SSH connection
        net_connect = ConnectHandler(**device)
        
        # Enter enable mode if a secret password is provided
        if device.get('secret'):
            net_connect.enable()
            
        print("[*] Retrieving running configuration...")
        output = net_connect.send_command('show running-config')
        
        # Save output to a timestamped file
        filename = f"{backup_folder}/{device['host']}_{today}.txt"
        with open(filename, 'w') as backup_file:
            backup_file.write(output)
            
        print(f"[+] Backup successfully saved to {filename}")
        net_connect.disconnect()
        
    except Exception as e:
        print(f"[-] Failed to connect or retrieve config from {device['host']}: {e}")

if __name__ == "__main__":
    print("=== Network Device Configuration Backup Tool ===")
    backup_device_config(cisco_device)
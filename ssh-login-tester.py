import paramiko
import ipaddress
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def ssh_login(ip, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=username, password=password, timeout=5)
        print(f"\033[92mSuccessful login: {ip}\033[0m")  # Green text
        client.close()
        return True
    except paramiko.AuthenticationException:
        print(f"Authentication failed for {ip}")
    except paramiko.SSHException as sshException:
        print(f"Unable to establish SSH connection: {sshException} for {ip}")
    except Exception as e:
        print(f"Exception in connecting to {ip}: {e}")
    return False

def scan_subnet(subnet, username, password, mode, max_workers=20):
    network = ipaddress.ip_network(subnet)
    targets_file = "targets/ssh_targets.txt"
    
    if not os.path.exists("targets"):
        os.makedirs("targets")
        
    if not os.path.exists(targets_file):
        open(targets_file, "w").close()

    with open(targets_file, "r") as f:
        scanned_ips = set(line.strip() for line in f)
        
    if mode == "scan":
        new_targets = [str(ip) for ip in network.hosts() if str(ip) not in scanned_ips]
    elif mode == "rescan":
        new_targets = list(scanned_ips)
    else:
        print("Invalid mode. Use 'scan' to scan a subnet and save targets, or 'rescan' to scan saved targets.")
        sys.exit(1)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {executor.submit(ssh_login, ip, username, password): ip for ip in new_targets}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            result = future.result()
            if result is False:  # Only log IPs that failed authentication
                with open(targets_file, "a") as f:
                    f.write(ip + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <subnet> <username> <password> <scan|rescan>")
        sys.exit(1)

    subnet = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    mode = sys.argv[4]

    scan_subnet(subnet, username, password, mode)

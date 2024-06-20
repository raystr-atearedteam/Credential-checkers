import paramiko
import ipaddress
import sys

def ssh_login(ip, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=username, password=password, timeout=5)
        print(f"Successful login: {ip}")
        client.close()
    except paramiko.AuthenticationException:
        print(f"Authentication failed for {ip}")
    except paramiko.SSHException as sshException:
        print(f"Unable to establish SSH connection: {sshException} for {ip}")
    except Exception as e:
        print(f"Exception in connecting to {ip}: {e}")

def scan_subnet(subnet, username, password):
    network = ipaddress.ip_network(subnet)
    for ip in network.hosts():
        ssh_login(str(ip), username, password)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <subnet> <username> <password>")
        sys.exit(1)

    subnet = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    scan_subnet(subnet, username, password)

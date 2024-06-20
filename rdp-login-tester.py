import ipaddress
import sys
import rdpclient

def rdp_login(ip, username, password):
    try:
        client = rdpclient.RDPClient()
        client.connect(ip, username, password)
        if client.is_connected:
            print(f"Successful login: {ip}")
        else:
            print(f"Failed login: {ip}")
        client.disconnect()
    except Exception as e:
        print(f"Exception in connecting to {ip}: {e}")

def scan_subnet(subnet, username, password):
    network = ipaddress.ip_network(subnet)
    for ip in network.hosts():
        rdp_login(str(ip), username, password)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <subnet> <username> <password>")
        sys.exit(1)

    subnet = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    scan_subnet(subnet, username, password)

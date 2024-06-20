import telnetlib
import ipaddress
import sys

def telnet_login(ip, username, password):
    try:
        tn = telnetlib.Telnet(ip, timeout=5)
        
        tn.read_until(b"login: ")
        tn.write(username.encode('ascii') + b"\n")
        
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
        
        result = tn.read_until(b"$", timeout=5)
        
        if b"$" in result:
            print(f"Successful login: {ip}")
        else:
            print(f"Failed login: {ip}")
        
        tn.close()
    except Exception as e:
        print(f"Exception in connecting to {ip}: {e}")

def scan_subnet(subnet, username, password):
    network = ipaddress.ip_network(subnet)
    for ip in network.hosts():
        telnet_login(str(ip), username, password)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <subnet> <username> <password>")
        sys.exit(1)

    subnet = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    scan_subnet(subnet, username, password)

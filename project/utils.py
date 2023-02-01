import secrets
import socket
import subprocess
import platform

def get_ipv4_address():
    try:
        system = platform.system()
        if system == 'Windows':
            output = subprocess.check_output("ipconfig", shell=True)
        elif system == 'Linux' or system == 'Darwin':
            output = subprocess.check_output("ifconfig", shell=True)
        else:
            return "Unsupported platform"
        lines = output.decode("utf-8").split("\n")
        for line in lines:
            if "inet" in line and system == 'Darwin':
                parts = line.split()
                return parts[1]
            elif "inet" in line and system == 'Linux':
                parts = line.split()
                if parts[0] == "inet":
                    return parts[1]
            elif "IPv4" in line and system == 'Windows':
                parts = line.split(":")
                if len(parts) == 2:
                    return parts[1].strip()
    except Exception as e:
        print("Error: ", e)

        
def get_port_and_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    ip_address, port = sock.getsockname()
    sock.close()
    public_ip = get_ipv4_address()
    return (public_ip, port)


def create_room_id():
    return secrets.token_urlsafe(6)


if __name__ == "__main__":
	print(create_room_id())
	print(type(create_room_id()))
	print(get_port_and_ip())

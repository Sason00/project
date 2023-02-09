import secrets
import socket
import subprocess
import platform
import json


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

ip, port = get_port_and_ip()

def create_room_id():
    return secrets.token_urlsafe(6)

def create_user(user_data={"username": "first2", "password": "123", "email": "check6@gmail.com", "type": "guide"}):
    # Create the data to send
    ip, port = get_port_and_ip()
    data = {"command": "create user", "data": user_data} 
    # json the data
    data = json.dumps(data)

    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send the data to the server
    sock.sendto(bytes(data, encoding="utf-8"), ("localhost", 5005))

    try:
        # Wait for the response
        response_jsond, addr = sock.recvfrom(1024)

        # Unjson the response
        response = json.loads(response_jsond)
    except ConnectionResetError:
        return {"message": "There is a problem with the server", "code": 104}

    # Print the response
    print(response["message"])
    print("Code: ",response["code"])


    # Close the socket
    sock.close()

def send_login(user_data={"username": "first2", "password": "123", "email": "check6@gmail.com", "type": "guide"}):
    # Create the data to send
    ip, port = get_port_and_ip()
    data = {"command": "login", "data": user_data}
    # json the data
    data = json.dumps(data)

    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send the data to the server
        sock.sendto(bytes(data, encoding="utf-8"), ("localhost", 5005))

        # Wait for the response
        response_jsond, addr = sock.recvfrom(1024)
    except ConnectionResetError:
        return {"message": "There is a problem with the server", "code": 104}

    # Unjson the response
    response = json.loads(response_jsond)
    
    # Close the socket
    sock.close()

    return response



def activate_room(user_data={"username": "first2", "password": "123", "email": "check6@gmail.com"}, data={"host_ip": ip, "host_port": port}):
    ip, port = get_port_and_ip()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = {"command": "open room", "user_info": user_data, "data": data}
    data = json.dumps(data)
    client_socket.sendto(bytes(data, encoding="utf-8"), ("localhost", 5005))
    response, _ = client_socket.recvfrom(1024)
    response = json.loads(response)
    if response["code"] == 200:
        print("Room successfully opened.")
    else:
        print("Error: " + response["message"])
    client_socket.close()
    

if __name__ == "__main__":
    pass
"""
    print(create_room_id())
    print(type(create_room_id()))
    print(get_port_and_ip())
"""



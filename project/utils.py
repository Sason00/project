import secrets
import socket
import subprocess
import platform
import json
import sys

"""
todo:
make a class that wrap everything nicely
"""

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


def send_udp_large_data(sock, data, buffer_size=1024):
    # Calculate the number of packets required to send the entire data
    packet_count = len(data) // buffer_size
    if len(data) % buffer_size != 0:
        packet_count += 1

    # Send the data in pieces
    for i in range(packet_count):
        # Get the current piece of data to send
        start = i * buffer_size
        end = min(start + buffer_size, len(data))
        data_chunk = data[start:end]

        # Send the current piece of data to the server
        sock.sendto(data_chunk, ("localhost", 5005))


def send_data(data):
    # json the data
    data = json.dumps(data)

    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send the data to the server
        send_udp_large_data(sock, bytes(data, encoding="utf-8"))

        # Wait for the response
        response_jsond, addr = sock.recvfrom(1024)
    except ConnectionResetError:
        sock.close()
        return {"message": "There is a problem with the server", "code": 104}

    # Unjson the response
    response = json.loads(response_jsond)
    
    # Close the socket
    sock.close()

    return response

        
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


def close_room(user_data={"username": "first2", "password": "123", "email": "check6@gmail.com"}):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = {"command": "close room", "user_info": user_data}
    response = send_data(data)
    if response["code"] == 200:
        print("Room was closed successfully")
    else:
        print("Error: " + response["message"])
    client_socket.close()


def activate_room(user_data={"username": "first2", "password": "123", "email": "check6@gmail.com"}, data={"host_ip": ip, "host_port": port}):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = {"command": "open room", "user_info": user_data, "data": data}
    response = send_data(data)
    if response["code"] == 200:
        print("Room successfully opened.")
    else:
        print("Error: " + response["message"])
    client_socket.close()


def get_host(room_code=""):
    data = {"command": "get host by code", "room_code": room_code}

    r = send_data(data)
    return r


def get_user_type(email):
    data = {"command": "get type by email", "email": email}
    r = send_data(data)
    if r["code"] == 104:
        r["user type"] = None
        return r
    return r


def get_user_name(email):
    data = {"command": "get type by name", "email": email}
    r = send_data(data)
    if r["code"] == 104:
        r["user name"] = None
        return r
    return r
    

class Client:
    def __init__(self, username=None, password=None, email=None):
        if not(password is None or email is None):
            self.username = get_user_name(email)["user name"]
            self.password = password
            self.email = email
            self.type = get_user_type(self.email)["user type"]
            self.user_data = {"username": self.username, "password": self.password, "email": self.email}
        else:
            self.username = None
            self.password = None
            self.email = None
            self.type = "normal"
            self.user_data = None

    def change_user(self, username=None, password=None, email=None):
        if not(password is None or email is None):
            self.username = get_user_name(email)["user name"]
            self.password = password
            self.email = email
            self.type = get_user_type(self.email)["user type"]
            self.user_data = {"username": self.username, "password": self.password, "email": self.email}
        else:
            self.username = None
            self.password = None
            self.email = None
            self.type = "normal"
            self.user_data = None

    def activate_room(self, data={"host_ip": ip, "host_port": port}):
        if self.user_data != None:
            return activate_room(self.user_data, data)
        return {"message": "You are not logged in"}

    def close_room(self):
        if self.user_data != None:
            return close_room(user_data)
        return {"message": "You are not logged in"}

    def send_login(self):
        if self.user_data != None:
            return send_login(self.user_data)
        return {"message": "You are not logged in"}

    def create_user(self, data):
        if self.user_data != None:
            self.change_user(data["username"], data["password"], data["email"])
            return create_user(data)
        return {"message": "username or password or mail are not valid"}

    def get_host(self, room_code):
        return get_host(room_code)


if __name__ == "__main__":
    print(get_user_name("23456789@gmail.com"))
    # print(get_port_and_ip())
"""
    activate_room({"username": "1", "password": "1", "email": "12345678@gmail.com"}, {"host_ip": ip, "host_port": port})
    print(get_host("XzcOnul3"))

    printc(create_room_id())
    print(type(create_room_id()))
    print(get_port_and_ip())
"""



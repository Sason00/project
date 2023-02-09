import socket
import json
import utils


def create_user():
    # Create the data to send
    ip, port = utils.get_port_and_ip()
    # data = {"command": "create user", "data": {"username": "first2", "password": "123", "email": "check6@gmail.com", "type": "guide"}}
    data = {"command": "create user", "data": {"username": "first3", "password": "123", "email": "check3@gmail.com", "type": "guide"}}
    # json the data
    data = json.dumps(data)
    print(data, bytes(data, encoding="utf-8"))

    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send the data to the server
    sock.sendto(bytes(data, encoding="utf-8"), ("localhost", 5005))


    # Wait for the response
    response_jsoned, addr = sock.recvfrom(1024)

    # Unjson the response
    response = json.loads(response_jsoned)

    # Print the response
    print(response["message"])
    print("Code: ",response["code"])


    # Close the socket
    sock.close()


def activate_room():
    ip, port = utils.get_port_and_ip()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = {"command": "open room", "user_info": {"username": "first3", "password": "123", "email": "check3@gmail.com", "type": "guide"}, "data": {"host_ip": ip, "host_port": port}}
    data = json.dumps(data)
    client_socket.sendto(bytes(data, encoding="utf-8"), ("localhost", 5005))
    response, _ = client_socket.recvfrom(1024)
    response = json.loads(response)
    if response["code"] == 200:
        print("Room successfully opened.")
    else:
        print("Error: " + response["message"])
    client_socket.close()

activate_room()

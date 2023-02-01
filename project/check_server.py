import socket
import pickle
import utils

def create_user():
    # Create the data to send
    ip, port = utils.get_port_and_ip()
    # data = {"command": "create user", "data": {"username": "first2", "password": "123", "email": "check6@gmail.com", "type": "guide"}}
    data = {"command": "login", "data": {"username": "first2", "password": "123", "email": "check6@gmail.com", "type": "guide"}}
    # Pickle the data
    data = pickle.dumps(data)

    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send the data to the server
    sock.sendto(data, ("localhost", 5005))


    # Wait for the response
    response_pickled, addr = sock.recvfrom(1024)

    # Unpickle the response
    response = pickle.loads(response_pickled)

    # Print the response
    print(response["message"])
    print("Code: ",response["code"])


    # Close the socket
    sock.close()


def activate_room():
    ip, port = utils.get_port_and_ip()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = {"command": "open room", "user_info": {"username": "first2", "password": "123", "email": "check6@gmail.com"}, "data": {"host_ip": ip, "host_port": port}}
    client_socket.sendto(pickle.dumps(data), ("localhost", 5005))
    response, _ = client_socket.recvfrom(1024)
    response = pickle.loads(response)
    if response["code"] == 200:
        print("Room successfully opened.")
    else:
        print("Error: " + response["message"])
    client_socket.close()

activate_room()

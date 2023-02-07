import socket
import threading
import sqlite3
import hashlib
import pickle
import re
import utils

salt = b'your_salt'

# Function to handle incoming connections
def handle_connection(data, addr):
    # Unpickle the data
    data = pickle.loads(data)
    print(data, addr)
    # example {"command": "create user", "data": {"username": "first2", "password": "123", "email": "check6@gmail.com", "type": "guide"}}
    # Check the command
    if data["command"] == "create user":
        # Get the user data
        user_data = data["data"]

        # Encrypt the password
        password = user_data["password"].encode()
        salted_password = hashlib.sha256(password + salt).hexdigest()

        # Check if email is valid
        email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
       
        if re.search(email_regex, user_data["email"]):
            # Connect to the database
            connection = sqlite3.connect("mydatabase.db")
            cursor = connection.cursor()

            # Check if the email is already in use
            cursor.execute("SELECT * FROM Users WHERE email=?", (user_data["email"],))
            result = cursor.fetchone()

            if result:
                send_response(addr, {"message": "Email already in use.", "code": 406})
                print("Email already in use.")
            else:
                # Insert the data into the users table
                if user_data["type"] == 'normal':
                    # Insert the data into the users table
                    cursor.execute("INSERT INTO users (username, password, email, type) VALUES (?, ?, ?, ?)", (user_data["username"], salted_password, user_data["email"], user_data["type"]))
                    send_response(addr, {"message": "User created successfully.", "code": 201})
                    print("User created successfully.")
                elif user_data["type"] == 'guide':
                    # Insert the data into the users table
                    room_code = utils.create_room_id()
                    cursor.execute("INSERT INTO users (username, password, email, type, room_code) VALUES (?, ?, ?, ?, ?)", (user_data["username"], salted_password, user_data["email"], user_data["type"], room_code))
                    send_response(addr, {"message": "User created successfully.", "code": 201, "room code": room_code})
                    print("User created successfully.")
                    print(f"{room_code = }")
                else:
                    send_response(addr, {"message": "Incorrect user type.", "code": 406})
                    print("Incorrect user type.")
                connection.commit()
            connection.close()
        else:
            send_response(addr, {"message": "Invalid command.", "code": 400})
            print("Invalid email address.")
    elif data["command"] == "login":
        # this if is just for check, need to be checked every time
        user_id = login(data["data"]["password"], data["data"]["email"])
        if user_id:
            send_response(addr, {"message": "You logged in.", "code": 201})
            print("You logged in.", user_id)
        else:
            send_response(addr, {"message": "Incorrect email or password", "code": 400})
    elif data["command"] == "open room":
        user_info = data["user_info"]
        user_id = login(user_info["password"], user_info["email"])
        if user_id is None:
            # Return error message to client
            send_response(addr, {"message": "Invalid password or mail.", "code": 401})
            return
        user_type = get_user_type(user_id)
        if user_type != "guide":
            # Return error message to client
            send_response(addr, {"message": "You are not authorized to open a room.", "code": 403})
            return
        room_code = get_room_code(user_id)
        host_ip = data["data"]["host_ip"]
        host_port = data["data"]["host_port"]
        insert_room(room_code, user_id, host_ip, host_port)
        # Return success message to client
        send_response(addr, {"message": "Room successfully opened.", "code": 200})
    else:
        print(data["command"], data["command"] == "open room")
        send_response(addr, {"message": "Invalid command.", "code": 400})
        print("Invalid command.")


def send_response(client, data):
    data = pickle.dumps(data)
    sock.sendto(data, client)


def compare_passwords(password:bytes, hashed_password:bytes, salt:bytes):
    salted_password = hashlib.sha256(password + salt).hexdigest().encode()
    return salted_password == hashed_password


def login(password, email):
    conn = sqlite3.connect("mydatabase.db")
    c = conn.cursor()
    c.execute("SELECT id, password FROM users WHERE email = ?", (email, ))
    user = c.fetchone()
    print(user)
    if user is not None:
        user_id, hashed_password = user
        print(user_id, hashed_password)
        if compare_passwords(str.encode(password), str.encode(hashed_password), salt):
            return user_id
    return None

def get_room_code(user_id):
    connection = sqlite3.connect("mydatabase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT room_code FROM users WHERE id=?", (user_id,))
    room_code = cursor.fetchone()
    if room_code:
        room_code = room_code[0]
    else:
        room_code = None
    connection.close()
    return room_code

def insert_room(room_code, user_id, host_ip, host_port):
    connection = sqlite3.connect("mydatabase.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO active_rooms (room_code, id, host_ip, host_port) VALUES (?, ?, ?, ?)", (room_code, user_id, host_ip, host_port))
    connection.commit()

def get_user_type(user_id):
    connection = sqlite3.connect("mydatabase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT type FROM users WHERE id=?", (user_id,))
    user_type = cursor.fetchone()[0]
    connection.close()
    return user_type

# Function to receive data
def receive_data():
    while True:
        # Receive data from the socket
        data, addr = sock.recvfrom(1024)
        # Start a new thread to handle the connection
        threading.Thread(target=handle_connection, args=(data, addr)).start()

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the address and port
sock.bind(("localhost", 5005))

# Start the receive data function in a new thread
threading.Thread(target=receive_data).start()

# Keep the program running
while True:
    pass

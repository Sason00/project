import socket
import threading
import sqlite3
import hashlib
import hmac
import json
import json
import re
import utils

"""
todo list:
"""

SERVER_IP = ""
SERVER_PORT = 5005

salt = b'your_salt'

# Function to handle incoming connections
def handle_connection(data, addr):
    # Unjson the data
    data = json.loads(data.decode(), strict=False)
    print(data, addr)

    sql_injection_pattern = re.compile(r"(?:')|(?:--)|(\b(select|update|delete|insert|drop|alter)\b)")

    """
    Doesn't work, check later
        # check for SQL injection
        if sql_injection_pattern.search(str(data)):
            send_response(addr, {"message": "Invalid command.", "code": 400})
            print("Possible SQL injection detected!")
    """ 
    # example {"command": "create user", "data": {"username": "first2", "password": "123", "email": "check6@gmail.com", "type": "guide"}}
    # Check the command
    if data["command"] == "create user":
        # Get the user data
        user_data = data["data"]

        # Encrypt the password
        password = user_data["password"].encode()
        salted_password = hashlib.sha256(password + salt).hexdigest()

        # Check if email is valid
        email_regex = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
       
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
        if user_info == None:
            send_response(addr, {"message": "You are not authorized to open a room.", "code": 403})
            return
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
        host_listener_port = data["data"]["host_listener_port"]
        insert_room(room_code, user_id, host_ip, host_port, host_listener_port)
        # Return success message to client
        send_response(addr, {"message": "Room successfully opened.", "code": 200, "room code": room_code})
    elif data["command"] == "close room":
        user_info = data["user_info"]
        if user_info == None:
            send_response(addr, {"message": "You are not authorized to open a room.", "code": 403})
            return
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
        with sqlite3.connect("mydatabase.db") as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM active_rooms WHERE id=?;", (user_id, ))
            connection.commit()
            send_response(addr, {"message": "Room was closed successfully", "code": 204})
    elif data["command"] == "get host by code":
        room_code = data["room_code"]
        with sqlite3.connect("mydatabase.db") as conn:
            c = conn.cursor()
            c.execute("SELECT host_ip, host_port, host_listener_port FROM active_rooms WHERE room_code = ?", (room_code, ))
            host_ip, host_port, host_listener_port = c.fetchone()
            send_response(addr, {"message": "Here are the host ip and port", "code": 200, "host ip": host_ip, "host port": host_port, "host_listener_port": host_listener_port})    
    elif data["command"] == "get type by email":
        email = data["email"]
        with sqlite3.connect("mydatabase.db") as conn:
            c = conn.cursor()
            c.execute("SELECT type FROM users WHERE email = ?", (email, ))
            user_type = c.fetchone()
            if not(user_type is None):
                user_type = user_type[0]
                send_response(addr, {"message": f"The user is {user_type}", "code": 200, "user type": user_type})    
            else:
                send_response(addr, {"message": "Invalid mail.", "code": 401, "user type": None})
    elif data["command"] == "get type by name":
        email = data["email"]
        with sqlite3.connect("mydatabase.db") as conn:
            c = conn.cursor()
            c.execute("SELECT username FROM users WHERE email = ?", (email, ))
            user_name = c.fetchone()
            if not(user_name is None):
                user_name = user_name[0]
                send_response(addr, {"message": f"The username is {user_name}", "code": 200, "user name": user_name})    
            else:
                send_response(addr, {"message": "Invalid mail.", "code": 401, "user name": None})
    elif data["command"] == "update room code":
        user_info = data["user_info"]
        new_room_code = data["new_room_code"]
        if len(new_room_code) == 0:
            send_response(addr, {"message": "Invalid room code.", "code": 401})
        changed = update_room_code(new_room_code, user_info["email"], user_info["password"])
        if changed:
            send_response(addr, {"message": "A matching record was found. No updates needed.", "code": 401})
            print("A matching record was found. No updates needed.")
        else:
            send_response(addr, {"message": "Room code updated successfully.", "code": 201})
            print("Room code updated successfully.")

    else:
        print(data["command"], data["command"] == "open room")
        send_response(addr, {"message": "Invalid command.", "code": 400})
        print("Invalid command.")


def update_room_code(new_room_code, email, password):
    print(new_room_code, email, password)
    result = None
    # Connect to the SQLite database using the "with" statement
    with sqlite3.connect('mydatabase.db') as conn:
        cursor = conn.cursor()
        # Check if the room_code exists for the given mail and password
        user_id = login(password, email)
        if user_id:
            cursor.execute("SELECT * FROM users WHERE room_code = ?", (new_room_code,))
            result = cursor.fetchone()
            print(result, bool(result))

            if not bool(result):
                # No matching records found, update the room_code
                cursor.execute("UPDATE users SET room_code = ? WHERE id = ?", (new_room_code, user_id))
                conn.commit()

    return bool(result)


def send_response(client, data):
    data = json.dumps(data)
    sock.sendto(bytes(data, encoding="utf-8"), client)


def compare_passwords(password:bytes, hashed_password:bytes, salt:bytes):
    print("hi")
    salted_password = hashlib.sha256(password + salt).hexdigest().encode()
    print(salted_password)
    print(hashed_password)
    return hmac.compare_digest(salted_password, hashed_password)


def login(password, email):
    with sqlite3.connect("mydatabase.db") as conn:
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
    with sqlite3.connect("mydatabase.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT room_code FROM users WHERE id=?", (user_id,))
        room_code = cursor.fetchone()
        if room_code:
            room_code = room_code[0]
        else:
            room_code = None
    return room_code

def insert_room(room_code, user_id, host_ip, host_port, host_listener_port):
    connection = sqlite3.connect("mydatabase.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO active_rooms (room_code, id, host_ip, host_port, host_listener_port) VALUES (?, ?, ?, ?, ?)", (room_code, user_id, host_ip, host_port, host_listener_port))
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
        # data, addr = sock.recvfrom(1024)
        data = b""
        while True:
            chunk, addr = sock.recvfrom(1024*2)
            data += chunk
            if len(chunk) < 1024:
                # end of message
                break
        print(data, "hi")
        # Start a new thread to handle the connection
        threading.Thread(target=handle_connection, args=(data, addr)).start()

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# set the buffer size to 4096 bytes
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1048576)

# Bind the socket to the address and port
sock.bind((SERVER_IP, SERVER_PORT))

# Start the receive data function in a new thread
threading.Thread(target=receive_data).start()

# Keep the program running
while True:
    pass

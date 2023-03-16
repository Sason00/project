import socket
import pyaudio
import wave
import utils
import threading

"""
1
1
12345678@gmail.com
"""

UDP_IP = "127.0.0.1"
UDP_PORT = 51166
host_listener_port = 51167

r = utils.activate_room({"username": "1", "password": "1", "email": "12345678@gmail.com"}, {"host_ip": UDP_IP, "host_port": UDP_PORT, "host_listener_port": host_listener_port})
print(r)

chunk = 1024      # Each chunk will consist of 1024 samples
sample_format = pyaudio.paInt16      # 16 bits per sample
channels = 1      # Number of audio channels
fs = 44100        # Record at 44100 samples per second
time_in_seconds = 30

sock = socket.socket(socket.AF_INET, # Internet
                       socket.SOCK_DGRAM) # UDP

clients = []

server = socket.socket(socket.AF_INET, # Internet
                       socket.SOCK_DGRAM) # UDP

server.bind((UDP_IP, host_listener_port))


p = pyaudio.PyAudio()  # Create an interface to PortAudio


def send(msg, ip, port):
    sock.sendto(msg, (ip, port))

def broadcast(msg):
    for i in clients:
        send(msg, i[0], i[1])

def handle_connection():
    data, addr = server.recvfrom(1024)
    print(addr[0], addr[1])
    if data == b"please activate mic":
        broadcast(b"listen to |" + addr[0].encode() + b":" + str(addr[1]).encode())
    elif data.startswith(b"accept me"):
        if addr not in clients:
            clients.append(addr)
            send(b"connected", addr[0], addr[1])

def list_devices():
    p2 = pyaudio.PyAudio()
    device_count = p2.get_device_count()
    for i in range(0, device_count):
        info = p2.get_device_info_by_index(i)
        print("Device {} = {}".format(info["index"], info["name"]))
    print(p2.get_default_input_device_info())

list_devices()

print('-----Now Recording-----')
 
#Open a Stream with the values we just defined
stream = p.open(format=sample_format,
                channels = p.get_default_input_device_info()["maxInputChannels"],
                rate = fs,
                frames_per_buffer = chunk,
                input = True,
                output=False,
                input_device_index=p.get_default_input_device_info()["index"])
 
frames = []  # Initialize array to store frames

print(f"{fs = }, {chunk = }, {time_in_seconds = }")
print(int(fs / chunk * time_in_seconds))

# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * time_in_seconds)):
    # check for connections
    t = threading.Thread(target=handle_connection)
    t.daemon = True
    t.start()
    
    data = stream.read(chunk)
    frames.append(data)
    broadcast(data)
 
# Stop and close the Stream and PyAudio
stream.stop_stream()
stream.close()
p.terminate()
 
print('-----Finished Recording-----')


broadcast("stop".encode())
print(utils.close_room({"username": "1", "password": "1", "email": "12345678@gmail.com"}))

"""
file = wave.open("output1.wav", 'wb')
file.setnchannels(channels)
file.setsampwidth(p.get_sample_size(sample_format))
file.setframerate(fs)
 
#Write and Close the File
file.writeframes(b''.join(frames))
file.close()
"""

import socket
import pyaudio
import wave
import utils
import random

ROOM_CODE = "nSMQ4PxU"

"""
1
1
12345678@gmail.com
"""

d = utils.get_host(ROOM_CODE)
UDP_IP, UDP_PORT, host_listener_port = d["host ip"], d["host port"], d["host_listener_port"]
print(UDP_IP, UDP_PORT)

chunk = 1024      # Each chunk will consist of 1024 samples
sample_format = pyaudio.paInt16      # 16 bits per sample
channels = 1      # Number of audio channels
fs = 44100        # Record at 44100 samples per second
time_in_seconds = 10

_, PORT, _ = utils.get_port_and_ip()

client = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

def list_devices():
    p2 = pyaudio.PyAudio()
    device_count = p2.get_device_count()
    for i in range(0, device_count):
        info = p2.get_device_info_by_index(i)
        print("Device {} = {}".format(info["index"], info["name"]))
    print(p2.get_default_output_device_info())

def send(msg):
    client.sendto(msg, (UDP_IP, host_listener_port))
        
list_devices()

p = pyaudio.PyAudio()  # Create an interface to PortAudio
stream = p.open(channels = p.get_default_output_device_info()["maxOutputChannels"],
                format=sample_format,
                rate = fs, # somehow when it's normal it 2 times faster
                frames_per_buffer = chunk,
                output=True,
                input=False,
                output_device_index=p.get_default_output_device_info()["index"])


frames = []
is_done = False
send(b"accept me")
print("listening")
while not is_done:
    data, addr = client.recvfrom(1024*100) # buffer size is 1024 bytes
    if data == b"stop":
        print(data)
        is_done = True
    if data[0] == 123 and data[-1] == 125:
        print(data)
    else:
        frames.append(data)
        stream.write(data)

    if random.random() > 0.8:
        send(b"please activate mic")
        

stream.stop_stream()
stream.close()
p.terminate()

"""
file = wave.open("output2.wav", 'wb')
file.setnchannels(channels)
file.setsampwidth(p.get_sample_size(sample_format))
file.setframerate(fs // 2)
 
#Write and Close the File
file.writeframes(b''.join(frames))
file.close()
"""

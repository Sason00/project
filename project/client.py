import socket
import pyaudio
import wave

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

chunk = 1024      # Each chunk will consist of 1024 samples
sample_format = pyaudio.paInt16      # 16 bits per sample
channels = 1      # Number of audio channels
fs = 44100        # Record at 44100 samples per second
time_in_seconds = 10

sock = socket.socket(socket.AF_INET, # Internet
                       socket.SOCK_DGRAM) # UDP

p = pyaudio.PyAudio()  # Create an interface to PortAudio


def send(msg):
    sock.sendto(msg, (UDP_IP, UDP_PORT))
    

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
    data = stream.read(chunk)
    frames.append(data)
    send(data)
 
# Stop and close the Stream and PyAudio
stream.stop_stream()
stream.close()
p.terminate()
 
print('-----Finished Recording-----')


send("stop".encode())

"""
file = wave.open("output1.wav", 'wb')
file.setnchannels(channels)
file.setsampwidth(p.get_sample_size(sample_format))
file.setframerate(fs)
 
#Write and Close the File
file.writeframes(b''.join(frames))
file.close()
"""

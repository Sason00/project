import socket
import pyaudio
import wave
import utils
import threading
import json


class AudioRecorder:
    def __init__(self, udp_ip, udp_port, host_listener_port, client):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.host_listener_port = host_listener_port
        self.client = client
        self.r = utils.activate_room(self.client.user_data, {"host_ip": self.udp_ip, "host_port": self.udp_port, "host_listener_port": self.host_listener_port})
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 1
        self.fs = 44100
        self.time_in_seconds = 30
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clients = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.udp_ip, self.host_listener_port))
        self.p = pyaudio.PyAudio()
        self.frames = []

    def send(self, msg, ip, port):
        self.sock.sendto(msg, (ip, port))

    def broadcast(self, msg):
        for i in self.clients:
            self.send(msg, i[0], i[1])

    def handle_connection(self):
        data, addr = self.server.recvfrom(1024)
        print(addr[0], addr[1])
        print(data)
        if data == b"please activate mic":
            msg = {"msg": "listen to", "ip": addr[0], "port": addr[1]}
            msg = json.dumps(msg)
            self.broadcast(bytes(msg, encoding="utf-8"))
        elif data.startswith(b"accept me"):
            if addr not in self.clients:
                self.clients.append(addr)
                msg = {"msg": "connected"}
                msg = json.dumps(msg)
                self.send(bytes(msg, encoding="utf-8"), addr[0], addr[1])

    def list_devices(self):
        p2 = pyaudio.PyAudio()
        device_count = p2.get_device_count()
        for i in range(0, device_count):
            info = p2.get_device_info_by_index(i)
            print("Device {} = {}".format(info["index"], info["name"]))
        print(p2.get_default_input_device_info())

    def _run(self):
        print('-----Now Recording-----')
        stream = self.p.open(format=self.sample_format,
                             channels=self.p.get_default_input_device_info()["maxInputChannels"],
                             rate=self.fs,
                             frames_per_buffer=self.chunk,
                             input=True,
                             output=False,
                             input_device_index=self.p.get_default_input_device_info()["index"])
        print(f"{self.fs=}, {self.chunk=}, {self.time_in_seconds=}")
        self.frames = []  
        for i in range(0, int(self.fs / self.chunk * self.time_in_seconds)):
            t = threading.Thread(target=self.handle_connection)
            t.daemon = True
            t.start()
            data = stream.read(self.chunk)
            self.frames.append(data)
            self.broadcast(data)
        stream.stop_stream()
        stream.close()
        self.p.terminate()
        print('-----Finished Recording-----')
        self.broadcast("stop".encode())
        print(utils.close_room(self.client.user_data))

    def run(self):
        threading.Thread(target=self._run, daemon=True).start()

    def run_and_save(self, name):
        threading.Thread(target=self._run, daemon=True).start()
        self.save(name)

    def save(self, file_name):
        try:
            with wave.open(file_name, 'wb') as file:
                file.setnchannels(self.channels)
                file.setsampwidth(self.p.get_sample_size(self.sample_format))
                file.setframerate(self.fs)
                file.writeframes(b''.join(self.frames))
        except (IOError, EOFError, ValueError) as e:
            print(f"Error occurred while saving the file: {e}") 

def main():
    # Create a client object
    client = utils.Client("1", "1", "12345678@gmail.com")

    utils.close_room(client.user_data)

    # Create an AudioRecorder object with the client object and parameters
    recorder = AudioRecorder(client=client, udp_ip="127.0.0.1", udp_port=51166,
                             host_listener_port=51167)

    # Start recording in the background
    recorder.run_and_save("output1.wav")

if __name__ == "__main__":
    main()

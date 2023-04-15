import socket
import pyaudio
import wave
import utils
import random
import threading
import json

class AudioClient:
    def __init__(self, room_code, client=None):
        self.room_code = room_code
        self.d = utils.get_host(self.room_code)
        self.UDP_IP, self.UDP_PORT, self.host_listener_port = self.d["host ip"], self.d["host port"], self.d["host_listener_port"]
        self.chunk = 1024      # Each chunk will consist of 1024 samples
        self.sample_format = pyaudio.paInt16      # 16 bits per sample
        self.channels = 1      # Number of audio channels
        self.fs = 44100        # Record at 44100 samples per second
        self.time_in_seconds = 10
        _, self.PORT, _ = utils.get_port_and_ip()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.is_done = False
        self.thread = None


    def list_devices(self):
        device_count = self.p.get_device_count()
        for i in range(0, device_count):
            info = self.p.get_device_info_by_index(i)
            print("Device {} = {}".format(info["index"], info["name"]))
        print(self.p.get_default_output_device_info())

    def send(self, msg):
        self.client.sendto(msg, (self.UDP_IP, self.host_listener_port))

    def run(self):
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def run_and_save(self, name):
        threading.Thread(target=self._run, daemon=True).start()
        self.save(name)
    
    def _run(self):
        stream = self.p.open(channels=self.p.get_default_output_device_info()["maxOutputChannels"],
                              format=self.sample_format,
                              rate=self.fs,  # somehow when it's normal it 2 times faster
                              frames_per_buffer=self.chunk,
                              output=True,
                              input=False,
                              output_device_index=self.p.get_default_output_device_info()["index"])
        msg = {"msg": "accept me"}
        self.send(b"accept me")
        print("listening")
        while not self.is_done:
            data, addr = self.client.recvfrom(1024 * 100)  # buffer size is 1024 bytes
            if data == b"stop":
                print(data)
                self.is_done = True
            if data[0] == 123 and data[-1] == 125:
                print(data)
            else:
                self.frames.append(data)
                stream.write(data)
            """
            if random.random() > 0.8:
                self.send(b"please activate mic")
            """
        stream.stop_stream()
        stream.close()
        self.p.terminate()

    def save(self, file_name):
        try:
            with wave.open(file_name, 'wb') as file:
                file.setnchannels(self.channels)
                file.setsampwidth(self.p.get_sample_size(self.sample_format))
                file.setframerate(self.fs)
                file.writeframes(b''.join(self.frames))
        except (IOError, EOFError, ValueError) as e:
            print(f"Error occurred while saving the file: {e}") 

    def connect(self):
        self.run()

    def send_msg(self, msg):
        msg = {"msg": "send msg", "msg content": msg}
        msg = json.dumps(msg)
        print(msg)
        self.send(bytes(msg, encoding="utf-8"))

if __name__ == "__main__":
    audio_client = AudioClient("nSMQ4PxU")
    audio_client.run_and_save("output2.wav")

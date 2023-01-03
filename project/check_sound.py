import pyaudio
import wave
 
chunk = 1024      # Each chunk will consist of 1024 samples
sample_format = pyaudio.paInt16      # 16 bits per sample
channels = 1      # Number of audio channels
fs = 44100        # Record at 44100 samples per second
time_in_seconds = 1
filename = "soundsample.wav"
 
p = pyaudio.PyAudio()  # Create an interface to PortAudio
 
print('-----Now Recording-----')
 
#Open a Stream with the values we just defined
stream = p.open(format=sample_format,
                channels = channels,
                rate = fs,
                frames_per_buffer = chunk,
                input = True,
                output=True)
 
frames = []  # Initialize array to store frames

print(f"{fs = }, {chunk = }, {time_in_seconds = }")
print(int(fs / chunk * time_in_seconds))

# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * time_in_seconds)):
    data = stream.read(chunk)
    frames.append(data)
 
# Stop and close the Stream and PyAudio
stream.stop_stream()
stream.close()
p.terminate()
 
print('-----Finished Recording-----')

p = pyaudio.PyAudio()  # Create an interface to PortAudio
stream = p.open(channels = 2,
                format=sample_format,
                rate = fs // 2, # somehow when it's normal it 2 times faster
                frames_per_buffer = chunk,
                output=True,
                input=False,
                output_device_index=4)

for i in frames:
    stream.write(i)

stream.stop_stream()
stream.close()
p.terminate()

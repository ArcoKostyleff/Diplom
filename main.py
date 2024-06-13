#Transmitter code starts here
#Transmitter code starts here
import time
import pyaudio
import wave
import serial
import RPi.GPIO as GPIO
import os
import sys, getopt
from edge_impulse_linux.audio import AudioImpulseRunner
# device index is 2

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 16000 # 44.1kHz sampling rate
chunk = 1024 # 2^12 samples for buffer
record_secs = 1 # 1 second to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav' # name of .wav file

id_det = 1

audio = pyaudio.PyAudio() # create pyaudio instantiation

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
lora = serial.Serial('/dev/ttyAMA0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
time.sleep(1)

# create pyaudio stream
def sendData():
    msg = "DET " + str(id_det)
    lora.write(msg)
    print "-signal emmited"
def classify(wav):
    answer = 100
#     call Edge impulse
    dir_path = os.path.dirname(os.path.realpath(__file__))
    modelfile = os.path.join(dir_path, model)

    with AudioImpulseRunner(modelfile) as runner:
        try:
            model_info = runner.init()
            labels = model_info['model_parameters']['labels']
            print('Loaded runner for "' + model_info['project']['owner'] + ' / ' + model_info['project']['name'] + '"')

            selected_device_id = None
            if len(args) >= 2:
                selected_device_id=int(args[1])
                print("Device ID "+ str(selected_device_id) + " has been provided as an argument.")

            for res, audio in runner.classifier(device_id=selected_device_id):
                #print('Result (%d ms.) ' % (res['timing']['dsp'] + res['timing']['classification']), end='')
                for label in labels:
                    score = res['result']['classification'][label]
                    if score >80:
                        print "-!DANGER DETECTED"
                        sendData()
                 #   print('%s: %.2f\t' % (label, score), end='')
               # print('', flush=True)

        finally:
            if (runner):
                runner.stop()
  

def recording(ev = None):
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=chunk)
    print("-recording")
    frames = []

    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)

    print("-stopped")

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    classify(wavefile)

try:
    while True:
        recording()   
except KeyboardInterrupt:
    print "Exiting Program"
except:
    print "Error, Exiting Program"
finally:
    audio.terminate()
    lora.stop()
    pass



def signal_handler(sig, frame):
    print('Interrupted')
    if (runner):
        runner.stop()
    sys.exit(0)
import time
import pyaudio
import wave
import serial
import RPi.GPIO as GPIO
import os
import sys, getopt
from edge_impulse_linux.audio import AudioImpulseRunner
# device index is 2

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 16000 # 44.1kHz sampling rate
chunk = 1024 # 2^12 samples for buffer
record_secs = 1 # 1 second to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav' # name of .wav file

id_det = 1

audio = pyaudio.PyAudio() # create pyaudio instantiation

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
lora = serial.Serial('/dev/ttyAMA0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
time.sleep(1)

# create pyaudio stream
def sendData():
    msg = "DET " + str(id_det)
    lora.write(msg)
    print "-signal emmited"
def classify(wav):
    answer = 100
#     call Edge impulse
    dir_path = os.path.dirname(os.path.realpath(__file__))
    modelfile = os.path.join(dir_path, model)

    with AudioImpulseRunner(modelfile) as runner:
        try:
            model_info = runner.init()
            labels = model_info['model_parameters']['labels']
            print('Loaded runner for "' + model_info['project']['owner'] + ' / ' + model_info['project']['name'] + '"')

            selected_device_id = None
            if len(args) >= 2:
                selected_device_id=int(args[1])
                print("Device ID "+ str(selected_device_id) + " has been provided as an argument.")

            for res, audio in runner.classifier(device_id=selected_device_id):
                #print('Result (%d ms.) ' % (res['timing']['dsp'] + res['timing']['classification']), end='')
                for label in labels:
                    score = res['result']['classification'][label]
                    if score >80:
                        print "-!DANGER DETECTED"
                        sendData()
                 #   print('%s: %.2f\t' % (label, score), end='')
               # print('', flush=True)

        finally:
            if (runner):
                runner.stop()
  

def recording(ev = None):
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=chunk)
    print("-recording")
    frames = []

    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)

    print("-stopped")

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    classify(wavefile)

try:
    while True:
        recording()   
except KeyboardInterrupt:
    print "Exiting Program"
except:
    print "Error, Exiting Program"
finally:
    audio.terminate()
    lora.stop()
    pass



def signal_handler(sig, frame):
    print('Interrupted')
    if (runner):
        runner.stop()
    sys.exit(0)

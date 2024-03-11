from requests import get
from json import loads

import pyaudio
import wave
import threading
from time import sleep


def load_conf():
    with open("./conf.json", "r") as f:
        raw_conf = f.read()
    return loads(raw_conf)

conf = load_conf()

api_server = conf["api_server"]
model = "bert_vits2"

def gen_audio(text: str):
    try:
        print(f"使用 {model} 合成 {text}")
        resp = get(f"{api_server}/gen/{model}/?text={text}")
        return resp.text
    except:
        pass


def play_wav(wav_file_path):
    chunk = 1024
    wf = wave.open(wav_file_path, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()

exit_flag = False
voice_seq = []

def play_background_seq():
    global voice_seq
    global exit_flag
    while not exit_flag:
        if voice_seq:
            current = voice_seq[0]
            voice_seq = voice_seq[1:]
            play_wav(current)
        sleep(0.3)



thread = threading.Thread(target=play_background_seq)
thread.start()


while True:
    print("使用@switch切换模型\n使用@exit安全退出")
    text = input(">")
    if text == "@switch":
        if model == "gpt_sovits":
            model = "bert_vits2"
        else:
            model = "gpt_sovits"
        continue
    elif text == "@exit":
        exit_flag = True
        break
    file_name = gen_audio(text)
    if type(file_name) == str:
        voice_seq.append(f"../unitts/"+file_name.replace('"', ""))

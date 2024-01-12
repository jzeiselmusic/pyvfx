import helper_classes
import numpy as np
from scipy.fft import fft

def is_mono(data: np.ndarray):
    try:
        second_channel = data.shape[1]
        if second_channel == 1:
            return True
        else:
            return False
    except:
        return True

def make_mono(data: np.ndarray):
    try:
        channels = data.shape[1]
    except:
        raise RuntimeError("data must be 2 dimensional with N channels")
    if data.shape[1] == 1:
        return data
    else:
        return np.mean(data, axis=1)

# for any video the audio sampling rate is going to be 
# higher than the frame rate.
# how many audio samples contributes to a single video frame?
def ratio_of_audio_to_frames(sr, fr):
    return int(sr / fr)

def get_stft_for_video(audio_data, sampling_rate, frame_rate):
    if not is_mono(audio_data):
        audio_data = make_mono(audio_data)
    ratio = ratio_of_audio_to_frames(sampling_rate, frame_rate)
    stft = [audio_data[i:i+ratio] for i in range(0, len(audio_data), ratio)]
    stft = [[abs(m) for m in fft(n)] for n in stft]
    stft = [n[0:int(len(n)/2)] for n in stft]
    return np.asarray(stft)

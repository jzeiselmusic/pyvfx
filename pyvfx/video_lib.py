import numpy as np
import cv2
import os
from moviepy.editor import VideoFileClip
import moviepy.editor as mpy
from alive_progress import alive_bar
import scipy.io.wavfile as wavfile
from skimage.exposure import adjust_gamma
from natsort import natsorted


def turn_img_into_np(vid: np.ndarray, crop: bool, width, height):
    result = np.asarray(vid)
    if (crop):
        result = result[:, height[0]:height[1], width[0]:width[1], :]
    return result


def import_video(source_path: str,
                crop:bool = False, 
                new_width:tuple = (50,100), 
                new_height:tuple = (50,100)) -> tuple[np.ndarray, int, int]:
    """ input path to video, receive the video as an ndarray, 
        frame rate, and frame count 

        use this function if you want to work with video data in memory 
    """ 
    vc = cv2.VideoCapture(source_path)
    if not vc.isOpened():
        raise RuntimeError("error opening file from given path")
    frames = []
    frame_rate = int(vc.get(cv2.CAP_PROP_FPS))
    frame_count = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))
    with alive_bar(frame_count, receipt=False) as bar:
        while vc.isOpened():
            ret, frame = vc.read()
            if not ret:
                break
            frames.append(frame)
            bar()

    vc.release()
    with alive_bar(title='Converting to NumPy Array', monitor=False, elapsed=False, receipt=False) as bar:
        total_frames = turn_img_into_np(frames, crop, new_width, new_height)
    return total_frames, frame_rate, frame_count


def import_audio_from_path(source_path: str) -> tuple[np.ndarray, int, int, int]:
    """ input path to video, receive the audio as an ndarray, 
    sample rate, sample count, and number of channels """ 
    try:
        video = VideoFileClip(source_path)
    except:
        raise RuntimeError("error opening video from path")
    audio_object = video.audio
    sample_rate = audio_object.fps
    audio_data = audio_object.to_soundarray()
    if len(audio_data.shape) == 1:
        num_channels = 1
    elif len(audio_data.shape) == 2:
        num_channels = audio_data.shape[1]
    else:
        raise RuntimeError(f"audio has unique shape: {audio_data.shape}")
    sample_count = audio_data.shape[0]
    return audio_data, sample_rate, sample_count, num_channels
    

def save_frames_from_path(destination_path: str, movie_name: str, source_path: str, 
                crop:bool = False, new_width:tuple = (50,100), new_height:tuple = (50,100)):
    """ provide path to save all frames of given video separately in a destination folder

        this function will separate the frames into images and save all frames in this folder

        use this function if you want to work with video on disk instead of in memory
    """
    vc = cv2.VideoCapture(source_path)
    if not vc.isOpened():
        raise RuntimeError("error opening file from given path")
    frame_count = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))
    with alive_bar(frame_count, receipt=False) as bar:
        while vc.isOpened():
            ret, frame = vc.read()
            if not ret:
                break
            if (crop):
                frame = frame[new_height[0]:new_height[1],new_width[0]:new_width[1]]
            cv2.imwrite(destination_path + movie_name + f"_{bar.current}.bmp", frame)
            bar()
    vc.release()


def save_frames_from_array(destination_path: str, movie_name: str, source: np.ndarray,
                crop:bool = False, new_width:tuple = (50,100), new_height:tuple = (50,100)):
    """ provide path to save all frames of given video separately in a destination folder

        this function will separate the frames into images and save all frames in this folder

        use this function if you want to work with video on disk instead of in memory
    """
    frame_count = source.shape[0]
    with alive_bar(frame_count, receipt=False) as bar:
        for frame in source:
            if (crop):
                frame = frame[new_height[0]:new_height[1],new_width[0]:new_width[1]]
            cv2.imwrite(destination_path + movie_name + f"_{bar.current}.bmp", frame)
            bar()


def save_audio_from_path(source_path: str, destination_path: str) -> None:
    """ provide path to save audio of given video (destination path) 
    
        creates .wav file from the video at source_path
    """
    data, sample_rate, _, _ = import_audio_from_path(source_path)
    wavfile.write(destination_path, sample_rate, data)


def create_video_from_frames(source_path: str, destination_path: str, fps: int):
    """ provide a source folder path, function will look in that folder and 
        concatenate all images in the folder into one video clip, saved to 
        destination path provided with frames per second provided.
        files will be concatenated in MacOS finder sort order (natural sort) 
    """
    img_file_exts = ("jpg", "png", "bmp", "JPEG", "jpeg", "svg")
    files = [source_path + n for n in natsorted(
        [m for m in os.listdir(source_path) if m[0] != "." and m[-3:] in img_file_exts])]
    clip = mpy.ImageSequenceClip(files, fps=fps)
    clip.write_videofile(destination_path, codec="libx264")


def create_video_from_array(source: np.ndarray, destination_path: str, fps: int):
    """ provide a source numpy array, function will write a .mp4 file out to 
        destination path.
    """
    width = source.shape[2]
    height = source.shape[1]
    out_vid = cv2.VideoWriter(destination_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    with alive_bar(source.shape[0], receipt=False) as bar:
        for frame in source:
            out_vid.write(frame.astype(np.uint8))
            bar()
    out_vid.release()


def add_audio_to_video(video_path: str, audio_path: str):
    video_clip = mpy.VideoFileClip(video_path)
    audio_clip = mpy.AudioFileClip(audio_path)
    video_clip.audio = audio_clip
    video_clip.write_videofile(video_path, codec='libx264', 
                               audio_codec='aac', 
                               temp_audiofile='temp.m4a', 
                               remove_temp=True)
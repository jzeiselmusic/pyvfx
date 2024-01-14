import effect_lib, video_lib, audio_lib
import subprocess

# first test
audio, sr, _, _ = video_lib.import_audio_from_path("./Lush.MOV")
vid, fr, fc = video_lib.import_video("./Lush.MOV", crop=True, new_width=(200,500), new_height=(300,600))
stft = audio_lib.get_stft_for_video(audio, sr, fr)
n_bins = len(stft[0])
effect_lib.mirrorize_video_from_array(vid, horizontal=False, vertical=True)
# video_lib.create_video_from_array(vid, "./_test1.mp4", fr)

# effect_lib.video_effect_based_on_audio(vid, stft, sr, 200, "laplace", 20)
effect_lib.video_effect_based_on_audio(vid, stft, sr, 90, "saturation", 20)
effect_lib.video_effect_to_whole(vid, "threshold", 100)
effect_lib.video_effect_to_whole(vid, "quantization", 4)
effect_lib.pixelate_video_from_array(vid, 4, randomize=False)

video_lib.save_audio_from_path("./Lush.MOV", "audio.wav")
video_lib.create_video_from_array(vid, "./_test3.mp4", fr)
#video_lib.add_audio_to_video("./_test3.mp4", "./audio.wav")
#print("adding audio back to video")
#subprocess.run(["ffmpeg", "-i", "./_test3.avi", "-i", "./audio.wav", "-c", "copy", "map", "0:v:0", "-map", "1:a:0", "_test3.mp4"])
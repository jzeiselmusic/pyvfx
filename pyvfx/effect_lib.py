import numpy as np
import cv2
from alive_progress import alive_bar
from helper_funcs import map_range, hz_to_bins
from helper_classes import AveragedValue
from skimage.exposure import adjust_gamma
from skimage.filters import laplace

def pixelate_video_from_path(source_path: str, pixel_size: int, randomize:bool=False):
    """ choose a size for NxN pixels, where each square is 
        all the same color, an average of all the pixel colors with
        that square, creating a pixelation effect 
        
        for best results, make pixel_size an exact division of width/height 
        
        if randomize == true, pixel size will be maximum size
    """
    img_file_exts = ("jpg", "png", "bmp", "JPEG", "jpeg", "svg")
    if source_path[-1] != "/": source_path += "/"
    files = [source_path + n for n in natsorted(
        [m for m in os.listdir(source_path) if m[0] != "." and m[-3:] in img_file_exts])]
    with alive_bar(len(files), receipt=False) as bar:
        for file in files:
            if (randomize):
                kernel_size = random.randint(5, pixel_size)
            else:
                kernel_size = pixel_size
            try:
                img = cv2.imread(file)
            except:
                raise RuntimeError(f"could not read file {file}")
            if (horizontal):
                for i in range(0, img.shape[0], kernel_size):
                    for j in range(0, img.shape[1], kernel_size):
                        for k in range(3):
                            img[i:i+kernel_size,j:j+kernel_size,k] = int(img[i:i+kernel_size,j:j+kernel_size,k].sum() \
                                                    / img[i:i+kernel_size,j:j+kernel_size,k].size)
            if (vertical):
                for i in range(0, img.shape[0], kernel_size):
                    for j in range(0, img.shape[1], kernel_size):
                        for k in range(3):
                            img[i:i+kernel_size,j:j+kernel_size,k] = int(img[i:i+kernel_size,j:j+kernel_size,k].sum() \
                                                    / img[i:i+kernel_size,j:j+kernel_size,k].size)

            cv2.imwrite(file, img)
            bar()


def pixelate_video_from_array(source: np.ndarray, pixel_size, randomize:bool=False):
    """ use array in memory instead of disk path.

        choose a size for NxN pixels, where each square is 
        all the same color, an average of all the pixel colors with
        that square, creating a pixelation effect 
        
        for best results, make pixel_size an exact division of width/height 
        
        if randomize == true, pixel size will be maximum size
    """
    with alive_bar(source.shape[0], receipt=False) as bar:
        for img in source:
            if (randomize):
                kernel_size = random.randint(5, pixel_size)
            else:
                kernel_size = pixel_size
            for i in range(0, img.shape[0], kernel_size):
                for j in range(0, img.shape[1], kernel_size):
                    for k in range(3):
                        img[i:i+kernel_size,j:j+kernel_size,k] = int(img[i:i+kernel_size,j:j+kernel_size,k].sum() \
                                                / img[i:i+kernel_size,j:j+kernel_size,k].size)
            bar()


def pixelate_image_from_array(source: np.ndarray, pixel_size):
    for i in range(0, source.shape[0], pixel_size):
        for j in range(0, source.shape[1], pixel_size):
            for k in range(3):
               img[i:i+pixel_size,j:j+pixel_size,k] = int(img[i:i+pixel_size,j:j+pixel_size,k].sum() \
                                                / img[i:i+pixel_size,j:j+pixel_size,k].size) 


def double_video_from_path(source_path: str, horizontal: bool, vertical: bool):
    """ creates a doubling effect. Copies one half to the other half for the video in either horizontal or 
        vertical direction or both. 

        Horizontal means the middle line is horizontal across the center of the video
        Vertical means the same in the vertical direction
    """
    img_file_exts = ("jpg", "png", "bmp", "JPEG", "jpeg", "svg")
    if source_path[-1] != "/": source_path += "/"
    files = [source_path + n for n in natsorted(
        [m for m in os.listdir(source_path) if m[0] != "." and m[-3:] in img_file_exts])]
    with alive_bar(len(files), receipt=False) as bar:
        for file in files:
            try:
                img = cv2.imread(file)
            except:
                raise RuntimeError(f"could not read file {file}")
            if (horizontal):
                img[0:int(img.shape[0]/2), :, :] = img[int(img.shape[0]/2):, :, :]
            if (vertical):
                img[:, 0:int(img.shape[1]/2),:] = img[:, int(img.shape[1]/2):, :]
            cv2.imwrite(file, img)
            bar()


def double_video_from_array(source: np.ndarray, horizontal: bool, vertical: bool):
    """ creates a doubling effect. Copies one half to the other half for the video in either horizontal or 
        vertical direction or both. 

        Horizontal means the middle line is horizontal across the center of the video
        Vertical means the same in the vertical direction
    """
    frame_count = source.shape[0]
    with alive_bar(frame_count, receipt=False) as bar:
        for img in source:
            if (horizontal):
                img[0:int(img.shape[0]/2), :, :] = img[int(img.shape[0]/2):, :, :]
            if (vertical):
                img[:, 0:int(img.shape[1]/2),:] = img[:, int(img.shape[1]/2):, :]
            bar()

def mirrorize_video_from_path(source_path: str, horizontal: bool, vertical: bool):
    """ creates a doubling effect. Copies one half to the other half for the video in either horizontal or 
        vertical direction or both. 

        Horizontal means the middle line is horizontal across the center of the video
        Vertical means the same in the vertical direction
    """
    img_file_exts = ("jpg", "png", "bmp", "JPEG", "jpeg", "svg")
    if source_path[-1] != "/": source_path += "/"
    files = [source_path + n for n in natsorted(
        [m for m in os.listdir(source_path) if m[0] != "." and m[-3:] in img_file_exts])]
    with alive_bar(len(files), receipt=False) as bar:
        for file in files:
            try:
                img = cv2.imread(file)
            except:
                raise RuntimeError(f"could not read file {file}")
            if (horizontal):
                img[0:int(img.shape[0]/2), :, :] = np.flip(img[int(img.shape[0]/2):, :, :], 0)
            if (vertical):
                img[:, 0:int(img.shape[1]/2),:] = np.flip(img[:, int(img.shape[1]/2):, :], 1)
            cv2.imwrite(file, img)
            bar()


def mirrorize_video_from_array(source: np.ndarray, horizontal: bool, vertical: bool):
    """ creates a doubling effect. Copies one half to the other half for the video in either horizontal or 
        vertical direction or both. 

        Horizontal means the middle line is horizontal across the center of the video
        Vertical means the same in the vertical direction
    """
    frame_count = source.shape[0]
    with alive_bar(frame_count, receipt=False) as bar:
        for img in source:
            if (horizontal):
                img[0:int(img.shape[0]/2), :, :] = np.flip(img[int(img.shape[0]/2):, :, :], 0)
            if (vertical):
                img[:, 0:int(img.shape[1]/2),:] = np.flip(img[:, int(img.shape[1]/2):, :], 1)
            bar()


def video_effect_to_whole(video: np.ndarray, type: str, amt):
    if type=="exposure":
        with alive_bar(len(video), receipt=False) as bar:
            for idx, frame in enumerate(video):
                video[idx] = expose_image_from_array(frame, amt)
                bar()
    elif type=="saturation":
        with alive_bar(len(video), receipt=False) as bar:
            for idx, frame in enumerate(video):
                video[idx] = saturate_image_from_array(frame, amt)
                bar()
    elif type=="quantization":
        with alive_bar(len(video), receipt=False) as bar:
            for idx, frame in enumerate(video):
                video[idx] = quantize_image_from_array(frame, amt)
                bar()
    elif type=="laplace":
        with alive_bar(len(video), receipt=False) as bar:
            for idx, frame in enumerate(video):
                video[idx] = laplace_image_from_array(frame, amt)
                bar()
    elif type=="threshold":
        with alive_bar(len(video), receipt=False) as bar:
            for idx, frame in enumerate(video):
                video[idx] = threshold_image_from_array(frame, amt)
                bar()
    return video


def video_effect_based_on_audio(video: np.ndarray, 
                                stft: np.ndarray,
                                sample_rate: float,
                                frequency: float, 
                                type: str,
                                avging: int):
    _bin = hz_to_bins(frequency, sample_rate, len(stft[0]))
    max_at_bin = max([n[_bin] for n in stft])
    min_at_bin = min([n[_bin] for n in stft])
    sample = AveragedValue(avging)
    if type=="exposure":
        with alive_bar(len(video), receipt=False) as bar:
            for idx, frame in enumerate(video):
                gamma = 1.0 - map_range(sample.append(stft[idx][_bin]), min_at_bin, max_at_bin, 0.0, 0.5)
                gamma *= 0.9
                video[idx] = expose_image_from_array(frame, gamma)
                bar()
    elif type=="saturation":
        with alive_bar(len(video), receipt=False) as bar:
            for idx, frame in enumerate(video):
                amt = map_range(sample.append(stft[idx][_bin]), min_at_bin, max_at_bin / 2.0, 0.9, 3.0)
                video[idx] = saturate_image_from_array(frame, amt)
                bar()
    elif type=="quantization":
        with alive_bar(len(video), receipt=False) as bar:
            for idx, frame in enumerate(video):
                amt = int(map_range(sample.append(stft[idx][_bin]), min_at_bin, max_at_bin/2.0, 1, 5))
                video[idx] = quantize_image_from_array(frame, amt)
                bar()
    elif type=="laplace":
        with alive_bar(len(video), receipt=False) as bar:
            for idx, frame in enumerate(video):
                amt = map_range(sample.append(stft[idx][_bin]), min_at_bin, max_at_bin / 3.0, 0.1, 0.9)
                video[idx] = laplace_image_from_array(frame, amt)
                bar()
    elif type=="threshold":
        with alive_bar(len(video), receipt=False) as bar:
            for idx, frame in enumerate(video):
                amt = map_range(sample.append(stft[idx][_bin]), min_at_bin, max_at_bin / 2.0, 20, 200)
                video[idx] = threshold_image_from_array(frame, amt)
                bar()
    return video


def rotate_video(vid: np.ndarray, n_times: int):
    l = [np.rot90(n, k = n_times) for n in vid]
    vid = np.asarray(l)
    return vid


## image based effects ## 


def saturate_image_from_array(img: np.ndarray, amt: float):
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_image)
    s = s.astype(float)
    s *= amt
    s = s.astype(np.uint8) # may result in overflow
    hsv_image = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)


def expose_image_from_array(img: np.ndarray, gamma: float):
    return adjust_gamma(img, gamma)


def quantize_image_from_array(img: np.ndarray, amt: int):
    return img & (0xFFFE << amt)


def laplace_image_from_arrays(img: np.ndarray, amt: float):
    # amt should be between 0 and 1. percentage of the image that 
    # is the frangi, vs the percentage that is the OG image
    return 3.0*amt*laplace(img) + (1.0-(amt/3.0))*img


def threshold_image_from_array(img: np.ndarray, thresh: int):
    mask = img < thresh
    img[mask] = 0
    return img
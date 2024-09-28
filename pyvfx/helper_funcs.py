import imageio.v3 as imageio
import numpy as np
import cv2
import os

def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def hz_to_bins(freq: float, sr: float, bins: int):
    """
    get the bin that corresponds to the input frequency
    given: the total bins and sampling rate
    """
    return int(bins * freq / (sr/2))

def save_as_jpeg(image: np.ndarray, path: str, amt: int):
    """
    Saves a numpy ndarray as a JPEG (.jpg) image.
    """
    # Ensure the file name has the correct extension
    if not path.lower().endswith('.jpg'):
        path += '.jpg'
    cv2.imwrite(path, image, [cv2.IMWRITE_JPEG_QUALITY, amt, cv2.IMWRITE_JPEG_SAMPLING_FACTOR, cv2.IMWRITE_JPEG_SAMPLING_FACTOR_444])

def save_as_jp2(image: np.ndarray, path: str, amt: int):
    """
    Saves a numpy ndarray as a JPEG2000 (.jp2) image.
    """
    # Ensure the file name has the correct extension
    if not path.lower().endswith('.jp2'):
        path += '.jp2'
    cv2.imwrite(path, image, [cv2.IMWRITE_JPEG2000_COMPRESSION_X1000, amt])

def import_img_from_path(path: str):
    image_array = cv2.imread(path)
    return image_array
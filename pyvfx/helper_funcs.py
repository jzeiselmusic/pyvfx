def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# get the bin that corresponds to the input frequency
# given: the total bins and sampling rate
def hz_to_bins(freq: float, sr: float, bins: int):
    return int(bins * freq / (sr/2))

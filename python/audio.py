import numpy as np
import sounddevice as sd
from config import DEVICE, SAMPLERATE, LED_COUNT

BLOCK_SIZE = 1024  # larger = more frequency precision, but higher latency
SMOOTHING = 0.0

prev_fft = np.zeros(LED_COUNT)


def frequencies_to_colors(fft_data):
    colors = []

    for i, freq_bin in enumerate(fft_data):
        amplitude = min(1.0, freq_bin)

        # color gradient: bass=red, mid=green, highs=blue
        t = i / LED_COUNT  # 0.0 ... 1.0
        if t < 0.5:
            r = int(255 * (1 - t * 2) * amplitude)
            g = int(255 * (t * 2) * amplitude)
            b = 0
        else:
            r = 0
            g = int(255 * (1 - (t - 0.5) * 2) * amplitude)
            b = int(255 * ((t - 0.5) * 2) * amplitude)

        colors.append((r, g, b))

    return colors


def start(callback):
    def _callback(indata, frames, time_info, status):
        global prev_fft

        mono = indata[:, 0]
        fft = np.abs(np.fft.rfft(mono))
        fft = np.log1p(fft * 10)  # log scale to balance bass and highs

        # resample to LED_COUNT bins using log scale indices
        fft_len = len(fft)
        indices = np.logspace(0, np.log10(fft_len - 1), LED_COUNT).astype(int)
        fft_resampled = fft[indices]

        # normalize to 0.0 - 1.0
        max_val = np.max(fft_resampled)
        if max_val > 0:
            fft_resampled = fft_resampled / max_val

        # smoothing: blend with previous frame
        fft_resampled = SMOOTHING * prev_fft + (1 - SMOOTHING) * fft_resampled
        prev_fft = fft_resampled

        callback(frequencies_to_colors(fft_resampled))

    return sd.InputStream(
        device=DEVICE,
        channels=2,
        samplerate=SAMPLERATE,
        blocksize=BLOCK_SIZE,
        callback=_callback,
    )

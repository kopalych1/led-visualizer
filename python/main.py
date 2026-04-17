import time
import serial
from serial_sender import send_colors
from audio import start
from config import PORT, BAUDRATE

ser = serial.Serial(PORT, BAUDRATE, timeout=1)
time.sleep(2)  # wait for arduino to reset after opening the serial port


def on_colors(colors):
    send_colors(ser, colors)


def main():
    with start(on_colors):
        input("Press Enter to stop\n")


if __name__ == "__main__":
    main()

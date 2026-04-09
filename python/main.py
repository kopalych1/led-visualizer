import time
import serial
from serial_sender import send_colors

PORT = "COM5"
BAUDRATE = 500000
LED_COUNT = 150

ser = serial.Serial(PORT, BAUDRATE, timeout=1)
time.sleep(2)  # Wait for arduino to reset after opening the serial port

colors = [(255, 0, 0)] * 50 + [(0, 255, 0)] * 50 + [(0, 0, 255)] * 50

while True:
    send_colors(ser, colors)
    time.sleep(0.05)

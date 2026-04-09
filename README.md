# LED Visualizer

LED strip control via Serial with Arduino.

## Hardware
- Arduino (LED_PIN = 9)
- Addressable LED strip, 150 LEDs

## Protocol
Binary packet over Serial (500000 baud):
```
[0xAB][0xCD]  start marker (2 bytes)
[count]       number of LEDs (1 byte)
[R][G][B]     color of each LED (3 bytes × count)
[XOR][0xFF]   checksum + end marker (2 bytes)
```

## Running

### Arduino
Open `arduino/led_visualizer/led_visualizer.ino` in Arduino IDE and upload to the board.

### Python
```bash
pip install pyserial
cd python
python main.py
```

## Structure
```
arduino/
  led_visualizer/
    led_visualizer.ino
python/
  main.py          — entry point
  serial_sender.py — send packets to Arduino
  audio.py         — audio capture (in development)
```

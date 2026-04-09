import serial


# Packet structure:
# [0xAB][0xCD] — marker (2 bytes)
# [count]      — number of LEDs (1 byte)
# [R][G][B]    — color of each (3 bytes × count)
# [XOR][0xFF]  — checksum + final marker (2 bytes)
def send_colors(ser: serial.Serial, rgb_list: list[tuple[int, int, int]]):
    count = len(rgb_list)

    payload: list[int] = []
    xor_sum = 0
    for r, g, b in rgb_list:
        payload += [r, g, b]
        xor_sum ^= r ^ g ^ b

    packet = (
        bytes([0xAB, 0xCD]) + bytes([count]) + bytes(payload) + bytes([xor_sum, 0xFF])
    )

    ser.write(packet)
    ser.flush()

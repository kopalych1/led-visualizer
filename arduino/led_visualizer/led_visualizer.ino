#include <Adafruit_NeoPixel.h>

#define LED_PIN 9
#define LED_COUNT 150

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

uint8_t r[LED_COUNT], g[LED_COUNT], b[LED_COUNT];

// Waits until at least `count` bytes are available in the serial buffer or timeout occurs.
bool waitBytes(int count, int timeout_ms = 500) {
  unsigned long t = millis();
  while (Serial.available() < count) {
    if (millis() - t > timeout_ms) return false;
  }
  return true;
}

// Packet structure:
// [0xAB][0xCD] — marker (2 bytes)
// [count]      — number of LEDs (1 byte)
// [R][G][B]    — color of each (3 bytes x count)
// [XOR][0xFF]  — checksum + final marker (2 bytes)
bool readPacket() {
  static uint8_t prev = 0;

  // Look for the marker in the serial stream
  while (Serial.available()) {
    uint8_t curr = Serial.read();
    if (prev == 0xAB && curr == 0xCD) {
      prev = 0;
      goto marker_found;
    }
    prev = curr;
  }
  return false;

marker_found:
  if (!waitBytes(1)) return false;
  uint8_t count = Serial.read();
  if (count != LED_COUNT) return false;

  uint8_t xorSum = 0;
  for (int i = 0; i < count; i++) {
    if (!waitBytes(3)) return false;
    r[i] = Serial.read();
    g[i] = Serial.read();
    b[i] = Serial.read();
    xorSum ^= r[i] ^ g[i] ^ b[i];
  }

  if (!waitBytes(2)) return false;
  uint8_t receivedXor = Serial.read();
  uint8_t endMarker = Serial.read();

  if (endMarker != 0xFF) return false;
  if (xorSum != receivedXor) return false;

  return true;
}

void setup() {
  Serial.begin(500000);

  strip.begin();
  strip.fill(0);
  strip.setBrightness(30);
  strip.show();
}

void loop() {
  if (readPacket()) {
    for (int i = 0; i < LED_COUNT; i++) {
      strip.setPixelColor(i, strip.Color(r[i], g[i], b[i]));
    }
    strip.show();
  }
}

import wiringpi as wp
import time
import subprocess

# Constants
BUTTON_PIN = 17
LED_PIN = 27
DEBOUNCE_TIME = 0.2  # 200 ms debounce time

# Setup
wp.wiringPiSetupGpio()
wp.pinMode(BUTTON_PIN, wp.INPUT)
wp.pullUpDnControl(BUTTON_PIN, wp.PUD_UP)
wp.pinMode(LED_PIN, wp.OUTPUT)
wp.digitalWrite(LED_PIN, wp.LOW)

def button_pressed():
    return wp.digitalRead(BUTTON_PIN) == wp.LOW

def main():
    while True:
        if button_pressed():
            wp.digitalWrite(LED_PIN, wp.HIGH)
            subprocess.run(["python3", "print_daemon.py"])
            wp.digitalWrite(LED_PIN, wp.LOW)
            time.sleep(DEBOUNCE_TIME)
        time.sleep(0.01)  # Polling delay

if __name__ == "__main__":
    main()
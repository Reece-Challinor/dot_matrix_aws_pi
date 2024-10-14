import wiringpi as wp
import time
import subprocess
import logging

# Constants
BUTTON_PIN = 17
LED_PIN = 27
DEBOUNCE_TIME = 0.2  # 200 ms debounce time

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup
try:
    wp.wiringPiSetupGpio()
    wp.pinMode(BUTTON_PIN, wp.INPUT)
    wp.pullUpDnControl(BUTTON_PIN, wp.PUD_UP)
    wp.pinMode(LED_PIN, wp.OUTPUT)
    wp.digitalWrite(LED_PIN, wp.LOW)
    logging.info("GPIO setup completed successfully.")
except Exception as e:
    logging.error(f"Error during GPIO setup: {e}")
    raise

def button_pressed():
    """Check if the button is pressed."""
    return wp.digitalRead(BUTTON_PIN) == wp.LOW

def main():
    """Main loop to monitor button press and trigger actions."""
    try:
        while True:
            if button_pressed():
                logging.info("Button pressed.")
                wp.digitalWrite(LED_PIN, wp.HIGH)
                try:
                    subprocess.run(["python3", "print_daemon.py"], check=True)
                    logging.info("Print daemon triggered successfully.")
                except subprocess.CalledProcessError as e:
                    logging.error(f"Error triggering print daemon: {e}")
                wp.digitalWrite(LED_PIN, wp.LOW)
                time.sleep(DEBOUNCE_TIME)
            time.sleep(0.01)  # Polling delay
    except KeyboardInterrupt:
        logging.info("Program terminated by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        wp.digitalWrite(LED_PIN, wp.LOW)
        logging.info("Cleaned up GPIO settings.")

if __name__ == "__main__":
    main()
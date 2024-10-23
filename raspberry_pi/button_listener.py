import wiringpi as wp
import time
import subprocess
import logging
import queue
import threading
import os
from pathlib import Path
from typing import Optional

class ButtonController:
    """Controls button interaction and print daemon management."""
    
    def __init__(self, button_pin: int = 17, led_pin: int = 27):
        # Pin Configuration
        self.BUTTON_PIN = button_pin
        self.LED_PIN = led_pin
        self.DEBOUNCE_TIME = 0.2  # 200ms debounce
        
        # Queue for print jobs
        self.print_queue = queue.Queue()
        
        # Status tracking
        self.daemon_running = False
        self.is_processing = False
        
        # Setup logging
        self._setup_logging()
        
        # Initialize GPIO
        self._setup_gpio()
        
        # Start worker thread
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()
    
    def _setup_logging(self):
        """Configure logging with rotation."""
        log_dir = Path('/var/log/button_controller')
        log_dir.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger('ButtonController')
        self.logger.setLevel(logging.DEBUG)
        
        # File handler with rotation
        handler = logging.handlers.RotatingFileHandler(
            log_dir / 'button_controller.log',
            maxBytes=1024*1024,  # 1MB
            backupCount=5
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def _setup_gpio(self):
        """Initialize GPIO pins with error handling."""
        try:
            wp.wiringPiSetupGpio()
            
            # Configure button pin
            wp.pinMode(self.BUTTON_PIN, wp.INPUT)
            wp.pullUpDnControl(self.BUTTON_PIN, wp.PUD_UP)
            
            # Configure LED pin
            wp.pinMode(self.LED_PIN, wp.OUTPUT)
            wp.digitalWrite(self.LED_PIN, wp.LOW)
            
            self.logger.info("GPIO setup completed successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize GPIO: {e}")
            raise
    
    def _button_pressed(self) -> bool:
        """Check if button is pressed with debouncing."""
        if wp.digitalRead(self.BUTTON_PIN) == wp.LOW:
            time.sleep(self.DEBOUNCE_TIME)  # Debounce wait
            return wp.digitalRead(self.BUTTON_PIN) == wp.LOW
        return False
    
    def _blink_led(self, times: int = 3, interval: float = 0.2):
        """Blink LED to indicate status."""
        for _ in range(times):
            wp.digitalWrite(self.LED_PIN, wp.HIGH)
            time.sleep(interval)
            wp.digitalWrite(self.LED_PIN, wp.LOW)
            time.sleep(interval)
    
    def _check_daemon_script(self) -> bool:
        """Verify print daemon script exists and is executable."""
        daemon_path = Path('./print_daemon.py')
        if not daemon_path.exists():
            self.logger.error("print_daemon.py not found")
            return False
        if not os.access(daemon_path, os.X_OK):
            self.logger.error("print_daemon.py not executable")
            return False
        return True
    
    def _start_print_daemon(self) -> Optional[subprocess.Popen]:
        """Start the print daemon process."""
        if not self._check_daemon_script():
            return None
        
        try:
            process = subprocess.Popen(
                ["python3", "print_daemon.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.daemon_running = True
            self.logger.info("Print daemon started successfully")
            return process
        except subprocess.SubprocessError as e:
            self.logger.error(f"Failed to start print daemon: {e}")
            return None
    
    def _process_queue(self):
        """Process the print queue in a separate thread."""
        while True:
            try:
                # Wait for queue item
                _ = self.print_queue.get()
                self.is_processing = True
                wp.digitalWrite(self.LED_PIN, wp.HIGH)
                
                # Start daemon if not running
                if not self.daemon_running:
                    daemon_process = self._start_print_daemon()
                    if daemon_process:
                        # Wait for daemon to initialize
                        time.sleep(2)
                        
                        # Check if process is still running
                        if daemon_process.poll() is None:
                            self._blink_led(2, 0.5)  # Success indication
                        else:
                            stdout, stderr = daemon_process.communicate()
                            self.logger.error(f"Daemon failed to start: {stderr.decode()}")
                            self._blink_led(5, 0.1)  # Error indication
                    
                self.is_processing = False
                wp.digitalWrite(self.LED_PIN, wp.LOW)
                self.print_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"Error in queue processing: {e}")
                self.is_processing = False
                wp.digitalWrite(self.LED_PIN, wp.LOW)
                self._blink_led(5, 0.1)  # Error indication
    
    def run(self):
        """Main loop to monitor button presses."""
        self.logger.info("Button controller started")
        
        try:
            while True:
                if self._button_pressed() and not self.is_processing:
                    self.logger.info("Button pressed - queueing print job")
                    self.print_queue.put(1)
                    
                time.sleep(0.01)  # Prevent CPU hogging
                
        except KeyboardInterrupt:
            self.logger.info("Button controller stopped by user")
        except Exception as e:
            self.logger.error(f"Unexpected error in main loop: {e}")
        finally:
            # Cleanup
            wp.digitalWrite(self.LED_PIN, wp.LOW)
            self.daemon_running = False
            self.logger.info("Button controller shutdown complete")

if __name__ == "__main__":
    controller = ButtonController()
    controller.run()
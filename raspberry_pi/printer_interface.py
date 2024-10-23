import cups
import logging
import time
import queue
import threading
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/printer_interface.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('printer_interface')

class PrinterError(Exception):
    """Custom exception for printer-related errors"""
    pass

class DotMatrixPrinter:
    """Handles communication with dot matrix printer via CUPS"""
    
    def __init__(self, printer_name: str = "KX-P1592"):
        self.printer_name = printer_name
        self.print_queue = queue.Queue()
        self.retry_count = 3
        self.retry_delay = 5  # seconds
        self.temp_dir = Path("/tmp/print_jobs")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Connect to CUPS
        try:
            self.conn = cups.Connection()
            self._verify_printer()
        except Exception as e:
            logger.error(f"Failed to initialize CUPS connection: {e}")
            raise PrinterError("CUPS initialization failed")
        
        # Start print queue worker
        self.worker_thread = threading.Thread(target=self._process_print_queue, daemon=True)
        self.worker_thread.start()

    def _verify_printer(self):
        """Verify printer exists and is ready"""
        printers = self.conn.getPrinters()
        if self.printer_name not in printers:
            raise PrinterError(f"Printer {self.printer_name} not found")
        
        printer_info = printers[self.printer_name]
        if printer_info['printer-state'] == 5:  # 5 = stopped
            raise PrinterError(f"Printer {self.printer_name} is stopped")

    def get_printer_status(self) -> Dict[str, Any]:
        """Get current printer status and attributes"""
        try:
            printers = self.conn.getPrinters()
            if self.printer_name not in printers:
                raise PrinterError(f"Printer {self.printer_name} not found")
            
            printer = printers[self.printer_name]
            status = {
                'state': printer['printer-state'],
                'state_message': printer['printer-state-message'],
                'is_accepting': printer['printer-is-accepting-jobs'],
                'state_reasons': printer.get('printer-state-reasons', [])
            }
            return status
        except Exception as e:
            logger.error(f"Failed to get printer status: {e}")
            raise PrinterError("Could not retrieve printer status")

    def format_text_for_printer(self, text: str) -> str:
        """Format text for dot matrix printer"""
        # Add printer control codes and formatting
        formatted = "\x1B@"  # Initialize printer
        formatted += "\x1B3\x18"  # Set line spacing to 24/216"
        
        # Add headers and footers
        header = "=" * 80 + "\n"
        header += f"Printed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += "=" * 80 + "\n\n"
        
        footer = "\n" + "=" * 80 + "\n"
        footer += "End of Document\n"
        footer += "\f"  # Form feed
        
        return formatted + header + text + footer

    def prepare_print_job(self, content: str, job_name: Optional[str] = None) -> Path:
        """Prepare content for printing and save to temporary file"""
        if not job_name:
            job_name = f"print_job_{int(time.time())}"
        
        # Format content for dot matrix printer
        formatted_content = self.format_text_for_printer(content)
        
        # Save to temporary file
        temp_file = self.temp_dir / f"{job_name}.txt"
        temp_file.write_text(formatted_content)
        
        return temp_file

    def submit_print_job(self, content: str, job_name: Optional[str] = None) -> int:
        """Submit a new print job to the queue"""
        try:
            # Prepare print job
            temp_file = self.prepare_print_job(content, job_name)
            
            # Add to print queue
            self.print_queue.put((temp_file, job_name))
            
            logger.info(f"Print job {job_name} queued successfully")
            return self.print_queue.qsize()
            
        except Exception as e:
            logger.error(f"Failed to submit print job: {e}")
            raise PrinterError("Failed to submit print job")

    def _process_print_queue(self):
        """Process print queue in background thread"""
        while True:
            try:
                # Get next job from queue
                temp_file, job_name = self.print_queue.get()
                
                # Process job with retries
                success = False
                for attempt in range(self.retry_count):
                    try:
                        # Verify printer status
                        status = self.get_printer_status()
                        if status['state'] == 5:  # printer stopped
                            raise PrinterError("Printer is stopped")
                        
                        # Submit job to CUPS
                        job_id = self.conn.printFile(
                            self.printer_name,
                            str(temp_file),
                            job_name or "Intelligence Brief",
                            {
                                "raw": "true",  # Send raw text
                                "job-priority": "50",
                                "cpi": "10",  # Characters per inch
                                "lpi": "6"    # Lines per inch
                            }
                        )
                        
                        logger.info(f"Print job {job_name} (ID: {job_id}) submitted to printer")
                        success = True
                        break
                        
                    except Exception as e:
                        logger.warning(f"Print attempt {attempt + 1} failed: {e}")
                        if attempt < self.retry_count - 1:
                            time.sleep(self.retry_delay)
                
                if not success:
                    logger.error(f"Failed to print job {job_name} after {self.retry_count} attempts")
                
                # Cleanup
                if temp_file.exists():
                    temp_file.unlink()
                
                self.print_queue.task_done()
                
            except Exception as e:
                logger.error(f"Error in print queue processing: {e}")
                continue

    def cancel_all_jobs(self):
        """Cancel all pending print jobs"""
        try:
            jobs = self.conn.getJobs(which_jobs='not-completed')
            for job_id in jobs:
                self.conn.cancelJob(job_id)
            logger.info("All print jobs cancelled")
        except Exception as e:
            logger.error(f"Failed to cancel jobs: {e}")
            raise PrinterError("Failed to cancel print jobs")

    def retry_failed_jobs(self):
        """Retry all failed print jobs"""
        try:
            jobs = self.conn.getJobs()
            retried = 0
            
            for job_id, job in jobs.items():
                if job['job-state'] == 8:  # aborted
                    try:
                        self.conn.cancelJob(job_id)
                        new_id = self.conn.printFile(
                            self.printer_name,
                            job['job-originating-user-name'],
                            job['job-name'],
                            job['job-attributes-tag']
                        )
                        logger.info(f"Retried job {job_id} as {new_id}")
                        retried += 1
                    except Exception as e:
                        logger.error(f"Failed to retry job {job_id}: {e}")
            
            return retried
        except Exception as e:
            logger.error(f"Failed to retry jobs: {e}")
            raise PrinterError("Failed to retry print jobs")

if __name__ == "__main__":
    # Example usage
    try:
        printer = DotMatrixPrinter()
        
        # Print test page
        test_content = """
        TEST PAGE
        ---------
        This is a test of the dot matrix printer interface.
        Testing formatting and printer control.
        
        1234567890
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        abcdefghijklmnopqrstuvwxyz
        
        Special characters: !@#$%^&*()
        """
        
        printer.submit_print_job(test_content, "test_page")
        
        # Wait for queue to empty
        printer.print_queue.join()
        
    except PrinterError as e:
        logger.error(f"Printer error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Printer interface stopped by user")
        sys.exit(0)
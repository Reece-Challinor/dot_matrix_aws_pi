#!/usr/bin/env python3
"""
Test script for the dot matrix printer setup
This script tests:
1. Basic printer connectivity via CUPS
2. Formatting of a test briefing
3. Print submission
"""
import logging
import sys
from pathlib import Path
import subprocess
import time
import json
from datetime import datetime
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('printer_test')

def check_printer_setup():
    """Check if the printer is configured in CUPS"""
    logger.info("Checking printer configuration...")
    try:
        result = subprocess.run(['lpstat', '-p', config.PRINTER_NAME], 
                               capture_output=True, text=True)
        
        if config.PRINTER_NAME in result.stdout:
            logger.info(f"✓ Printer '{config.PRINTER_NAME}' is configured")
            return True
        else:
            logger.error(f"✗ Printer '{config.PRINTER_NAME}' not found in CUPS")
            logger.info("Available printers:")
            printers = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
            logger.info(printers.stdout)
            return False
    except Exception as e:
        logger.error(f"Error checking printer: {e}")
        return False

def generate_test_briefing():
    """Generate a sample briefing for testing"""
    logger.info("Generating test briefing content...")
    
    # Create test data
    test_data = {
        "location": "Test Location",
        "classification": "TEST DOCUMENT",
        "sentiment": "Positive",
        "weather_impact": "Clear skies, no impact",
        "security_level": "Low",
        "market_data": {
            "dow_value": "38,650.32",
            "dow_change": "+0.76%",
            "sp_value": "5,123.41",
            "sp_change": "+0.55%",
            "nasdaq_value": "16,302.48",
            "nasdaq_change": "+1.03%",
            "gold_price": "2,311.20",
            "gold_trend": "72",
            "gold_direction": "↑",
            "oil_price": "82.45",
            "oil_trend": "55",
            "oil_direction": "↓"
        },
        "supply_chain": [
            "No major disruptions reported",
            "Shipping rates stable across major routes",
            "Warehouse capacity at 85%"
        ],
        "headlines": [
            "Test Headline 1 - This is a test",
            "Test Headline 2 - Testing printer capabilities",
            "Test Headline 3 - Dot matrix printing in progress"
        ],
        "recommendations": [
            "This is a test document only",
            "No action required"
        ]
    }
    
    # Import the formatter
    try:
        from data_aggregator import BriefingFormatter
        formatter = BriefingFormatter()
        formatted_briefing = formatter.format_briefing(test_data)
        logger.info("✓ Successfully formatted test briefing")
        return formatted_briefing
    except Exception as e:
        logger.error(f"Error formatting briefing: {e}")
        # Fallback to simple text if formatter fails
        return "TEST BRIEFING\n==============\n\nThis is a test of the printer system."

def test_print_submission(content):
    """Test submitting a print job"""
    logger.info("Testing print submission...")
    
    try:
        # Save content to temp file
        temp_file = config.TEMP_DIR / f"test_print_{int(time.time())}.txt"
        temp_file.write_text(content)
        
        # Submit to printer
        print_cmd = [
            'lp', 
            '-d', config.PRINTER_NAME,
            '-o', 'raw',
            '-o', 'cpi=10',
            '-o', 'lpi=6',
            str(temp_file)
        ]
        
        result = subprocess.run(print_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            job_id = result.stdout.strip()
            logger.info(f"✓ Print job submitted successfully: {job_id}")
            return True
        else:
            logger.error(f"✗ Failed to submit print job: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Error submitting print job: {e}")
        return False

def main():
    """Run all printer tests"""
    logger.info("=== STARTING DOT MATRIX PRINTER TESTS ===")
    
    # Test 1: Check printer configuration
    if not check_printer_setup():
        logger.error("Printer setup test failed. Cannot continue.")
        return False
        
    # Test 2: Generate test briefing
    test_content = generate_test_briefing()
    if not test_content:
        logger.error("Briefing generation test failed. Cannot continue.")
        return False
    
    # Test 3: Test print submission
    print_success = test_print_submission(test_content)
    
    if print_success:
        logger.info("=== ALL TESTS COMPLETED SUCCESSFULLY ===")
        return True
    else:
        logger.error("=== TEST FAILED: Print submission error ===")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
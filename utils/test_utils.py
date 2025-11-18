import time
import random
import string
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class TestUtils:
    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test_{random_string}@example.com"
    
    @staticmethod
    def generate_random_password(length=12):
        characters = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choices(characters, k=length))
    
    @staticmethod
    def calculate_sl_tp_prices(current_price, order_type, sl_points, tp_points):
        """Calculate stop loss and take profit prices based on points"""
        pip_value = 0.0001  # For most forex pairs
        
        if order_type.lower() == 'buy':
            sl_price = current_price - (sl_points * pip_value)
            tp_price = current_price + (tp_points * pip_value)
        else:  # sell
            sl_price = current_price + (sl_points * pip_value)
            tp_price = current_price - (tp_points * pip_value)
        
        return round(sl_price, 5), round(tp_price, 5)
    
    @staticmethod
    def get_future_date(days=1):
        """Get future date for expiry testing"""
        future_date = datetime.now() + timedelta(days=days)
        return future_date.strftime("%Y-%m-%d")
    
    @staticmethod
    def wait_for_condition(condition_func, timeout=30, poll_interval=1):
        """Wait for a condition to be true"""
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                if condition_func():
                    return True
            except Exception as e:
                logger.debug(f"Condition check failed: {str(e)}")
            time.sleep(poll_interval)
        return False
    
    @staticmethod
    def compare_values(expected, actual, tolerance=0.0001):
        """Compare two numeric values with tolerance"""
        try:
            exp_val = float(expected)
            act_val = float(actual)
            return abs(exp_val - act_val) <= tolerance
        except (ValueError, TypeError):
            return expected == actual
    
    @staticmethod
    def extract_order_details_from_notification(notification_text):
        """Parse notification text to extract order details"""
        details = {}
        # Implement parsing logic based on actual notification format
        return details
    
    @staticmethod
    def format_volume(volume):
        """Format volume to standard trading format"""
        return f"{float(volume):.2f}"
    
    @staticmethod
    def validate_price_format(price):
        """Validate if price is in correct format"""
        try:
            float_price = float(price)
            return True
        except ValueError:
            return False
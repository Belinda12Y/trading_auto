import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys

class TradePage(BasePage):
        NOTIFICATION = (By.CSS_SELECTOR, "[data-testid='notification-box-description']")
        #region Order Creation
        BUY_BUTTON = (By.CSS_SELECTOR, "[data-testid='trade-button-order']")
        LAST_PRICE = (By.CSS_SELECTOR, "[data-testid='trade-live-buy-price']")
        STOP_LOSS_INPUT = (By.CSS_SELECTOR, "[data-testid='trade-input-stoploss-price']")
        TAKE_PROFIT_INPUT = (By.CSS_SELECTOR, "[data-testid='trade-input-takeprofit-price']")
        VOLUME_INPUT = (By.CSS_SELECTOR, "[data-testid='trade-input-volume']")
        CONFIRM_BUTTON = (By.CSS_SELECTOR, "[data-testid='trade-confirmation-button-confirm']")
        ORDER_TYPE_DROPDOWN = (By.CSS_SELECTOR, "[data-testid='trade-dropdown-order-type']")
        ORDER_TYPE_OPTIONS = (By.XPATH, "//*[@id=\"root\"]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[2]")
        PRICE_INPUT = (By.XPATH, "//*[@id=\"root\"]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[2]/div[5]/div/div[2]/div/input")
        EXPIRY_DROPDOWN = (By.CSS_SELECTOR, "[data-testid='trade-dropdown-expiry']")
        EXPIRY_OPTIONS = (By.XPATH, "//*[@id=\"root\"]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[2]/div[8]/div/div[2]/div[2]")
        #endregion
        #region Open Listing
        OPEN_LIST_TABLE = (By.XPATH, "//*[@id=\"root\"]/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[2]")
        OPEN_RECORD = (By.CSS_SELECTOR, "[data-testid='asset-open-list-item']")
        EDIT_BUTTON = (By.CSS_SELECTOR, "[data-testid='asset-open-button-edit']")
        CLOSE_BUTTON = (By.CSS_SELECTOR, "[data-testid='asset-open-button-close']")
        OPEN_SL_PRICE = (By.CSS_SELECTOR, "[data-testid='trade-input-stoploss-price']")
        UPDATE_BUTTON = (By.CSS_SELECTOR, "[data-testid='edit-button-order']")
        OPEN_VOLUME = (By.XPATH, "//*[@id=\"overlay-aqx-trader\"]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/input")
        CLOSE_CONFIRM_BUTTON = (By.XPATH, "//*[@id=\"overlay-aqx-trader\"]/div/div[3]/div/div/button[2]")
        EDIT_MODAL = (By.CSS_SELECTOR, "[data-testid='edit-confirmation-modal']")
        EDIT_CONFIRM_BUTTON = (By.CSS_SELECTOR, "[data-testid='trade-confirmation-button-confirm']")
        EDIT_CONFIRMATION_MODAL = (By.XPATH, "//*[@id=\"overlay-aqx-trader\"]/div")
        PENDING_TAB = (By.CSS_SELECTOR, "[data-testid='tab-asset-order-type-pending-orders']")
        PENDING_RECORD = (By.CSS_SELECTOR, "[data-testid='asset-pending-list-item']")
        PENDING_PRICE = (By.XPATH, "//*[@id=\"overlay-aqx-trader\"]/div/div[2]/div[2]/div[2]/div/div[2]/div/input")
        PENDING_UPDATE_BUTTON = (By.XPATH, "//*[@id=\"overlay-aqx-trader\"]/div/div[3]/div/div/button[2]")
        #endregion

        # region Order History
        HISTORY_TAB = (By.CSS_SELECTOR, "[data-testid='tab-asset-order-type-history']")
        HISTORY_RECORD = (By.CSS_SELECTOR, "[data-testid='asset-history-position-list-item']")
        ENTRY_PRICE = (By.CSS_SELECTOR, "[data-testid='asset-history-column-entry-price']")
        ORDER_TYPE = (By.CSS_SELECTOR, "[data-testid='asset-history-column-order-type']")
        VOLUME = (By.CSS_SELECTOR, "[data-testid='asset-history-column-volume']")
        # endregion

        def __init__(self, driver):
            super().__init__(driver)
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(self.VOLUME_INPUT)
            )

        def wait_for_valid_price(self, timeout=10):
            wait = WebDriverWait(self.driver, timeout)

            def price_is_valid(driver):
                try:
                    text = driver.find_element(*self.LAST_PRICE).text.strip()
                    clean = (
                        text.replace("$","")
                            .replace(",","")
                            .replace("+","")
                            .replace("-","")
                            .strip()
                    )
                    float(clean)
                    return clean
                except:
                    return False

            return wait.until(price_is_valid)
        
        def set_value_with_retry(self, locator, value, retries=3):
            for _ in range(retries):
                self.clear(locator)
                self.send_keys(locator, Keys.BACKSPACE * 10)
                self.send_keys(locator, str(value))

                entered = self.get_attribute(locator, "value")
                if entered == str(value):
                    return True

                time.sleep(0.5)

            raise Exception(f"Failed to set value for {locator}")

        def select_dropdown_option(self, dropdown_locator, option_modal_locator, option_text):
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(dropdown_locator)
            )
            dropdown.click()

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(option_modal_locator)
            )
            option_locator = (
            By.XPATH,
            f"//div[contains(@class,'sc-dTvVRJ')][normalize-space()='{option_text}']"
            )

            option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(option_locator)
            )
            option.click()

        def place_order(self, order_type="Market", volume=10, stop_loss=100, take_profit=200):
            self.select_dropdown_option(self.ORDER_TYPE_DROPDOWN, self.ORDER_TYPE_OPTIONS, order_type)

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.VOLUME_INPUT)
            )
            self.set_value_with_retry(self.VOLUME_INPUT, volume)

            clean_price = self.wait_for_valid_price()
            current_price = float(clean_price)

            if order_type == "Limit" or order_type == "Stop":
                limit_price = current_price 
                self.set_value_with_retry(self.PRICE_INPUT, limit_price)

            stop_loss_price = current_price - stop_loss
            take_profit_price = current_price + take_profit

            self.set_value_with_retry(self.STOP_LOSS_INPUT, stop_loss_price)
            self.set_value_with_retry(self.TAKE_PROFIT_INPUT, take_profit_price)

            if(order_type == "Stop"):
                self.select_dropdown_option(self.EXPIRY_DROPDOWN, self.EXPIRY_OPTIONS, "Good Till Day")

            self.click(self.BUY_BUTTON)

            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.CONFIRM_BUTTON)
            )
            self.click(self.CONFIRM_BUTTON)

        #region Open Listing
        def get_first_record(self, locator):
            self.wait.until(EC.visibility_of_element_located(locator))
            records = self.driver.find_elements(*locator)
            if not records:
                return None
            return records[0]
        
        def edit_open_position(self, sl_decrease=50):
            record = self.get_first_record(self.OPEN_RECORD)
            if not record:
                print("No open record found")
                return

            record.find_element(*self.EDIT_BUTTON).click()

            modal_overlay = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.EDIT_MODAL)
            )

            sl_input = modal_overlay.find_element(*self.OPEN_SL_PRICE)
            def value_populated(driver):
                val = sl_input.get_attribute("value")
                return val

            current_sl_str = WebDriverWait(self.driver, 10).until(value_populated)
            
            current_sl = float(current_sl_str.strip())

            new_sl = current_sl - sl_decrease
            sl_input.clear()
            sl_input.send_keys(Keys.BACKSPACE * 10) 
            sl_input.send_keys(str(new_sl))

            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", sl_input)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", sl_input)

            self.click(self.UPDATE_BUTTON)

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.EDIT_CONFIRM_BUTTON))
            self.click(self.EDIT_CONFIRM_BUTTON)


        def partial_close_position(self, percent=80):
            record = self.get_first_record(self.OPEN_RECORD)
            if not record:
                print("No open record found")
                return

            # Click Close
            record.find_element(*self.CLOSE_BUTTON).click()

            # Wait for volume input
            self.wait.until(EC.visibility_of_element_located(self.OPEN_VOLUME))

            # Calculate new volume
            current_volume = float(self.get_attribute(self.OPEN_VOLUME, "value"))
            new_volume = current_volume * (percent / 100)

            self.clear(self.OPEN_VOLUME)
            self.send_keys(self.OPEN_VOLUME, Keys.BACKSPACE * 10)
            self.send_keys(self.OPEN_VOLUME, str(new_volume))

            # Confirm partial close
            self.click(self.CLOSE_CONFIRM_BUTTON)

        def full_close_position(self):
            record = self.get_first_record(self.OPEN_RECORD)
            if not record:
                print("No open record found")
                return

            # Click Close
            record.find_element(*self.CLOSE_BUTTON).click()

            # Wait for confirm button
            self.wait.until(EC.element_to_be_clickable(self.CLOSE_CONFIRM_BUTTON))

            # Confirm full close
            self.click(self.CLOSE_CONFIRM_BUTTON)
        #endregion

        #region Pending Listing
        def edit_pending_order(self, price_decrease=1):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.PENDING_TAB)
            )
            self.click(self.PENDING_TAB)

            record = self.get_first_record(self.PENDING_RECORD)
            if not record:
                print("No open record found")
                return

            record.find_element(*self.EDIT_BUTTON).click()

            modal_overlay = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.EDIT_CONFIRMATION_MODAL)
            )

            input = modal_overlay.find_element(*self.PENDING_PRICE)
            def value_populated(driver):
                val = input.get_attribute("value")
                return val

            current_str = WebDriverWait(self.driver, 10).until(value_populated)
            
            current_price = float(current_str.strip())

            new_price = current_price - price_decrease
            input.clear()
            input.send_keys(Keys.BACKSPACE * 10) 
            input.send_keys(str(new_price))

            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", input)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", input)

            self.click(self.PENDING_UPDATE_BUTTON)

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.EDIT_CONFIRM_BUTTON))
            self.click(self.EDIT_CONFIRM_BUTTON)
        #endregion

        #region Validation
        def get_first_history_record(self):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.HISTORY_TAB)
            )
            self.click(self.HISTORY_TAB)

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.HISTORY_RECORD)
            )

            records = self.driver.find_elements(*self.HISTORY_RECORD)
            if not records:
                return None

            row = records[0]
            return {
                "order_type": row.find_element(*self.ORDER_TYPE).text.strip(),
                "entry_price": row.find_element(*self.ENTRY_PRICE).text.strip(),
                "volume": row.find_element(*self.VOLUME).text.strip()
            }
        #endregion
        def get_notification(self):
            return self.get_text(self.NOTIFICATION)

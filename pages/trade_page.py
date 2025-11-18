from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class TradePage(BasePage):
    BUY_BUTTON = (By.ID, "buyBtn")
    SELL_BUTTON = (By.ID, "sellBtn")
    MARKET_ORDER_BTN = (By.ID, "marketOrder")
    STOP_LOSS_INPUT = (By.ID, "stopLoss")
    TAKE_PROFIT_INPUT = (By.ID, "takeProfit")
    NOTIFICATION = (By.ID, "notification")  # Example, replace with actual

    def place_market_order(self, order_type="buy", stop_loss=None, take_profit=None):
        if order_type.lower() == "buy":
            self.click(self.BUY_BUTTON)
        else:
            self.click(self.SELL_BUTTON)

        if stop_loss:
            self.send_keys(self.STOP_LOSS_INPUT, stop_loss)
        if take_profit:
            self.send_keys(self.TAKE_PROFIT_INPUT, take_profit)

        self.click(self.MARKET_ORDER_BTN)

    def get_notification(self):
        return self.get_text(self.NOTIFICATION)

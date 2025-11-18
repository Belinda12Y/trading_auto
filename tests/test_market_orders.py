import pytest
from pages.login_page import LoginPage
from pages.trade_page import TradePage
from selenium.webdriver.common.by import By

def test_place_market_order(driver):
    login_page = LoginPage(driver)
    login_page.login()

    trade_page = TradePage(driver)
    trade_page.place_market_order(order_type="buy", stop_loss="100", take_profit="200")

    notification = trade_page.get_notification()
    assert "Order Placed" in notification  # Replace with actual expected text

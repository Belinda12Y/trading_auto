from pages.login_page import LoginPage
from pages.trade_page import TradePage

def test_place_limit_order(driver):
    login_page = LoginPage(driver)
    login_page.login()

    trade_page = TradePage(driver)
    trade_page.place_order(order_type="Limit", volume ="10", stop_loss=100.00, take_profit=200.00)
    trade_page.place_order(order_type="Stop", volume ="10", stop_loss=100.00, take_profit=100.00)
    notification = trade_page.get_notification()
    assert "Order has been created." in notification

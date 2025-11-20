from pages.login_page import LoginPage
from pages.trade_page import TradePage

def test_pending_order_management(driver):
    login_page = LoginPage(driver)
    login_page.login()

    trade_page = TradePage(driver)
    trade_page.edit_pending_order(price_decrease=1.00)
    notification = trade_page.get_notification()
    assert "Order has been updated." in notification 
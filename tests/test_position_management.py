from pages.login_page import LoginPage
from pages.trade_page import TradePage

def test_position_management(driver):
    login_page = LoginPage(driver)
    login_page.login()

    trade_page = TradePage(driver)
    trade_page.edit_open_position(sl_decrease=50.00)
    trade_page.partial_close_position(percent=80)
    trade_page.full_close_position()
    notification = trade_page.get_notification()
    assert (
    "Position has been closed." in notification 
    or "Position has been updated." in notification 
    )
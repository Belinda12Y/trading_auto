from pages.login_page import LoginPage
from pages.trade_page import TradePage

def test_validate_order_history_entry_price(driver):
    login = LoginPage(driver)
    login.login()

    trade = TradePage(driver)

    clean_price = trade.wait_for_valid_price()
    expected_entry_price = float(clean_price)

    trade.place_order(order_type="Market", volume=10)

    trade.full_close_position()

    history = trade.get_first_history_record()

    assert history is not None, "No history record found!"

    history_entry_price = float(history["entry_price"].replace(",", ""))
    assert abs(history_entry_price - expected_entry_price) < 0.1, \
        f"Entry price mismatch: expected {expected_entry_price}, got {history_entry_price}"

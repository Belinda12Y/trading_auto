from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import USERNAME, PASSWORD

class LoginPage(BasePage):
    USERNAME_INPUT = (By.CSS_SELECTOR, "[data-testid='login-user-id']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-testid='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-testid='login-submit']")

    def login(self, username=USERNAME, password=PASSWORD):
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

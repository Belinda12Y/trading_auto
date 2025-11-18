from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import USERNAME, PASSWORD

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")

    def login(self, username=USERNAME, password=PASSWORD):
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

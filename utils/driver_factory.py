from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    driver_path = ChromeDriverManager().install()  # working ChromeDriver path
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # optional for CI/CD
    driver = webdriver.Chrome(service=Service(driver_path), options=options)
    return driver

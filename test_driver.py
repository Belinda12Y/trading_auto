from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Install and get the ChromeDriver path
driver_path = ChromeDriverManager().install()

# Start Chrome browser
driver = webdriver.Chrome(service=Service(driver_path))
driver.get("https://www.google.com")

# Print page title
print(driver.title)

# Close the browser
driver.quit()

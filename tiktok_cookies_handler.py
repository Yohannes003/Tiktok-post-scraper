
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
import pickle
import time

firefox_options = webdriver.FirefoxOptions()
firefox_service = FirefoxService(GeckoDriverManager().install())
driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
driver.get("https://www.tiktok.com/login")
time.sleep(120)  # Time to log in manually

# Save cookies
with open("tiktok_cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)
driver.quit()


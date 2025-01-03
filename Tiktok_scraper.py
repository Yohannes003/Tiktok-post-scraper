from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from tiktok_captcha_solver import SeleniumSolver
from selenium_stealth import stealth
import undetected_chromedriver as uc
import pickle
import json

def setup_driver():
    driver = uc.Chrome(headless=False)  
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver

def load_cookies(driver, cookie_file='tiktok_cookies.pkl'):
    if os.path.exists(cookie_file):
        with open(cookie_file, 'rb') as file:
            cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
        print(f"Loaded cookies from {cookie_file}.")
    else:
        print(f"Cookie file {cookie_file} not found. Proceeding without cookies.")

def save_to_json(data, filename="scraped_data.json"):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

def solve_captcha(driver, api_key):
    sadcaptcha = SeleniumSolver(
        driver,
        api_key,
        mouse_step_size=1,  # Adjust to change mouse speed
        mouse_step_delay_ms=10  # Adjust to change mouse speed
    )
    try:
        solved = sadcaptcha.solve_captcha_if_present()
        if solved:
            print("CAPTCHA solved successfully!")
        else:
            print("No CAPTCHA detected or failed to solve CAPTCHA.")
    except Exception as e:
        print(f"Error solving CAPTCHA: {e}")

def scrape_tiktok_video(url, cookies_file, api_key):
    driver = setup_driver()

    try:
        # Step 1: Load TikTok homepage and apply cookies
        driver.get("https://www.tiktok.com/login")
        time.sleep(5)  # Allow page to load

        # Check for CAPTCHA after loading the homepage
        if "captcha" in driver.page_source.lower():
            print("CAPTCHA detected on homepage. Attempting to solve CAPTCHA...")
            solve_captcha(driver, api_key)
            time.sleep(5)  # Wait for CAPTCHA solving

        load_cookies(driver, cookies_file)
        driver.refresh()
        time.sleep(5)  # Allow page to reload with cookies

        # Step 2: Navigate to the target video URL
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        # Check if CAPTCHA appears after navigating to the video
        if "captcha" in driver.page_source.lower():
            print("CAPTCHA detected on target page. Attempting to solve CAPTCHA...")
            solve_captcha(driver, api_key)
            time.sleep(5)  # Wait for CAPTCHA solving

        # Step 3: Scrape data
        data = {}

        # Username
        try:
            username_element = driver.find_element(By.CSS_SELECTOR, 'span.css-1c7urt-SpanUniqueId.evv7pft1')  # Adjust the class or selector
            username = username_element.text
            data['username'] = username
        except Exception as e:
            print(f"Error extracting username: {e}")
            data['username'] = None

        # Profile Image
        try:
            profile_image = driver.find_element(By.CSS_SELECTOR, 'img.css-1zpj2q-ImgAvatar.e1e9er4e1').get_attribute("src")
            data['profile_image'] = profile_image
        except Exception as e:
            print(f"Error extracting profile image: {e}")
            data['profile_image'] = None

        # Nickname and Post Date
        try:
            nickname_post_date = driver.find_element(By.CSS_SELECTOR, 'span[data-e2e="browser-nickname"]')
            nickname = nickname_post_date.find_element(By.CLASS_NAME, 'css-1xccqfx-SpanNickName').text
            post_date = nickname_post_date.find_elements(By.TAG_NAME, "span")[-1].text
            data['nickname'] = nickname
            data['post_date'] = post_date
        except Exception as e:
            print(f"Error extracting nickname or post date: {e}")
            data['nickname'] = None
            data['post_date'] = None

        # Post Text
        try:
            post_text = driver.find_element(By.CSS_SELECTOR, 'h1.css-1fbzdvh-H1Container.ejg0rhn1').text
            data['post_text'] = post_text
        except Exception as e:
            print(f"Error extracting post text: {e}")
            data['post_text'] = None

        # Likes and Comments Count
        try:
            likes = driver.find_element(By.CSS_SELECTOR, 'strong[data-e2e="like-count"]').text
            comments_count = driver.find_element(By.CSS_SELECTOR, 'strong[data-e2e="comment-count"]').text
            data['likes'] = likes
            data['comments_count'] = comments_count
        except Exception as e:
            print(f"Error extracting likes or comments count: {e}")
            data['likes'] = None
            data['comments_count'] = None

        # Print the scraped data
        print("Scraped Data:")
        print(json.dumps(data, indent=4, ensure_ascii=False))

        # Save the data to JSON
        save_to_json(data)

    except Exception as e:
        print(f"General scraping error: {e}")
    finally:
        driver.quit()

cookies_file = "tiktok_cookies.pkl"
API_KEY = "your api key"
TARGET_URL = "https://www.tiktok.com/@pythonblyat5/video/7443113349149117718"
scrape_tiktok_video(TARGET_URL, "tiktok_cookies.pkl", API_KEY)

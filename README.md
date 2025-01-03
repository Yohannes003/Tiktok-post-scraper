
---

# TikTok Post Scraper with CAPTCHA Solver

This project uses Selenium and other libraries to scrape TikTok video data, including the username, profile image, post text, likes, comments, and more. It also includes a CAPTCHA solver to bypass TikTok's CAPTCHA protection.

## Requirements

Before running the scraper, you need to install the required Python packages and set up the necessary configurations.

### Required Libraries

1. **Selenium**: For web automation and scraping.
2. **undetected_chromedriver**: For using a stealth Chrome driver to avoid detection by TikTok.
3. **selenium_stealth**: To make the browser session more undetectable.
4. **tiktok_captcha_solver**: To solve the CAPTCHA challenges.
5. **pickle**: For storing and loading cookies.
6. **json**: For saving the scraped data in JSON format.

Install the necessary libraries by running:

```bash
pip install selenium undetected-chromedriver selenium-stealth tiktok-captcha-solver
```

### API Key

- You need a valid API key for the **tiktok_captcha_solver**. You can obtain it from the service you're using for CAPTCHA solving. The API key is required for bypassing TikTok's CAPTCHA.

### Cookie File

- To avoid logging in every time, you should have a `tiktok_cookies.pkl` file containing your TikTok session cookies. You can generate this file by running the `tiktok_cookies_handler.py` script after logging into TikTok via the browser.

## Setup

### Steps to Run the Scraper

1. **Set up the environment**: Ensure you have all required libraries installed.
2. **Obtain the API Key**: Obtain a valid API key for the CAPTCHA solver and replace it in the script (`API_KEY = "your_api_key"`).
3. **Capture Cookies**: Run the `tiktok_cookies_handler.py` script to capture and save your cookies in a `tiktok_cookies.pkl` file.
4. **Run the Scraper**: Execute the main scraping script to scrape data from TikTok videos.

```bash
python Tiktok_scraper.py
```

### Configuration Details

- **`setup_driver()`**: Configures a headless Chrome browser with stealth settings to avoid detection.
- **`load_cookies()`**: Loads cookies from the specified file (`tiktok_cookies.pkl`) to bypass login.
- **`save_to_json()`**: Saves the scraped data to a JSON file (`scraped_data.json`).
- **`solve_captcha()`**: Handles CAPTCHA detection and solving via the `tiktok_captcha_solver` API.

### Example Usage

```python
TARGET_URL = "https://www.tiktok.com/@pythonblyat5/video/7443113349149117718"
scrape_tiktok_video(TARGET_URL, "tiktok_cookies.pkl", "your_api_key_here")
```

### Functionality

- The script opens TikTok in a browser, loads the specified video URL, and scrapes the following data:
  - **Username**: The username of the video creator.
  - **Profile Image**: The URL of the user's profile image.
  - **Nickname**: The display name of the user.
  - **Post Date**: The date when the post was published.
  - **Post Text**: The text content of the post.
  - **Likes**: The number of likes on the post.
  - **Comments Count**: The number of comments on the post.

- The data is printed to the console and saved as `scraped_data.json`.

### Error Handling

The script includes basic error handling for:
- Missing cookies file.
- CAPTCHA detection and solving.
- Data extraction failures.

### Troubleshooting

- **CAPTCHA Issues**: If the CAPTCHA solver fails, try adjusting the settings or use a different API key.
- **Incorrect Selectors**: TikTok might update their page structure, so you may need to update the CSS selectors in the script if data extraction fails.

---


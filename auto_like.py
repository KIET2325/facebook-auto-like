FB_EMAIL = "0877224335"
FB_PASSWORD = "minhkiet123"

import os
import time
from datetime import datetime, timedelta

import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Đọc thông tin đăng nhập từ biến môi trường
FB_EMAIL = os.getenv('FB_EMAIL')
FB_PASSWORD = os.getenv('FB_PASSWORD')

def login(driver):
    driver.get('https://www.facebook.com')
    time.sleep(2)
    driver.find_element(By.ID, 'email').send_keys(FB_EMAIL)
    driver.find_element(By.ID, 'pass').send_keys(FB_PASSWORD)
    driver.find_element(By.NAME, 'login').click()
    time.sleep(5)

def auto_like():
    # Khởi tạo headless Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)
    login(driver)

    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)

    while datetime.now() < end_time:
        posts = driver.find_elements(By.XPATH, "//div[@role='article']")
        for post in posts:
            try:
                if 'Bạn bè' in post.text:
                    btn = post.find_elements(By.XPATH, ".//div[@aria-label='Thích']")
                    if btn:
                        btn[0].click()
                        print(f"[{datetime.now()}] Đã like bài viết của bạn bè.")
                        time.sleep(10)
            except Exception as e:
                print("Lỗi khi like:", e)
        # Load thêm bài
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(3)

    driver.quit()

# Lên lịch chạy 1 lần mỗi ngày lúc 20:00 (cron sẽ trigger Actions)
# schedule.every().day.at("20:00").do(auto_like)

# Test chạy luôn không cần chờ
auto_like()

# if __name__ == '__main__':
#     print("Đang chờ schedule chạy...")
#     while True:
#         schedule.run_pending()
#         time.sleep(30)


#if __name__ == '__main__':
 #   print("Đang chờ schedule chạy...")
  #  while True:
   #     schedule.run_pending()
    #    time.sleep(30)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import schedule
from datetime import datetime, timedelta

# Cấu hình tài khoản FB và đường dẫn tới ChromeDriver
FB_EMAIL = '0877224335'
FB_PASSWORD = 'minhkiet123'
CHROME_DRIVER_PATH = './chromedriver'  # tải chromedriver phù hợp version Chrome

# Hàm đăng nhập Facebook
def login(driver):
    driver.get('https://www.facebook.com')
    time.sleep(2)
    driver.find_element(By.ID, 'email').send_keys(FB_EMAIL)
    driver.find_element(By.ID, 'pass').send_keys(FB_PASSWORD)
    driver.find_element(By.NAME, 'login').click()
    time.sleep(5)

# Hàm thực hiện thả like bài đăng của bạn bè
def auto_like():
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    login(driver)

    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)

    while datetime.now() < end_time:
        posts = driver.find_elements(By.XPATH, '//div[@role="article"]')

        for post in posts:
            try:
                # Kiểm tra nếu bài viết là từ bạn bè (dựa vào presence của dòng “Bạn bè”)
                if 'Bạn bè' in post.text:
                    like_buttons = post.find_elements(By.XPATH, ".//div[@aria-label='Thích']")
                    if like_buttons:
                        like_buttons[0].click()
                        print(f"[{datetime.now()}] Đã like bài viết.")
                        time.sleep(10)
            except Exception as e:
                print("Lỗi:", e)
                continue

        # Kéo xuống để load thêm bài viết
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(3)

    driver.quit()

# Lên lịch chạy mỗi ngày lúc 8 giờ tối
schedule.every().day.at("20:00").do(auto_like)

print("Đang chờ đến giờ chạy script...")
while True:
    schedule.run_pending()
    time.sleep(30)

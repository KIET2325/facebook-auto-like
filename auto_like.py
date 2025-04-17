import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Tải biến từ file .env
load_dotenv()

import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Đọc thông tin đăng nhập từ biến môi trường
FB_EMAIL = os.getenv('FB_EMAIL')
FB_PASSWORD = os.getenv('FB_PASSWORD')

# Kiểm tra biến môi trường
if not FB_EMAIL or not FB_PASSWORD:
    print("❌ Thiếu biến môi trường: FB_EMAIL hoặc FB_PASSWORD")
    exit()

def login(driver):
    driver.get("https://www.facebook.com")
    time.sleep(2)

    email_input = driver.find_element(By.ID, 'email')
    pass_input = driver.find_element(By.ID, 'pass')
    login_btn = driver.find_element(By.NAME, 'login')

    email_input.send_keys(FB_EMAIL)
    pass_input.send_keys(FB_PASSWORD)
    login_btn.click()

    time.sleep(5)  # Chờ trang tải xong sau khi đăng nhập

def auto_like():
    # Mở trình duyệt ở chế độ hiển thị (có thể đổi sang headless nếu muốn)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        login(driver)

        # 👉 TODO: Thêm URL bài viết hoặc newsfeed bạn muốn tự động like
        driver.get("https://www.facebook.com/YOUR_TARGET_PAGE_OR_POST")
        time.sleep(5)

        # 👉 Tìm nút "Like" và click (bạn cần cập nhật chính xác selector tuỳ theo nội dung)
        like_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Thích' or @aria-label='Like']")
        if like_buttons:
            like_buttons[0].click()
            print("✅ Đã like bài viết.")
        else:
            print("⚠️ Không tìm thấy nút Like.")

    except Exception as e:
        print("❌ Lỗi:", e)
    finally:
        driver.quit()

# Lên lịch chạy mỗi ngày lúc 8:00 sáng
# schedule.every().day.at("08:00").do(auto_like)

# Chạy ngay lập tức để test
if __name__ == "__main__":
    auto_like()

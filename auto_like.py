from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, os, random

LOG_FILE = "log_liked_posts.txt"

def load_liked_log():
    if not os.path.exists(LOG_FILE):
        return set()
    with open(LOG_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_to_log(post_id):
    with open(LOG_FILE, "a") as f:
        f.write(post_id + "\n")

def is_friend_post(post):
    try:
        author_span = post.find_element(By.XPATH, ".//span[contains(text(), 'bạn bè')]")
        return True if author_span else False
    except:
        return False

def auto_like():
    options = Options()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Tạm thời dùng headless thường
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    liked_log = load_liked_log()
    liked_count = 0

    try:
        driver.get("https://www.facebook.com/")
        input("➡️ Sau khi đăng nhập xong Facebook, nhấn ENTER để tiếp tục...")

        scrolls = 0
        while liked_count < 20 and scrolls < 10:
            posts = driver.find_elements(By.XPATH, "//div[@role='article']")
            print(f"📦 Đã tìm thấy {len(posts)} bài viết...")

            for post in posts:
                post_id = post.get_attribute("data-ft") or str(hash(post.get_attribute("innerHTML")))

                if not post_id or post_id in liked_log:
                    continue

                if not is_friend_post(post):
                    continue

                try:
                    like_button = post.find_element(By.XPATH, ".//div[@aria-label='Thích']")
                    if like_button:
                        like_button.click()
                        liked_count += 1
                        print(f"❤️ Đã like bài #{liked_count} - ID: {post_id}")
                        save_to_log(post_id)
                        time.sleep(random.randint(5, 15))
                        if liked_count >= 20:
                            break
                except Exception as e:
                    continue

            # Cuộn xuống để load thêm bài
            driver.execute_script("window.scrollBy(0, 1500);")
            time.sleep(3)
            scrolls += 1

    except Exception as e:
        print("❌ Lỗi:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    auto_like()

import asyncio
from pyppeteer import launch
import os

# Lấy cookie từ biến môi trường
FB_COOKIE = os.environ.get("FB_COOKIE", "")

async def auto_like():
    # Ép pyppeteer dùng Chrome đã cài
    browser = await launch(
        headless=True,
        executablePath="/usr/bin/google-chrome",
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )
    page = await browser.newPage()

    # Chuyển cookie string thành list các dict
    cookies = []
    for item in FB_COOKIE.split(';'):
        parts = item.strip().split('=', 1)
        if len(parts) == 2:
            cookies.append({
                'name': parts[0],
                'value': parts[1],
                'domain': '.facebook.com',
                'path': '/',
            })

    # Vào trang Facebook để set cookie và đăng nhập
    await page.goto('https://facebook.com', {'waitUntil': 'networkidle2'})
    if cookies:
        await page.setCookie(*cookies)

    # Mở newsfeed và chờ nút Like xuất hiện
    await page.goto('https://www.facebook.com/', {'waitUntil': 'networkidle2'})
    await page.waitForSelector('[aria-label="Thích"], [aria-label="Like"]', {'timeout': 10000})

    print("Đã đăng nhập bằng cookie!")

    # Like bài viết đầu tiên
    buttons = await page.querySelectorAll('[aria-label="Thích"], [aria-label="Like"]')
    if buttons:
        await buttons[0].click()
        print("Đã like bài viết đầu tiên.")
    else:
        print("Không tìm thấy nút Like.")

    await asyncio.sleep(2)
    await browser.close()

if __name__ == '__main__':
    asyncio.run(auto_like())

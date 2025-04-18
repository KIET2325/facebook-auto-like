import asyncio
from pyppeteer import launch
import os

FB_COOKIE = os.environ.get("FB_COOKIE")

async def auto_like():
    browser = await launch(headless=True,
                           args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()

    # Chuyển cookie string thành list các dict
    cookies = []
    for item in FB_COOKIE.split(';'):
        parts = item.strip().split('=')
        if len(parts) == 2:
            cookies.append({
                'name': parts[0],
                'value': parts[1],
                'domain': '.facebook.com',
                'path': '/',
            })

    # Set cookies
    await page.goto('https://facebook.com')  # Phải vào trước khi set cookies
    await page.setCookie(*cookies)

    # Mở Facebook sau khi set cookie
    await page.goto('https://www.facebook.com/', {'waitUntil': 'networkidle2'})
    await page.waitForSelector('[aria-label="Thích"]', {'timeout': 10000})

    print("Đã đăng nhập bằng cookie!")

    # Like post đầu tiên
    like_buttons = await page.querySelectorAll('[aria-label="Thích"]')
    if like_buttons:
        await like_buttons[0].click()
        print("Đã like bài viết đầu tiên.")
    else:
        print("Không tìm thấy nút Like.")

    await asyncio.sleep(2)
    await browser.close()

asyncio.run(auto_like())

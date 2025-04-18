import asyncio
import random
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
        parts = item.strip().split('=', 1)
        if len(parts) == 2:
            cookies.append({
                'name': parts[0],
                'value': parts[1],
                'domain': '.facebook.com',
                'path': '/',
            })

    # Truy cập Facebook và set cookie
    await page.goto('https://mbasic.facebook.com', {'waitUntil': 'networkidle2'})
    await page.setCookie(*cookies)

    # Reload lại trang sau khi set cookie để hiển thị newsfeed
    await page.goto('https://mbasic.facebook.com', {'waitUntil': 'networkidle2'})

    print("Đã đăng nhập bằng cookie!")

    # Lấy danh sách bài viết (thẻ div có role bài đăng)
    posts = await page.xpath('//div[contains(@id, "story") and .//a[text()="Thích"]]')
    print(f"Tìm thấy {len(posts)} bài viết có nút Thích.")

    count = 0
    for post in posts:
        if count >= 10:
            break
        like_btns = await post.xpath('.//a[text()="Thích"]')
        if like_btns:
            await like_btns[0].click()
            count += 1
            print(f"Đã like {count} bài viết.")
            delay = random.randint(5, 10)
            await page.waitForTimeout(delay * 1000)

    await browser.close()

# Chạy script với xử lý lỗi vòng lặp
try:
    asyncio.run(auto_like())
except RuntimeError as e:
    if str(e) != 'Event loop is closed':
        raise

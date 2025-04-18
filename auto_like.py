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
    await page.goto('https://www.facebook.com', {'waitUntil': 'networkidle2'})
    await page.setCookie(*cookies)

    # Reload lại trang sau khi set cookie để hiển thị newsfeed
    await page.goto('https://www.facebook.com', {'waitUntil': 'networkidle2'})
    print("Đã đăng nhập bằng cookie!")

    # Đợi thêm trước khi scroll để Facebook load feed
    await asyncio.sleep(5)

    # Debug: in ra HTML (chỉ 2000 ký tự đầu)
    html = await page.content()
    print("Trang HTML sau login:\n", html[:2000])

    # Cuộn trang nhiều lần để tải bài viết
    for _ in range(5):
        await page.evaluate('window.scrollBy(0, window.innerHeight)')
        await asyncio.sleep(2)

    # Lấy tất cả bài viết
    posts = await page.querySelectorAll('div[role="article"]')
    print(f"Tìm thấy {len(posts)} bài viết trong newsfeed.")

    count = 0
    for post in posts:
        if count >= 10:
            break

        # Kiểm tra nếu trong post có nút Like (bài viết, không phải comment)
        like_buttons = await post.xpath('.//span[contains(text(), "Thích") or contains(text(), "Like")]/ancestor::div[@role="button"]')
        if like_buttons:
            try:
                await like_buttons[0].click()
                count += 1
                print(f"Đã like {count} bài viết.")
                delay = random.randint(5, 10)
                await asyncio.sleep(delay)
            except Exception as e:
                print(f"Lỗi khi like: {e}")
                continue

    await browser.close()

# Chạy script với xử lý lỗi vòng lặp
try:
    asyncio.run(auto_like())
except RuntimeError as e:
    if str(e) != 'Event loop is closed':
        raise

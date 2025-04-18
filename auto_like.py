import asyncio
import os
from pyppeteer import launch
import random

FB_COOKIE = os.environ.get("FB_COOKIE")

async def auto_like():
    browser = await launch(headless=False,  # Để kiểm tra DOM nếu cần debug
                           args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()

    await page.setUserAgent(
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1"
    )

    # Parse cookie
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

    # Vào m.facebook.com
    await page.goto('https://m.facebook.com', {'waitUntil': 'networkidle2'})
    await page.setCookie(*cookies)

    await page.goto('https://m.facebook.com', {'waitUntil': 'networkidle2'})
    print("✅ Đã đăng nhập!")

    await asyncio.sleep(2)

    # In ra HTML để debug
    html = await page.content()
    print("✅ HTML sau login:\n", html[:2000])

    # Tìm các bài viết
    posts = await page.xpath('//div[contains(@data-ft, "") and .//a[contains(@href, "/a/like.php")]]')
    print(f"📰 Tìm thấy {len(posts)} bài viết có thể Like")

    count = 0
    for post in posts:
        if count >= 10:
            break
        try:
            like_link = await post.xpath('.//a[contains(@href, "/a/like.php")]')
            if like_link:
                href = await (await like_link[0].getProperty('href')).jsonValue()
                await page.goto(href)
                print(f"👍 Đã Like bài viết {count + 1}")
                await asyncio.sleep(random.randint(3, 6))
                count += 1
        except Exception as e:
            print(f"❌ Lỗi khi Like: {e}")

    await browser.close()

try:
    asyncio.run(auto_like())
except RuntimeError as e:
    if str(e) != 'Event loop is closed':
        raise

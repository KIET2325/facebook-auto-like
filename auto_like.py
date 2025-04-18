import asyncio
from pyppeteer import launch
import os
import random

FB_COOKIE = os.getenv('FB_COOKIE')

async def main():
    browser = await launch(
        headless=False,  # Đặt True nếu không cần hiển thị trình duyệt
        args=['--no-sandbox']
    )
    page = await browser.newPage()

    # Thiết lập cookie thủ công
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    await page.setCookie({
        'name': 'c_user',
        'value': FB_COOKIE.split('c_user=')[1].split(';')[0],
        'domain': '.facebook.com',
        'path': '/',
    }, {
        'name': 'xs',
        'value': FB_COOKIE.split('xs=')[1].split(';')[0],
        'domain': '.facebook.com',
        'path': '/',
    })

    # Truy cập newsfeed mobile
    await page.goto('https://m.facebook.com', {'waitUntil': 'networkidle2'})
    print("✅ Đã đăng nhập bằng cookie!")

    # Scroll nhẹ để load thêm bài viết
    for i in range(3):
        await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
        await asyncio.sleep(2)

    # Tìm tất cả nút Like
    like_links = await page.xpath('//a[contains(@href, "/a/like.php")]')
    print(f"📰 Tìm thấy {len(like_links)} nút Like")

    count = 0
    for link in like_links:
        if count >= 10:
            break
        try:
            href = await (await link.getProperty('href')).jsonValue()
            await page.goto(href)
            print(f"👍 Đã Like bài viết {count + 1}")
            await asyncio.sleep(random.randint(3, 6))
            count += 1
        except Exception as e:
            print(f"❌ Lỗi khi Like: {e}")

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

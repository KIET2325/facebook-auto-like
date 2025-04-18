const puppeteer = require('puppeteer-extra');
const Stealth = require('puppeteer-extra-plugin-stealth');
puppeteer.use(Stealth());

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox'],
    executablePath: '/usr/bin/google-chrome' // GitHub Actions dùng chrome mặc định
  });

  const [page] = await browser.pages();
  const cookies = JSON.parse(process.env.FB_COOKIE || '[]');
  await page.setCookie(...cookies);

  await page.goto('https://m.facebook.com', { waitUntil: 'domcontentloaded' });

  const posts = await page.$$('article');
  for (let post of posts) {
    const like = await post.$('a[aria-label*="Like"], a[aria-label*="Thích"]');
    if (like) {
      await like.click();
      await page.waitForTimeout(2000 + Math.random() * 3000);
    }
  }

  await browser.close();
})();

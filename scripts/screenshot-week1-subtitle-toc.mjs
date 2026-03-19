import path from "node:path";
import { fileURLToPath } from "node:url";

import puppeteerImport from "puppeteer";
const puppeteer = puppeteerImport?.default ?? puppeteerImport;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rootDir = path.join(__dirname, "..");
const pageFile = path.join(rootDir, "pages", "phase-1", "module-1", "week-1", "index.html");
const outputFile = path.join(rootDir, "screenshots", "week-1-subtitle-toc.png");
const pageUrl = `file://${pageFile}`;

const browser = await puppeteer.launch({
  headless: "new",
  args: ["--no-sandbox", "--disable-setuid-sandbox"],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 850, deviceScaleFactor: 2 });

  await page.goto(pageUrl, { waitUntil: "domcontentloaded" });
  await page.waitForSelector("article.prose .pageSubtitle");
  await page.waitForSelector("article.prose .proseToc");
  await new Promise((r) => setTimeout(r, 200));

  const clip = await page.evaluate(() => {
    const article = document.querySelector("article.prose");
    if(!article) return null;
    const sub = article.querySelector(".pageSubtitle");
    const toc = article.querySelector(".proseToc");
    if(!sub || !toc) return null;

    const r1 = sub.getBoundingClientRect();
    const r2 = toc.getBoundingClientRect();

    const top = Math.min(r1.top, r2.top);
    const left = Math.min(r1.left, r2.left);
    const right = Math.max(r1.right, r2.right);
    const bottom = Math.max(r1.bottom, r2.bottom);

    const pad = 16;
    return {
      x: Math.max(0, Math.floor(left - pad)),
      y: Math.max(0, Math.floor(top - pad)),
      width: Math.ceil(right - left) + pad * 2,
      height: Math.ceil(bottom - top) + pad * 2,
    };
  });

  if(!clip) throw new Error("Could not determine clip bounds.");

  await page.screenshot({ path: outputFile, clip });
  // eslint-disable-next-line no-console
  console.log(`Saved screenshot: ${outputFile}`);
} finally {
  await browser.close();
}


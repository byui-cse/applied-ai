import path from "node:path";
import { fileURLToPath } from "node:url";

// `puppeteer` is intentionally not listed in dependencies; we load it via `npx -p puppeteer ...`.
import puppeteerImport from "puppeteer";

const puppeteer = puppeteerImport?.default ?? puppeteerImport;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rootDir = path.join(__dirname, "..");
const pageFile = path.join(rootDir, "pages", "phase-1", "module-1", "week-1", "index.html");
const outputFile = path.join(rootDir, "screenshots", "week-1-header.png");

const pageUrl = `file://${pageFile}`;

const browser = await puppeteer.launch({
  headless: "new",
  // Commonly required in containerized/sandboxed environments.
  args: ["--no-sandbox", "--disable-setuid-sandbox"],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 650, deviceScaleFactor: 2 });

  await page.goto(pageUrl, { waitUntil: "domcontentloaded" });
  await page.waitForSelector("article.prose h1");
  // Small delay for any late CSS/app.js effects.
  await new Promise((r) => setTimeout(r, 200));

  // Screenshot the page header: `h1` + optional `.pageSubtitle`.
  const clip = await page.evaluate(() => {
    const h1 = document.querySelector("article.prose h1");
    const sub = document.querySelector("article.prose .pageSubtitle");
    if (!h1) return null;

    const r1 = h1.getBoundingClientRect();
    let top = r1.top;
    let left = r1.left;
    let right = r1.right;
    let bottom = r1.bottom;

    if (sub) {
      const rs = sub.getBoundingClientRect();
      top = Math.min(top, rs.top);
      left = Math.min(left, rs.left);
      right = Math.max(right, rs.right);
      bottom = Math.max(bottom, rs.bottom);
    }

    const pad = 16;
    return {
      x: Math.max(0, Math.floor(left - pad)),
      y: Math.max(0, Math.floor(top - pad)),
      width: Math.ceil(right - left) + pad * 2,
      height: Math.ceil(bottom - top) + pad * 2,
    };
  });

  if (!clip) throw new Error("Could not determine header clip bounds.");

  await page.screenshot({ path: outputFile, clip });
  // eslint-disable-next-line no-console
  console.log(`Saved screenshot: ${outputFile}`);
} finally {
  await browser.close();
}


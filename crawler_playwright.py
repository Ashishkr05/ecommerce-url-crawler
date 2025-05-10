import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urljoin
import re
from collections import defaultdict
import json
import logging

# -------------------- Logging Setup --------------------
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger()

# -------------------- Configuration --------------------
DOMAINS = [
    "https://www.virgio.com/",
    "https://www.tatacliq.com/",
    "https://www.nykaafashion.com/",
    "https://www.westside.com/",
]

PRODUCT_PATTERNS = [
    re.compile(r"/products/[a-zA-Z0-9\-]+$", re.IGNORECASE),
    re.compile(r"/p-mp[0-9]{8,}", re.IGNORECASE),
    re.compile(r"/p/[a-zA-Z0-9\-]+$", re.IGNORECASE),
    re.compile(r"/collections/.*/products/[a-zA-Z0-9\-]+$", re.IGNORECASE),
    re.compile(r"/products/[a-zA-Z0-9\-]+-[0-9]+$", re.IGNORECASE),
]

EXCLUDED_DOMAINS = ["play.google.com", "onetrust.com", "facebook.com", "instagram.com"]

# -------------------- Utility Functions --------------------
def is_product_url(url):
    return any(pattern.search(url) for pattern in PRODUCT_PATTERNS)

def should_exclude(url):
    return any(domain in url for domain in EXCLUDED_DOMAINS)

def normalize_url(base, link):
    return urljoin(base, link)

# -------------------- Crawler Logic --------------------
async def crawl_site(domain):
    product_links = set()
    visited = set()

    try:
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)          
            context = await browser.new_context()
            page = await context.new_page()

            logger.info(f"Visiting {domain}")
            try:
                await page.goto(domain, timeout=30000, wait_until="domcontentloaded")
            except Exception as e:
                logger.warning(f"❌ Failed to load {domain}: {e}")
                await browser.close()
                return []

            for _ in range(5):
                await page.mouse.wheel(0, 3000)
                await page.wait_for_timeout(2000)

            anchors = await page.query_selector_all("a")
            extra_links = []
            for a in anchors:
                href = await a.get_attribute("href")
                if href and any(k in href for k in ["/collections/", "/category/", "/men", "/women"]):
                    extra_links.append(href)

            for path in extra_links[:3]:
                if not path:
                    continue
                full_path = normalize_url(domain, path)
                try:
                    logger.info(f"🔁 Navigating deeper: {full_path}")
                    await page.goto(full_path, timeout=20000, wait_until="domcontentloaded")
                    await page.wait_for_timeout(3000)
                except Exception as e:
                    logger.warning(f"❌ Failed navigating to {full_path}: {e}")
                    continue

                for _ in range(3):
                    await page.mouse.wheel(0, 3000)
                    await page.wait_for_timeout(1500)

                sub_anchors = await page.query_selector_all("a")
                for anchor in sub_anchors:
                    href = await anchor.get_attribute("href")
                    if not href:
                        continue
                    full_url = normalize_url(domain, href).split("?")[0]
                    if full_url in visited or should_exclude(full_url):
                        continue
                    visited.add(full_url)
                    if is_product_url(full_url):
                        logger.info(f"✅ Found product: {full_url}")
                        product_links.add(full_url)

                if "tatacliq.com" in domain:
                    clickable_divs = await page.query_selector_all("div[onclick]")
                    for div in clickable_divs:
                        onclick_value = await div.get_attribute("onclick")
                        if onclick_value and "location.href='" in onclick_value:
                            match = re.search(r"location\.href='(.*?)'", onclick_value)
                            if match:
                                raw_url = match.group(1)
                                full_url = normalize_url(domain, raw_url).split("?")[0]
                                if full_url in visited or should_exclude(full_url):
                                    continue
                                visited.add(full_url)
                                if is_product_url(full_url):
                                    logger.info(f"✅ Found product (onclick): {full_url}")
                                    product_links.add(full_url)

            await browser.close()

    except Exception as e:
        logger.error(f"❌ Unexpected error with domain {domain}: {e}")

    return list(product_links)

# -------------------- Main Function --------------------
async def main():
    all_products = defaultdict(list)

    tasks = [
        asyncio.wait_for(crawl_site(domain), timeout=120)
        for domain in DOMAINS
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for domain, links in zip(DOMAINS, results):
        if isinstance(links, Exception):
            logger.error(f"⚠️ Error crawling {domain}: {links}")
            continue
        all_products[domain] = links

    with open("product_urls_output.txt", "w", encoding="utf-8") as f:
        for domain, urls in all_products.items():
            f.write(f"Domain: {domain}\n")
            for url in urls:
                f.write(f"  {url}\n")
            f.write("\n")

    with open("product_urls_output.json", "w", encoding="utf-8") as jf:
        json.dump(all_products, jf, indent=2)

    logger.info("✅ Done! Product URLs saved to 'product_urls_output.txt' and '.json'")

if __name__ == "__main__":
    asyncio.run(main())

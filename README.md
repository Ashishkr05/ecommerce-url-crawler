# 🕷️ E-Commerce Product URL Crawler

This project implements a **scalable**, **robust**, and **asynchronous web crawler** built using **Python** and **Playwright**. The primary goal is to discover and extract all valid **product URLs** from major e-commerce platforms.

---

## 📦 Features

- ✅ Intelligent product URL detection using multiple regex patterns.
- 🚀 Asynchronous crawling with Playwright for high performance.
- 🔁 Auto-scroll and deep-link navigation for lazy-loaded content.
- 🧱 Robust handling of diverse site structures and edge cases.
- 📤 Outputs clean, unique, and structured product URLs in `.txt` and `.json`.

---

## 🛍️ Supported Domains

The crawler currently supports (but is not limited to):

- [Virgio](https://www.virgio.com/)
- [TataCliq](https://www.tatacliq.com/)
- [Nykaa Fashion](https://www.nykaafashion.com/)
- [Westside](https://www.westside.com/)

More domains can be easily added by extending the `DOMAINS` list and/or updating regex patterns.

---

## 🧠 Approach & Logic

### 1️⃣ URL Discovery Strategy

Each domain has different structures for product URLs. We use multiple **regular expressions** to detect product pages accurately:

```python
PRODUCT_PATTERNS = [
  re.compile(r"/products/[a-zA-Z0-9\-]+$"),                     # Virgio, Westside
  re.compile(r"/p-mp[0-9]{8,}"),                                # TataCliq
  re.compile(r"/p/[a-zA-Z0-9\-]+$"),                            # Nykaa
  re.compile(r"/collections/.*/products/[a-zA-Z0-9\-]+$"),      # Shopify variants
  re.compile(r"/products/[a-zA-Z0-9\-]+-[0-9]+$"),              # Additional formats
]

# 🕷️ E-Commerce Product URL Crawler

This project implements a **scalable**, **robust**, and **asynchronous web crawler** built using **Python**, **Playwright**, and a **Streamlit UI**. The goal is to efficiently discover and extract all valid **product URLs** from leading fashion e-commerce platforms.

---

## 📦 Features

- ✅ Intelligent product URL detection using multiple regex patterns
- 🚀 Asynchronous crawling with Playwright for high performance
- 🔁 Auto-scroll and deep-link navigation for lazy-loaded content
- 🧱 Robust error handling and domain-specific crawling strategies
- 🖥️ Interactive **Streamlit Web UI** to crawl by entering supported domain URLs
- 📤 Outputs clean, unique, and structured product URLs in both `.txt` and `.json` format

---

## 🛍️ Supported Domains

This version supports the following:

- [Virgio](https://www.virgio.com/)
- [TataCliq](https://www.tatacliq.com/)
- [Nykaa Fashion](https://www.nykaafashion.com/)
- [Westside](https://www.westside.com/)

⚠️ *Crawler is domain-specific. Only enter one of the above domains in the UI to crawl product URLs.*

---

## 🧠 Approach & Logic

### 1️⃣ URL Discovery Strategy

Each domain uses unique patterns for product pages. The crawler applies multiple **regular expressions** to detect and validate URLs:

```python
PRODUCT_PATTERNS = [
  re.compile(r"/products/[a-zA-Z0-9\-]+$"),                     # Virgio, Westside
  re.compile(r"/p-mp[0-9]{8,}"),                                # TataCliq
  re.compile(r"/p/[a-zA-Z0-9\-]+$"),                            # Nykaa
  re.compile(r"/collections/.*/products/[a-zA-Z0-9\-]+$"),      # Shopify variants
  re.compile(r"/products/[a-zA-Z0-9\-]+-[0-9]+$"),              # Additional formats
]
```

### 2️⃣ Crawling Strategy

- Starts at homepage of the domain
- Scrolls multiple times to trigger lazy-loaded products
- Follows up to 3 internal deep-links based on `href` patterns
- Extracts and filters all valid product URLs

---

## 🖥️ Streamlit UI

- Users can launch `streamlit_app.py`
- Enter a **supported domain** from the list
- View product URLs directly in the browser

![Screenshot 2025-05-10 123855](https://github.com/user-attachments/assets/68dc392d-5cc6-47e9-87ae-27aa9831c01d)
---

## 🛠️ Project Structure

```bash
📁 ecommerce-crawler
├── crawler_playwright.py        # Core async crawler logic
├── streamlit_app.py             # Frontend UI using Streamlit
├── product_urls_output.txt      # Output in plain text format
├── product_urls_output.json     # Output in JSON format
└── requirements.txt             # Python dependencies
```

---

## 🌱 Future Scalability

- 🔌 Add support for more e-commerce platforms via regex & scroll-depth tuning
- 🌐 Deploy UI and backend to cloud (Render, EC2, Docker, etc.)
- 📈 Performance tuning using concurrency & page prefetching
- 📊 Real-time dashboard with crawl stats & URL classification
- 🧪 Automated testing & health-checks for each domain crawl

---

## 📎 How to Run

```bash
# Backend Only
python crawler_playwright.py

# Streamlit UI
streamlit run streamlit_app.py
```

---

## 🚫 Deployment Limitation

> **Note:** Due to the use of **Playwright**, free-tier hosting platforms (like Render, Vercel, etc.) do not support headless browser environments without paid plans.  
> To preserve **performance optimization** and **future scalability**, we’ve chosen not to compromise by switching to a lighter alternative.  
> As a result, the current version is not deployed online and needs to be run locally.

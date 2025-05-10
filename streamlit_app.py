import streamlit as st
import asyncio
import sys

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from crawler_playwright import crawl_site

st.title("🕷️ E-commerce Product Crawler")

st.markdown("**Enter an E-commerce Domain (Choose from one of the 4 supported):**")
st.code("""
https://www.virgio.com/
https://www.tatacliq.com/
https://www.nykaafashion.com/
https://www.westside.com/
""")

domain = st.text_input("Domain URL")

if st.button("Crawl"):
    async def run_crawler():
        return await crawl_site(domain)

    with st.spinner("Crawling..."):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(run_crawler())
            if results:
                st.success(f"✅ Found {len(results)} product URLs:")
                for url in results:
                    st.write(url)
            else:
                st.warning("⚠️ No product URLs found. Please ensure the domain is correct and supported.")
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

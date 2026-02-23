import asyncio
import random
import pandas as pd
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

class JianshuScraper:
    def __init__(self, target_url, output_csv="jianshu_articles_data.csv"):
        self.target_url = target_url
        self.output_csv = output_csv
        self.articles = []

    async def load_all_articles(self, page):
        """Clicks 'Load More' until all articles are loaded."""
        print("Starting pagination...")
        while True:
            # Scroll to bottom to ensure button is in view (sometimes helps)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)

            # Check for Load More button
            # Confirmed selector: #load-more-btn
            load_more = await page.query_selector("#load-more-btn")
            
            if load_more:
                if await load_more.is_visible():
                    print("Clicking 'Load More'...")
                    await load_more.click()
                    # Wait for new content.
                    await page.wait_for_timeout(random.randint(1500, 3000))
                else:
                    print("Load more button found but not visible.")
                    break
            else:
                print("No 'Load More' button found. All articles loaded.")
                break

    async def get_article_details(self, browser, article_url):
        """Visits article page to get Notebook (Column) name and potentially other stats."""
        page = await browser.new_page()
        details = {
            "Column Name": "Uncategorized",
            "Bookmark Count": "0" 
        }
        try:
            await page.goto(article_url, wait_until='domcontentloaded')
            await page.wait_for_timeout(random.randint(1000, 2000))

            # Notebook/Column Name extraction
            # Verified Selector: a[href*='/nb/'] span or just the text of a link with /nb/
            
            try:
                # Wait for potential element
                await page.wait_for_selector('a[href*="/nb/"]', timeout=3000)
                notebook_el = await page.query_selector("a[href*='/nb/']")
                if notebook_el:
                     details["Column Name"] = await notebook_el.inner_text()
            except:
                pass 

            # Bookmark/Fav Count
            # Still using 0 as default if not found
            
        except Exception as e:
            print(f"Error visiting {article_url}: {e}")
        finally:
            await page.close()
        
        return details

    async def run(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            page = await context.new_page()

            print(f"Navigating to {self.target_url}")
            await page.goto(self.target_url, timeout=60000)
            
            # Load all
            await self.load_all_articles(page)

            # Parse content
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Process articles
            # Jianshu list items are usually <li> in .note-list
            items = soup.select('ul.note-list li')
            print(f"Found {len(items)} articles. Processing...")

            for item in items:
                try:
                    # Title
                    title_tag = item.select_one('a.title')
                    title = title_tag.get_text(strip=True) if title_tag else "N/A"
                    
                    # URL
                    url_suffix = title_tag['href'] if title_tag else ""
                    if url_suffix.startswith("/"):
                        url = f"https://www.jianshu.com{url_suffix}"
                    else:
                        url = url_suffix # Should be full url or handled

                    # Meta info (Date, Views, Likes, Comments)
                    # Date: span.time
                    date_tag = item.select_one('span.time')
                    if date_tag and date_tag.has_attr('data-shared-at'):
                        date = date_tag['data-shared-at'].split('T')[0] # ISO format
                    elif date_tag:
                         date = date_tag.get_text(strip=True)
                    else:
                        date = "N/A"
                    
                    # Stats are usually in .meta
                    # View: in a tag with target="_blank" usually, or check icon class
                    # View: .ic-list-read
                    # Comment: .ic-list-comments
                    # Like: .ic-list-like
                    
                    view_count = "0"
                    comment_count = "0"
                    like_count = "0"
                    
                    meta_div = item.select_one('div.meta')
                    if meta_div:
                        # Helper to find text next to icon
                        def get_stat(icon_class):
                            icon = meta_div.select_one(f'i.{icon_class}')
                            if icon and icon.parent:
                                return icon.parent.get_text(strip=True)
                            return "0"

                        view_count = get_stat('ic-list-read')
                        comment_count = get_stat('ic-list-comments')
                        like_count = get_stat('ic-list-like')
                        
                    self.articles.append({
                        "Title": title,
                        "Publish Date": date,
                        "View Count": view_count,
                        "Like Count": like_count,
                        "Comment Count": comment_count,
                        "Bookmark Count": "N/A", # Will update in details
                        "Article URL": url,
                        "Column Name": "Pending"
                    })

                except Exception as e:
                    print(f"Error parsing item: {e}")

            # Visit details
            total_articles = len(self.articles)
            print(f"Fetching details (Notebook name, etc.) from individual pages... Total: {total_articles}")
            
            for i, article in enumerate(self.articles):
                # Progress Countdown
                # Total {total} - Processed {current} = Remaining {remaining}
                # Print every 5 articles or for the first one
                if (i + 1) % 5 == 0 or i == 0:
                    processed = i
                    remaining = total_articles - processed
                    print(f"Fetching details: Total {total_articles} - Processed {processed} = Remaining {remaining}")

                if article['Article URL'] != "N/A":
                    details = await self.get_article_details(browser, article['Article URL'])
                    article['Column Name'] = details['Column Name']
                    if details['Bookmark Count'] != "0":
                         article['Bookmark Count'] = details['Bookmark Count']
                    else:
                        # Fallback if not found, use like count or 0
                        article['Bookmark Count'] = "0" 

            print(f"Fetching details completed. Processed all {total_articles} articles.")
            await browser.close()

    def save_csv(self):
        df = pd.DataFrame(self.articles)
        # Sort by Date
        df['Publish Date'] = pd.to_datetime(df['Publish Date'], errors='coerce')
        df = df.sort_values(by='Publish Date', ascending=True)
        
        import os
        # Robust path resolution:
        # Script is in scraper_core/, so root is one level up.
        current_dir = os.path.dirname(os.path.abspath(__file__)) # .../web_scraper/scraper_core
        project_root = os.path.dirname(current_dir) # .../web_scraper
        output_dir = os.path.join(project_root, 'scraper_output')
        
        # Ensure directory exists just in case
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        output_path = os.path.join(output_dir, os.path.basename(self.output_csv))
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")

if __name__ == "__main__":
    import json
    import os
    
    # Load config from root directory
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            jianshu_config = config.get('platforms', {}).get('jianshu', {})
            
            target_url = jianshu_config.get('url', "https://www.jianshu.com/u/d614825bc8a1")
            output_csv = jianshu_config.get('output_csv', "scraper_output/jianshu_articles_data.csv")
    except Exception as e:
        print(f"Failed to load config.json: {e}. Using defaults.")
        target_url = "https://www.jianshu.com/u/d614825bc8a1"
        output_csv = "scraper_output/jianshu_articles_data.csv"

    scraper = JianshuScraper(target_url, output_csv)
    asyncio.run(scraper.run())
    scraper.save_csv()

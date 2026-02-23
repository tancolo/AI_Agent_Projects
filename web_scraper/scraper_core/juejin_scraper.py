import asyncio
import random
import pandas as pd
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

class JuejinScraper:
    def __init__(self, target_url, output_csv="juejin_articles_data.csv"):
        self.target_url = target_url
        self.output_csv = output_csv
        self.articles = []

    async def scroll_to_bottom(self, page):
        """Scrolls to the bottom to load all articles."""
        print("Starting infinite scroll...")
        prev_height = -1
        retries = 0
        while retries < 5:
            # Scroll to bottom
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)

            # Check if height changed
            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == prev_height:
                retries += 1
                print(f"Height didn't change ({retries}/5). Waiting...")
                await page.wait_for_timeout(2000)
            else:
                retries = 0
                prev_height = new_height
                
        print("Infinite scroll finished.")

    async def get_article_details(self, browser, article_url):
        """Visits article page to get Column Name and Exact Date."""
        page = await browser.new_page()
        details = {
            "Column Name": "Uncategorized",
            "Exact Date": "N/A",
            "Bookmark Count": "0" 
        }
        try:
            await page.goto(article_url, wait_until='domcontentloaded')
            await page.wait_for_timeout(random.randint(1000, 2000))

            # Ensure header is loaded
            try:
                await page.wait_for_selector(".article-header, .meta-box", timeout=5000)
            except:
                print(f"Header not found for {article_url}")

            # Column Name
            # Selector: .first-column .title
            try:
                column_el = await page.query_selector(".first-column .title") 
                if column_el:
                    details["Column Name"] = await column_el.inner_text()
                else:
                    # Fallback
                    tag_el = await page.query_selector("a.tag-link")
                    if tag_el:
                        details["Column Name"] = await tag_el.inner_text()
            except Exception as e:
                print(f"Column extraction error: {e}")

            # Exact Date
            # Selector: time.time
            try:
                await page.wait_for_selector("time.time", timeout=3000)
                time_el = await page.query_selector("time.time")
                if time_el:
                    details["Exact Date"] = await time_el.inner_text()
            except Exception as e:
                print(f"Date extraction error: {e}")

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
            
            # Scroll
            await self.scroll_to_bottom(page)

            # Parse content
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Select Items
            # Use direct child selector to avoid picking up nested .item elements (like stats)
            items = soup.select('.entry-list > .item')
            if not items:
                items = soup.select('.entry-list > li.item')
            
            print(f"Found {len(items)} articles. Processing...")

            for i, item in enumerate(items):
                try:
                    # Title
                    title_tag = item.select_one('a.title')
                    if not title_tag: 
                        # Debug: Print why skipped (should be rare with better selector)
                        print(f"Skipping item {i}: No title tag found.")
                        continue
                    
                    title = title_tag.get_text(strip=True)
                    url_suffix = title_tag['href']
                    if url_suffix.startswith("/"):
                        url = f"https://juejin.cn{url_suffix}"
                    else:
                        url = url_suffix

                    # Meta Row (Date, Views, etc)
                    # Date from list is relative, will override with exact date from details
                    date = "Pending" 
                    
                    view_count = "0"
                    like_count = "0"
                    comment_count = "0"
                    
                    # Stats
                    # Views: .view
                    # Likes: .like
                    # Comments: .comment
                    
                    # Need to be careful with selectors, Juejin changes classes.
                    # Helper to find text in action list
                    # Structure: ul.action-list > li.item.view, li.item.like, li.item.comment
                    action_list = item.select_one('ul.action-list')
                    if action_list:
                        for action in action_list.select('li.item'):
                            text = action.get_text(strip=True)
                            if not text: continue
                            
                            classes = action.get('class', [])
                            
                            if 'view' in classes:
                                view_count = text
                            elif 'like' in classes:
                                like_count = text
                            elif 'comment' in classes:
                                comment_count = text

                    self.articles.append({
                        "Title": title,
                        "Publish Date": date, # Might need cleaning "1年前"
                        "View Count": view_count,
                        "Like Count": like_count,
                        "Comment Count": comment_count,
                        "Bookmark Count": "0", 
                        "Article URL": url,
                        "Column Name": "Pending"
                    })

                except Exception as e:
                    print(f"Error parsing item {i}: {e}")

            # Details
            total_articles = len(self.articles)
            print(f"Fetching details... Total: {total_articles}")
            
            for i, article in enumerate(self.articles):
                # Progress Countdown
                if (i + 1) % 5 == 0 or i == 0:
                    processed = i
                    remaining = total_articles - processed
                    print(f"Fetching details: Total {total_articles} - Processed {processed} = Remaining {remaining}")

                if article['Article URL'] != "N/A":
                    details = await self.get_article_details(browser, article['Article URL'])
                    article['Column Name'] = details['Column Name']
                    if details['Exact Date'] != "N/A":
                         article['Publish Date'] = details['Exact Date']

            print(f"Fetching details completed. Processed all {total_articles} articles.")
            await browser.close()

    def save_csv(self):
        df = pd.DataFrame(self.articles)
        # Sort not possible accurately if date is "1 year ago" without conversion
        # Will save as is.
        import os
        # Robust path resolution
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        output_dir = os.path.join(project_root, 'scraper_output')
        
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
            juejin_config = config.get('platforms', {}).get('juejin', {})
            
            target_url = juejin_config.get('url', "https://juejin.cn/user/345669300651932/posts")
            output_csv = juejin_config.get('output_csv', "scraper_output/juejin_articles_data.csv")
    except Exception as e:
        print(f"Failed to load config.json: {e}. Using defaults.")
        target_url = "https://juejin.cn/user/345669300651932/posts"
        output_csv = "scraper_output/juejin_articles_data.csv"

    scraper = JuejinScraper(target_url, output_csv)
    asyncio.run(scraper.run())
    scraper.save_csv()

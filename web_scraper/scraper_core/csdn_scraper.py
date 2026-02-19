import asyncio
import random
import pandas as pd
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

class CSDNScraper:
    def __init__(self, target_url):
        self.target_url = target_url
        self.articles = []

    async def scroll_to_bottom(self, page):
        """Scrolls to the bottom of the page to load all articles."""
        print("Starting infinite scroll...")
        prev_height = -1
        retries = 0
        while retries < 5: # Try up to 5 times if height doesn't change
            # Scroll to bottom
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000) # Base delay

            # Check if height changed
            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == prev_height:
                retries += 1
                print(f"Height didn't change ({retries}/5). Waiting...")
                await page.wait_for_timeout(2000)
            else:
                retries = 0 # Reset retries if we successfully loaded more
                prev_height = new_height
                # Optional: scroll up a bit to trigger lazy loaders
                await page.evaluate("window.scrollBy(0, -100)")
                await page.wait_for_timeout(500)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        print("Infinite scroll finished.")

    async def get_article_details(self, browser, article_url):
        """Visits article page to get Column/Series name."""
        page = await browser.new_page()
        column_name = None
        try:
            await page.goto(article_url, wait_until='domcontentloaded') # Faster than networkidle
            # Try to find column name
            # Selectors vary, common ones: .tag-link, .column-link, #blog_detail_zk_collection
            # Based on inspection of CSDN usually column is in a specific box or tag
            
            # Wrapper for safety
            try:
                # Wait for potential column element
                await page.wait_for_selector('a.item-target, .tag-link', timeout=3000)
            except:
                pass # Proceed anyway if not found

            # Strategy: look for element with specific class or text
            # Verified selector: a.item-target which contains the column title
            column_element = await page.query_selector('a.item-target')
            
            if column_element:
                # Get title attribute or text
                title_attr = await column_element.get_attribute('title')
                if title_attr:
                    column_name = title_attr
                else:
                    column_name = await column_element.inner_text()
            else:
                # Fallback
                column_element = await page.query_selector('.tag-link')
                if column_element:
                     column_name = await column_element.inner_text()
            
            # Add random delay
            await page.wait_for_timeout(random.randint(500, 1000))

        except Exception as e:
            print(f"Error visiting {article_url}: {e}")
        finally:
            await page.close()
        
        return column_name

    async def run(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False) # Headless False for visibility and safety
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            page = await context.new_page()

            print(f"Navigating to {self.target_url}")
            await page.goto(self.target_url)
            
            # Handle infinite scroll
            await self.scroll_to_bottom(page)

            # Parse content
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Select all article items
            # Initial analysis in browser subagent found 'article.blog-list-box'
            article_items = soup.select('article.blog-list-box')
            print(f"Found {len(article_items)} articles. Processing...")

            for item in article_items:
                try:
                    # Title
                    title_tag = item.select_one('h4')
                    title = title_tag.get_text(strip=True) if title_tag else "N/A"
                    
                    # URL
                    url_tag = item.select_one('a')
                    url = url_tag['href'] if url_tag else "N/A"

                    # Stats (View, Like, Comment, etc are in .blog-list-footer-left)
                    footer = item.select_one('.blog-list-footer-left')
                    
                    date = "N/A"
                    view_count = "0"
                    like_count = "0"
                    comment_count = "0"
                    bookmark_count = "0" # 'Fav' or 'Collect'
                    
                    if footer:
                        # Text parsing might be needed as classes aren't always unique per stat
                        # But typically: properties are in spans or divs
                        # CSDN strict format: "Unknown" | Date | Views | ...
                        
                        # Let's rely on finding specific text or classes if known
                        # From browser agent:
                        # Date: "发布博客 YYYY.MM.DD" or similar
                        text = footer.get_text()
                        
                        import re
                        # Extract Date
                        date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', text)
                        if date_match:
                            date = date_match.group(1)
                        
                        # Extract Views "123 阅读"
                        view_match = re.search(r'(\d+)\s*阅读', text)
                        if view_match:
                            view_count = view_match.group(1)
                            
                        # Extract Likes "123 点赞"
                        like_match = re.search(r'(\d+)\s*点赞', text)
                        if like_match:
                            like_count = like_match.group(1)

                        # Extract Comments "123 评论"
                        comment_match = re.search(r'(\d+)\s*评论', text)
                        if comment_match:
                            comment_count = comment_match.group(1)
                        
                        # Extract Bookmarks "123 收藏"
                        bookmark_match = re.search(r'(\d+)\s*收藏', text)
                        if bookmark_match:
                            bookmark_count = bookmark_match.group(1)

                    # Get Column Name (requires visiting page)
                    # To save time, we can collect all basic info first then update column
                    # But verifying 'ALL' fields now.
                    # Note: Visiting 59 pages might take time.
                    
                    self.articles.append({
                        "Title": title,
                        "Publish Date": date,
                        "View Count": view_count,
                        "Like Count": like_count,
                        "Comment Count": comment_count,
                        "Bookmark Count": bookmark_count,
                        "Article URL": url,
                        "Column Name": "Pending" 
                    })
                except Exception as e:
                    print(f"Error parsing item: {e}")

            # Now visit each article to get column name
            # We can use the same context
            total_articles = len(self.articles)
            print(f"Fetching column names from individual pages... Total: {total_articles}")
            
            for i, article in enumerate(self.articles):
                # Progress Countdown
                if (i + 1) % 5 == 0 or i == 0:
                    processed = i
                    remaining = total_articles - processed
                    print(f"Fetching details: Total {total_articles} - Processed {processed} = Remaining {remaining}")

                if article['Article URL'] != "N/A":
                    # print(f"Checking details for: {article['Title']}")
                    col_name = await self.get_article_details(browser, article['Article URL'])
                    article['Column Name'] = col_name if col_name else "Uncategorized"

            print(f"Fetching details completed. Processed all {total_articles} articles.")
            await browser.close()

    def save_csv(self):
        df = pd.DataFrame(self.articles)
        # Sort by Date
        # Convert date to datetime
        df['Publish Date'] = pd.to_datetime(df['Publish Date'], format='%Y.%m.%d', errors='coerce')
        df = df.sort_values(by='Publish Date', ascending=True) # Oldest to Newest
        
        import os
        # Robust path resolution
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        output_dir = os.path.join(project_root, 'scraper_output')
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        output_path = os.path.join(output_dir, 'csdn_articles_data.csv')
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")

if __name__ == "__main__":
    scraper = CSDNScraper("https://blog.csdn.net/shrimpcolo?type=blog")
    asyncio.run(scraper.run())
    scraper.save_csv()

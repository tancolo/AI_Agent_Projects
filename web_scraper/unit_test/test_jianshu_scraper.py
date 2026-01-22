import unittest
import sys
import os
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
import pandas as pd

# Add parent directory to path to allow importing jianshu_scraper
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jianshu_scraper import JianshuScraper

class TestJianshuScraper(unittest.TestCase):
    def setUp(self):
        self.target_url = "https://www.jianshu.com/u/d614825bc8a1"
        self.scraper = JianshuScraper(self.target_url)

    def test_init(self):
        self.assertEqual(self.scraper.target_url, self.target_url)
        self.assertEqual(self.scraper.articles, [])

    @patch('jianshu_scraper.pd')
    def test_save_csv(self, mock_pd):
        # Setup dummy data
        self.scraper.articles = [
            {
                "Title": "Test Article",
                "Publish Date": "2023-01-01",
                "View Count": "100",
                "Like Count": "10",
                "Comment Count": "1",
                "Bookmark Count": "0",
                "Article URL": "http://test.com",
                "Column Name": "Test Column"
            }
        ]

        # Mock DataFrame
        mock_df = MagicMock()
        mock_pd.DataFrame.return_value = mock_df
        # Ensure sort_values returns the same mock_df so we can check to_csv on it
        mock_df.sort_values.return_value = mock_df
        
        # Call the method
        self.scraper.save_csv()

        # Assertions
        mock_pd.DataFrame.assert_called_once_with(self.scraper.articles)
        mock_df.sort_values.assert_called()
        mock_df.to_csv.assert_called_with('jianshu_articles_data.csv', index=False)

class TestJianshuScraperAsync(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.target_url = "https://www.jianshu.com/u/d614825bc8a1"
        self.scraper = JianshuScraper(self.target_url)

    async def test_get_article_details(self):
        # Mock browser and page
        mock_browser = AsyncMock()
        mock_page = AsyncMock()
        mock_browser.new_page.return_value = mock_page
        
        # Mock element for notebook/column name
        mock_element = AsyncMock()
        mock_element.inner_text.return_value = "My Notebook"
        mock_page.query_selector.return_value = mock_element

        # Call the method
        details = await self.scraper.get_article_details(mock_browser, "http://test.com/article/1")

        # Assertions
        self.assertEqual(details["Column Name"], "My Notebook")
        self.assertEqual(details["Bookmark Count"], "0") # Default mock behavior
        
        mock_browser.new_page.assert_called_once()
        mock_page.goto.assert_called_with("http://test.com/article/1", wait_until='domcontentloaded')
        mock_page.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()

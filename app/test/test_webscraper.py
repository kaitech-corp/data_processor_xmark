import unittest

from app.scraper.scraper_v2 import WebScraper





class TestWebScraper(unittest.TestCase):

    location = 'us-central1'
    project_number = '247644706560'

    def setUp(self):
        self.scraper = WebScraper(self.project_number, self.location)

    def test_scrape_website(self):

        # Define test data
        url = 'https://medium.com/@blendvisions?source=user_profile-------------------------------------'
        keywords = ["we", "will", "explore", "the", "core", "user", "and"]

        # Run the method under test
        title, content = self.scraper.scrape_website(url=url,keywords=keywords)

        # Define test data result
        testTitle = "Blend Visions – Medium"
        testContent = """1 day ago React JS Hooks: The Latest and Greatest in React State Management React JS Hooks are a new way to manage state in React. They’re easier to use than traditional state management methods, and they can help you to write more modular and reusable code. In this blog article, we’ll take a look at what React JS Hooks are and how to use them. Introducing React 18: What's New? - Blend Visions\nExplore the powerful features of React 18, the latest version of the popular Java Script library for creating user…blendvisions.me React3 min read React3 min read"""
        
        # Assertions
        self.assertEqual(title, testTitle)
        self.assertEqual(content, testContent)


    def test_scrape_website_error(self):

        # Define test data
        url = "https://example.com"
        keywords = ["keyword1", "keyword2"]

        # Run the method under test
        title, content = self.scraper.scrape_website(url, keywords)

        # Assertions
        self.assertIsNone(title)
        self.assertIsNone(content)

if __name__ == '__main__':
    unittest.main()

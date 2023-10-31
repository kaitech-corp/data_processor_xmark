import unittest

from app.scraper.scraper_v2 import WebScraper






class TestWebScraper(unittest.TestCase):

    location = 'us-central1'
    project_number = '247644706560'

    def setUp(self):
        self.scraper = WebScraper(self.project_number, self.location)

    def test_read_text_file(self):
        # Create a test file with sample data
        with open('test_tag_words.txt', 'w') as test_file:
            test_file.write("tag1\ntag2\ntag3")

        result = self.scraper.read_text_file('test_tag_words.txt')
        self.assertEqual(result, ["tag1", "tag2", "tag3"])

    def test_tag_word_file_count(self):
        # Open Tag word file 
        with open('app/resources/tag_words.txt', 'r') as test_file:
            lines = [line.strip() for line in test_file.readlines()]
            self.assertEqual(len(lines), 299)        

    def test_remove_unwanted_characters(self):
        text = "This is \\some example text \\with backslashes."
        result = self.scraper.remove_unwanted_characters(text)
        self.assertEqual(result, "This is  example text  backslashes.")
        
    def test_split_combined_words(self):
        text = "This is someExample textWith combined words."
        result = self.scraper.split_combined_words(text)
        self.assertEqual(result, "This is some Example text With combined words.")

    def test_isValidUrl(self):
        url = "https://python.langchain.com/docs/get_started/introduction"
        result = self.scraper.isValidUrl(url)
        self.assertEqual(result, True)

    def test_isValidUrlFalse(self):
        url = "https://not a real site.com"
        result = self.scraper.isValidUrl(url)
        self.assertEqual(result, False)

if __name__ == '__main__':
    unittest.main()

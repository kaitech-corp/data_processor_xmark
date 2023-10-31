import datetime
import json
import os
import re
import requests
import uuid
from bs4 import BeautifulSoup
import dateutil.parser as dparser
from vertexai.preview.language_models import TextGenerationModel
import vertexai
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError

class WebScraper:
    def __init__(self, project_number, location):
        vertexai.init(project=project_number, location=location)
        
    def read_text_file(self, file_path='resources/tag_words.txt'):
        try:
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file.readlines()]
                return lines
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []

    def remove_unwanted_characters(self, text):
        pattern = r'\\[a-zA-Z0-9]+'
        return re.sub(pattern, '', text)

    def split_combined_words(self, text):
        pattern = r'([a-z])([A-Z])'
        return re.sub(pattern, r'\1 \2', text)

    def isValidUrl(self, url):
        try:
            response = requests.get(url)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def scrape_website(self, url, keywords):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string
            content = soup.find("article")
            if content:
                content = content.get_text(strip=True)
                cleaned_content = self.split_combined_words(self.remove_unwanted_characters(content))
                keyword_count = 0

                for keyword in keywords:
                    if keyword.lower() in cleaned_content.lower():
                        keyword_count += 1
                        if keyword_count >= 5:
                            return title, cleaned_content

            return None, None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None, None

    def scrape_posted_date(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                date_elements = soup.find_all(['time', 'span', 'div', 'p'], {'data-testid': ['ri hg l', 'storyPublishDate']})
                date_text = " ".join(element.get_text() for element in date_elements)
                parsed_date = dparser.parse(date_text, fuzzy=True)

                if parsed_date:
                    return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    return "Date not found"
            else:
                return "Date not found"
        except Exception as e:
            return str(e)

    def create_json(self, title, content, tags, url, date_posted):
        json_obj = {
            'title': title,
            'content': content,
            'tags': tags,
            'date_created': str(datetime.datetime.now()),
            'date_posted': str(date_posted),
            'url': url
        }
        return json.dumps(json_obj)

    def process(self, element):

        """
        This function processes the given element.

        Args:
            element (str): The URL of the website to be processed.

        Returns:
            str: Status of the processed element.
        """
        try:
            if self.isValidUrl(element):
                keywords = self.read_text_file()
                title, content = self.scrape_website(element, keywords)
                if title and content and len(content) > 750:
                    date_posted = self.scrape_posted_date(element)
                    tag_prompt = f'Generate 10 one word tags in comma separated format all related to the following content: {content}'
                    tags = prompt_model(tag_prompt)
                    json_element = self.create_json(title=title, content=content, tags=tags, url=element, date_posted=date_posted)
                    self.write_to_gcs(json_element)
                    return 'Completed'
                return 'Website did not pass checks.'
            return 'Did not process'
        except Exception as e:
            # Handle other exceptions
            return f"Error: {e}"
        

    def write_to_gcs(self, element):
            try:
                # Initialize the Google Cloud Storage client
                storage_client = storage.Client()

                folder_name = os.environ.get("GSCFOLDERNAME")
                bucket_name = os.environ.get("BUCKETNAME")
                bucket = storage_client.get_bucket(bucket_name)

                # Upload the JSON string to the specified location in the bucket
                id_str = str(uuid.uuid4())
                # print(id_str)
                blob = bucket.blob(f"{folder_name}/{id_str}.json")
                blob.upload_from_string(element)

                print(
                    f"File {id_str} uploaded to {bucket_name}/{folder_name}")
            except GoogleCloudError as e:
                # Handle Google Cloud Storage-related errors
                print(f"Google Cloud Storage Error: {e}")
            except Exception as e:
                # Handle other exceptions
                print(f"Error: {e}")
        
def prompt_model( prompt: str):
    parameters = {
        "max_output_tokens": 1024,
        "temperature": 0.3,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")
    try:
        response = model.predict(prompt, **parameters)
        return response.text
    except:
        return "error"

class TransformFn():
    def __init__(self):
        location = os.environ.get("LOCATION")
        project_number = os.environ.get("PROJECTNUMBER")
        vertexai.init(project=project_number, location=location)
        self.scraper = WebScraper(project_number, location)

    def process(self, element):
        return self.scraper.process(element)


                                                 

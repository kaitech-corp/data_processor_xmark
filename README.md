# Cloud Run Data Processing Application

This Cloud Run application serves as a data processor for web scraping tasks. When provided with a URL, the application performs the following key tasks:

1. **URL Validation**: It verifies the validity of the provided URL.

2. **Web Scraping**: The application scrapes the target website to extract its content.

3. **Tag Generation**: It generates tags associated with the scraped content.

4. **JSON Format Creation**: The data is structured into a JSON format, including the following fields:
   - Title
   - Content
   - Tags
   - Date Created
   - Date Posted
   - URL

5. **Google Cloud Storage**: The resulting JSON file is saved to Google Cloud Storage for storage and further processing.

This Cloud Run application is designed to be triggered by PubSub, meaning URLs are passed to this function via PubSub messages, enabling seamless integration into your data processing workflows.
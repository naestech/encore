import requests
from bs4 import BeautifulSoup
import re

def sanitize_filename(url):
    # Remove the protocol (http:// or https://)
    url = re.sub(r'^https?://', '', url)
    # Replace invalid filename characters with underscores
    return re.sub(r'[^\w\-_\. ]', '_', url)

def save_website_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        soup = BeautifulSoup(response.text, 'html.parser')
        html_content = soup.prettify()

        filename = sanitize_filename(url) + '.html'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f"HTML content saved to {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")

if __name__ == "__main__":
    url = input("Enter the website URL: ")
    save_website_html(url)

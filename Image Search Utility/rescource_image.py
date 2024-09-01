import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_image_urls(webpage_url):
    try:
        # Send a GET request to the webpage URL
        response = requests.get(webpage_url)
        response.raise_for_status()  # Raise an exception for bad responses

        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all image tags
        img_tags = soup.find_all('img')

        # Extract the 'src' attribute from each image tag
        image_urls = [urljoin(webpage_url, img['src']) for img in img_tags if 'src' in img.attrs]

        return image_urls

    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
webpage_url = 'https://ssec.si.edu/stemvisions-blog/what-photosynthesis'
image_urls = get_image_urls(webpage_url)

if image_urls:
    for i, url in enumerate(image_urls, 1):
        print(f"Image {i}: {url}")
else:
    print("Failed to retrieve image URLs.")

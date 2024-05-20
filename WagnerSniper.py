import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

def download_images(image_links, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for i, link in enumerate(image_links, start=1):
        filename = os.path.join(output_folder, f"image_{i}.jpg")
        try:
            response = requests.get(link)
            response.raise_for_status()
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Exception occurred while downloading image from {link}: {e}")

def find_photos(url):
    with webdriver.Firefox() as driver:
        driver.get(url)
        driver.implicitly_wait(60)
        html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    jpg_links = [img['src'] for img in soup.find_all('img', src=lambda s: s and s.endswith('.jpg'))]
    return jpg_links

def write_links_to_file(links, filename):
    with open(filename, 'w') as file:
        file.write('\n'.join(links))

url = ''  # Put your URL here
jpg_links = find_photos(url)

for link in jpg_links:
    print('link -> ' + link)

write_links_to_file(jpg_links, 'output.txt')
download_images(jpg_links, 'downloaded_images')

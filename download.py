#!/bin/env python3
"""
Downloads all UK radio station logos from media.info for the in-car
entertainment system in VAG vehicles (eg Discover Media)
"""
import os
from urllib.error import HTTPError
import urllib.request

from bs4 import BeautifulSoup

PAGE_BASE_URL = 'https://media.info/uk/radio/stations/starting-with/'
IMAGE_BASE_URL = 'https://media.info/i/lv/'
OUTPUT_DIR = '/logos'


def download_url(url, filename):
    """Downloads a URL into the specified filename."""
    print(f'Downloading {url} to {filename}')
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response,\
                open(filename, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
    except HTTPError as exception:
        print(f'Download {filename} from {url} failed: {exception}')


def process_page(source, image_base_url, output_dir):
    """Process a page of HTML, extract image locations and station name, and download the image."""
    soup = BeautifulSoup(source, 'html.parser')
    info_links = soup.select('div.info > a')
    for info_link in info_links:
        name = info_link['href'].split('/')[-1]
        images = info_link.findChildren('img', recursive=False)
        if len(images) > 0:
            segments = images[0]['src'].split('/')[slice(4, 6)]
            extension = segments[1].split('.')[1]
            filename = f'{output_dir}/{name}.{extension}'
            url = f'{image_base_url}{name}/{segments[0]}/{segments[1]}'

            download_url(url, filename)
        else:
            print(f'No image for {name}')


def download_a_to_z(page_base_url, image_base_url, output_dir):
    """Retrieve each page of stations from a-z and download logos that are present."""
    for char in range(ord('a'), ord('z')+1):
        page = f'{page_base_url}{chr(char)}'
        source = urllib.request.urlopen(page).read()
        process_page(source, image_base_url, output_dir)
        break


def main():
    """Download all UK radio station logos fro media.info."""
    page_base_url = os.getenv('PAGE_BASE_URL', default=PAGE_BASE_URL)
    image_base_url = os.getenv('IMAGE_BASE_URL', default=IMAGE_BASE_URL)
    output_dir = os.getenv('OUTPUT_DIR', default=OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)
    download_a_to_z(page_base_url, image_base_url, output_dir)


if __name__ == "__main__":
    main()

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spi.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/30 18:40:02 by hubourge          #+#    #+#              #
#    Updated: 2025/05/30 19:47:38 by hubourge         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r",
                        action="store_true",
                        help="Enable recursive download")
    parser.add_argument("-l",
                        type=int,
                        default=5,
                        help="Set maximum depth level (default: 5)")
    parser.add_argument("-p",
                        default="./data/",
                        help="Set output path (default: ./data/)")
    parser.add_argument("url",
                        help="Target URL")

    args = parser.parse_args()

    # Check that level is positive
    if args.l < 0:
        parser.error("Depth level (-l) must be a positive number")

    return args

def extract_images_and_links(url):
    # Validate URL
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return

    if response.status_code != 200:
        print(f"HTTP error {response.status_code} when accessing {url}")
        return

    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract images
    print("\nImages found:")
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            full_url = urljoin(url, src)
            print(" -", full_url)

    # Extract links
    print("\nLinks found:")
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            full_url = urljoin(url, href)
            print(" -", full_url)

def main():
    args = parse_args()

    print(f"Recursive:   {args.r}")
    print(f"Max depth:   {args.l}")
    print(f"Output path: {args.p}")
    print(f"URL:         {args.url}")

    extract_images_and_links(args.url)

if __name__ == "__main__":
    main()

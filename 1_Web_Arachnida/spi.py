# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spi.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/30 18:40:02 by hubourge          #+#    #+#              #
#    Updated: 2025/06/02 18:29:55 by hubourge         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

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
        parser.error("[Input] Depth level (-l) must be a positive number")

    return args

def extract_images_and_links(url, depth, output_path):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            print(f"[Error] HTTP error {response.status_code} when accessing {url}")
            return [], []
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return [], []

    soup = BeautifulSoup(response.text, 'html.parser')

    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    images_printed = False

    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            full_url = urljoin(url, src)
            if full_url.lower().endswith(valid_extensions):
                if not images_printed:
                    print(f"\n{depth} Images from {url}")
                    images_printed = True
                print("  -", full_url)
        try:
            img_data = requests.get(full_url, timeout=5).content
            filename = os.path.basename(urlparse(full_url).path)
            filepath = os.path.join(output_path, filename)
            with open(filepath, 'wb') as f:
                f.write(img_data)
        except Exception as e:
            print(f"[Error] Failed to download {full_url}: {e}")

    links = []
    # print(f"\n{depth} Links from {url}:")
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            full_url = urljoin(url, href)
            # print("  -", full_url)
            links.append(full_url)

    return links

def crawl(url, recursive=False, max_depth=1, output_path="./data/"):
    visited = set()
    to_visit = [(url, 0)]

    while to_visit:
        current_url, depth = to_visit.pop(0)
        if current_url in visited or depth > max_depth:
            continue
        visited.add(current_url)

        links = extract_images_and_links(current_url, depth, output_path)
        if recursive and depth < max_depth:
            for link in links:
                if isinstance(link, str):
                    to_visit.append((link, depth + 1))            

def create_output_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        print(f"[Error] Failed to create output directory '{path}': {e}")
        sys.exit(1)

def main():
    args = parse_args()

    print(f"Recursive:   {args.r}")
    print(f"Max depth:   {args.l}")
    print(f"Output path: {args.p}")
    print(f"URL:         {args.url}")

    create_output_directory(args.p)
    crawl(args.url, args.r, args.l, args.p)

if __name__ == "__main__":
    main()

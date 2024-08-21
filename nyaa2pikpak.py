import asyncio
import json
import httpx
import requests
from bs4 import BeautifulSoup
from pikpakapi import PikPakApi
import os
import schedule
import time

# Set proxy setting
HTTP_PROXY = "http://127.0.0.1:8080"
PROCESSED_LINKS_FILE = "processed_links.txt"

async def get_magnet_links(url):
    response = requests.get(url, proxies={'http': HTTP_PROXY, 'https': HTTP_PROXY})
    soup = BeautifulSoup(response.content, 'html.parser')
    magnet_links = [a['href'] for a in soup.find_all('a', href=lambda href: href and href.startswith('magnet:'))]
    return magnet_links

async def download_magnets(magnet_links, processed_links):
    global client
    if client is None:
        print("Client not initialized. Skipping task.")
        return

    for link in magnet_links:
        if link in processed_links:
            print(f"Skipping already processed link: {link}")
            continue
        try:
            result = await client.offline_download(link)
            print(f"Added to download: {link}")
            print(json.dumps(result, indent=4))
            processed_links.add(link)
            save_processed_links(processed_links)
        except Exception as e:
            print(f"Failed to add {link}: {str(e)}")

def load_processed_links():
    if os.path.exists(PROCESSED_LINKS_FILE):
        with open(PROCESSED_LINKS_FILE, "r") as file:
            return set(file.read().splitlines())
    return set()

def save_processed_links(processed_links):
    with open(PROCESSED_LINKS_FILE, "w") as file:
        for link in processed_links:
            file.write(f"{link}\n")

async def main_task():
    global client
    if client is None:
        print("Client not initialized. Skipping task.")
        return
    
    base_url = "https://nyaa.si/?c=2_2&s=seeders&o=desc&p="
    # Number of pages to scrape
    pages_to_scrape = 5

    all_magnet_links = []
    # Load processed links from file
    processed_links = load_processed_links()

    for page in range(1, pages_to_scrape + 1):
        url = f"{base_url}{page}"
        magnet_links = await get_magnet_links(url)
        all_magnet_links.extend(magnet_links)

    await download_magnets(all_magnet_links, processed_links)

    print("=" * 50, end="\n\n")

def run_main_task():
    asyncio.run(main_task())

def initialize_client():
    global client
    try:
        client = PikPakApi(
            username="username",
            password="password",
            httpx_client_args={
                "proxy": HTTP_PROXY,
                "transport": httpx.AsyncHTTPTransport(retries=3),
            },
        )
        asyncio.run(client.login())
        asyncio.run(client.refresh_access_token())
        
        print("Get Pikpak User Info:")
        print(json.dumps(client.get_user_info(), indent=4))
        print("=" * 50, end="\n\n")
    except Exception as e:
        print(f"Failed to initialize client: {str(e)}")
        client = None

if __name__ == "__main__":
    while True:
        initialize_client()  # Initialize and log in only once
        if client is not None:
            schedule.every(15).minutes.do(run_main_task)
            while True:
                try:
                    schedule.run_pending()
                    time.sleep(1)
                except Exception as e:
                    print(f"Error in scheduler: {str(e)}")
                    print("Waiting for 10 minutes before retrying...")
                    # Wait for 10 minutes
                    time.sleep(10 * 60)
        else:
            print("Client initialization failed. Exiting...")
            time.sleep(10 * 60)

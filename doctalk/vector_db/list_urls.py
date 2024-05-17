import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

visited_links = set()

def scrape_links(url):
    if url in visited_links:
        return

    print("Scraping:", url)
    try:
        visited_links.add(url)

        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to retrieve the page: {url}")
            return

        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a"):
            href = link.get("href")
            if href:
                absolute_url = urljoin(url, href)
                if absolute_url.startswith(base_url):
                    if "#" not in absolute_url:
                        scrape_links(absolute_url)
    except:
        print("Something went wrong...")
        return


if __name__ == "__main__":
    # Scrape links (base URL is used to avoid external links)
    base_url = "https://docs.pinecone.io"
    scrape_links("https://docs.pinecone.io/home")
    # Prepare the dictionary
    url_list = []
    for url in visited_links:
        url_list.append({"url": url})
    # Dump to file
    json_str = json.dumps(url_list, indent=4)
    with open('data/pinecone_docs_urls.json', 'w') as fp:
        print(json_str, file=fp)

    # Scrape links (base URL is used to avoid external links)
    visited_links = set()
    base_url = "https://octo.ai"
    scrape_links("https://octo.ai")
    # Prepare the dictionary
    url_list = []
    for url in visited_links:
        url_list.append({"url": url})
    # Dump to file
    json_str = json.dumps(url_list, indent=4)
    with open('data/octoai_docs_urls.json', 'w') as fp:
        print(json_str, file=fp)

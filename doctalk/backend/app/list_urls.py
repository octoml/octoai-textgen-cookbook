import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

visited_links = set()


def to_json():
    input_file = "data/pinecone_docs_urls.json"  # The name of your input file
    output_file = "pinecone_docs_urls_output.txt"  # The name of your output file

    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            url = line.strip()  # Remove any leading/trailing whitespace
            formatted_line = '{{"url": "{}"}},\n'.format(url)
            outfile.write(formatted_line)

    print("File has been converted.")


def scrape_links(url):
    if url in visited_links:
        return
    print("Scraping:", url)
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
            if base_url in absolute_url:
                scrape_links(absolute_url)


if __name__ == "__main__":
    # to_json()
    base_url = "https://docs.pinecone.io/docs"
    scrape_links(base_url)

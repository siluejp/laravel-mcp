import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# The base URL for the Laravel 5.6 documentation
BASE_URL = "https://laravel.com/docs/5.6"
import sys
import os

# Add project root to path to allow importing from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.config import VECTOR_STORE_PATH

def get_all_doc_links(url):
    """
    Crawls the documentation sidebar to find all unique page links.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching main URL {url}: {e}")
        return set()

    soup = BeautifulSoup(response.content, 'lxml')
    
    sidebar = soup.find('div', class_='docs_sidebar')
    if not sidebar:
        print("Could not find the documentation sidebar.")
        return set()

    links = set()
    for a_tag in sidebar.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/') or href.startswith(BASE_URL):
            full_url = urljoin(BASE_URL + '/', href)
            parsed_url = urlparse(full_url)
            clean_url = parsed_url._replace(fragment="").geturl()
            if '/docs/5.6/' in clean_url:
                links.add(clean_url)

    return links

def scrape_page_content(url):
    """
    Scrapes the main textual content from a single documentation page.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        main_content = soup.find('section', class_='docs_main')
        if main_content:
            return main_content.get_text(separator='\n', strip=True)
        else:
            print(f"Warning: Could not find <main> content for {url}")
            return ""
    except requests.RequestException as e:
        print(f"Error fetching page {url}: {e}")
        return ""

def main():
    """
    Main function to crawl, scrape, chunk, and embed the documentation.
    """
    print("Starting documentation crawl...")
    doc_links = get_all_doc_links(BASE_URL)
    
    if not doc_links:
        print("No documentation links found. Exiting.")
        return

    print(f"Found {len(doc_links)} unique documentation pages.")
    
    documents = []
    for i, link in enumerate(doc_links):
        print(f"Scraping page {i+1}/{len(doc_links)}: {link}")
        content = scrape_page_content(link)
        if content:
            documents.append({"page_content": content, "metadata": {"source": link}})

    print("\nScraping complete. Now chunking text...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    # Re-structure documents for the text splitter
    docs_to_split = [d["page_content"] for d in documents]
    all_splits = text_splitter.create_documents(docs_to_split, metadatas=[d["metadata"] for d in documents])
    
    print(f"Successfully created {len(all_splits)} text chunks.")

    print("\nInitializing embedding model... (This may download the model)")
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cpu'} # Use CPU
    embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

    print("\nCreating and saving FAISS vector store...")
    vector_store = FAISS.from_documents(all_splits, embeddings)
    vector_store.save_local(VECTOR_STORE_PATH)
    
    print(f"\nVector store successfully saved to '{VECTOR_STORE_PATH}'")

if __name__ == "__main__":
    main()

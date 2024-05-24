from bs4 import BeautifulSoup
import cloudscraper
import time
import random

def get_complaint_links(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    complaint_links = soup.find_all('a', class_='complaint-layer')
    return [link['href'] for link in complaint_links]

def main():
    current_page = 2
    max_pages = 350
    all_complaint_links = []
    
    while current_page <= max_pages:
        scraper = cloudscraper.create_scraper()
        base_url = "https://www.sikayetvar.com"
        next_page_url = f"{base_url}/turkcell?page={current_page}"
        
        response = scraper.get(next_page_url)
        if response.status_code != 200:
            print(f"Failed to retrieve page {current_page}.")
            break
        
        html_text = response.text
        complaint_links = get_complaint_links(html_text)
        if not complaint_links:
            break
        
        all_complaint_links.extend([base_url + link for link in complaint_links])
        
        print(f"Page {current_page} processed.")
        current_page += 1
        time.sleep(random.randint(15,20))
        
    open("complaint_links.txt","w").write("\n".join(all_complaint_links))

if __name__ == "__main__":
    main()
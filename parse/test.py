from bs4 import BeautifulSoup
import cloudscraper
import time

def get_complaint_links(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    complaint_links = soup.find_all('a', class_='complaint-description')
    return [link['href'] for link in complaint_links]

def main():
    scraper = cloudscraper.create_scraper()
    base_url = "https://www.sikayetvar.com"
    start_url = f"{base_url}/turkcell"
    
    response = scraper.get(start_url)
    if response.status_code != 200:
        print("Failed to retrieve the first page.")
        return
    
    html_text = response.text
    first_page_links = get_complaint_links(html_text)
    all_complaint_links = [base_url + link for link in first_page_links]
    
    current_page = 2
    while True:
        response = scraper.get(f"{start_url}?page={current_page}")
        if response.status_code != 200:
            print(f"Failed to retrieve page {current_page}")
            break
        
        html_text = response.text
        complaint_links = get_complaint_links(html_text)
        if not complaint_links:
            break  
        
        all_complaint_links.extend([base_url + link for link in complaint_links])
        
        print(f"Page {current_page} processed.")
        current_page += 1
        
        time.sleep(10)  
    
    print("All complaint links:")
    for link in all_complaint_links:
        print(link)
        
        time.sleep(10)  

if __name__ == "__main__":
    main()

from bs4 import BeautifulSoup
import cloudscraper
import time
import random

def get_complaint_links(html_text,company_name):
    soup = BeautifulSoup(html_text, 'html.parser')
    complaint_links = soup.find_all('a', class_='complaint-layer')
    links=[]
    for link in complaint_links:
        if link['href'].split("/")[1]==company_name:
            links.append(link["href"])
    return links

def main(company_name="",max_pages = 350):
    current_page = 2
    
    all_complaint_links = []
    
    while current_page <= max_pages:
        scraper = cloudscraper.create_scraper()
        base_url = "https://www.sikayetvar.com"
        next_page_url = f"{base_url}/{company_name}?page={current_page}"
        
        response = scraper.get(next_page_url)
        if response.status_code != 200:
            print(f"Failed to retrieve page {current_page}.")
            break
        
        html_text = response.text
        complaint_links = get_complaint_links(html_text,company_name)
        if len(complaint_links)==0:
            break
        
        all_complaint_links.extend([base_url + link for link in complaint_links])
        
        print(f"Page {current_page} processed.")
        current_page += 1
        time.sleep(random.randint(4,8))
        
    open(f"complaint_links_{company_name}.txt","w").write("\n".join(list(set(all_complaint_links))))

if __name__ == "__main__":
    main(company_name="vodafone",max_pages=400)
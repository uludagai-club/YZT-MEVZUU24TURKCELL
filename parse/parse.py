import cloudscraper
from bs4 import BeautifulSoup
import time
import requests
import csv
import random

def get_complaint_detail_description(url:str):
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, 'html.parser')
        complaint_detail = soup.find('div', class_='complaint-detail-description')
        if complaint_detail:
            paragraph = complaint_detail.find('p')
            if paragraph:
                return paragraph.get_text().strip()
            else:
                return 'No <p> tag found within the complaint detail description div.'
        else:
            return 'No div with class "complaint-detail-description" found.'
    except requests.exceptions.RequestException as e:
        return f'Error fetching the URL: {e}'

def load_links(company_name:str)->list[str]:
    with open(f'docs/complaint_links_{company_name}.txt', 'r', encoding="utf-8") as f:
        complaint_links = f.readlines()
    
    return list(set(complaint_links))

def write_to_csv(results:list[dict[str, str]],company_name:str):
    if len(results)>25:
        with open(f'docs/complaints_{company_name}.csv', mode='a+', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['url', 'complaint'])
            writer.writerows(results)
        results.clear()

def get_paragraphes(complaint_links:list[str],company_name:str):
    results=[]
    for url in complaint_links:
        complaint = get_complaint_detail_description(url)
        results.append({'url': url, 'complaint': complaint})
        time.sleep(random.randint(4,8))
        
        write_to_csv(results=results,company_name=company_name)

if __name__ == "__main__":
    
    company_name="turkcell"
    complaint_links=load_links(company_name=company_name)
    get_paragraphes(complaint_links=complaint_links,company_name=company_name)

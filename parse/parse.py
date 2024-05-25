import cloudscraper
from bs4 import BeautifulSoup
import time
import requests
import csv
import random

def get_complaint_detail_description(url):
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

results = []

all_complaint_links=[]
with open('complaint_vodafone_links.txt', 'r', encoding="utf-8") as f:
    all_complaint_links = f.readlines()
    
all_complaint_links = list(set(all_complaint_links))


for url in all_complaint_links[3026:]:
    print(f'Fetching data from {url}')
    result = get_complaint_detail_description(url)
    results.append({'url': url, 'complaint': result})
    time.sleep(random.randint(4,8))
    if len(results)>100:
        with open('complaints_vodafone.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['url', 'complaint'])
            writer.writerows(results)
        results=[]

print("Data has been written to complaints.csv")
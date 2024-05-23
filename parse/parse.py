import cloudscraper
from bs4 import BeautifulSoup
import time
import requests
import csv

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
with open('test.txt', 'r', encoding="utf-8") as f:
    all_complaint_links = f.readlines()

for url in all_complaint_links:
    print(f'Fetching data from {url}')
    result = get_complaint_detail_description(url)
    results.append({'url': url, 'complaint': result})
    time.sleep(20)  

with open('complaints.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['url', 'complaint'])
    writer.writeheader()
    writer.writerows(results)

print("Data has been written to complaints.csv")
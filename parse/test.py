# import cloudscraper
# import csv
# import time

# scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
# # print(scraper.get("https://www.sikayetvar.com/turkcell/turkcell-internet-ve-konusma-paketleri").text)  # => "<!DOCTYPE html><html><head>..."

# html_text = scraper.get("https://www.sikayetvar.com/turkcell").text

# # pattern = r'<a class="complaint-description" href="#">(.*?)</a>'

# # # Metindeki tüm eşleşmeleri bul
# # matches = re.findall(pattern, web_site_html)

# # # CSV dosyasını aç ve yazma modunda başlat
# # with open('complaints.csv', 'w', newline='', encoding='utf-8') as csvfile:
# #     # CSV dosyası yazma işlemi için writer objesini oluştur
# #     writer = csv.writer(csvfile)
    
# #     # Her bir eşleşmeyi CSV'ye yaz
# #     for match in matches:
# #         writer.writerow([match])

# # print("Complaint metinleri başarıyla CSV dosyasına yazıldı.")

# scraper = cloudscraper.create_scraper()  

# html_text = scraper.get("https://www.sikayetvar.com/turkcell").text

# def get_texts_from_html(html_text):
#     texts = []
#     lines = html_text.split('\n')
#     for line in lines:
#         if 'complaint-description' in line:
#             start_index = line.find('>') + 1
#             end_index = line.rfind('<')
#             text = line[start_index:end_index].strip()
#             texts.append(text)
#     return texts

# def write_to_csv(data, filename):
#     with open(filename, 'a', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Text'])
#         for row in data:
#             writer.writerow([row])

# def main():
#     scraper = cloudscraper.create_scraper()  
#     html_text = scraper.get("https://www.sikayetvar.com/turkcell").text
#     current_page = 1

#     while True:
#         active_page_index = html_text.find('class="page active"')
#         if active_page_index == -1:
#             break
        
#         html_text = html_text[active_page_index:]
#         texts = get_texts_from_html(html_text)
#         write_to_csv(texts, 'complaints.csv')
        
#         print(f'Page {current_page} processed.')
        
#         current_page += 1
#         time.sleep(15)  

# if __name__ == "__main__":
#     main()

from bs4 import BeautifulSoup
import cloudscraper

def get_complaint_links(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    complaint_links = soup.find_all('a', class_='complaint-description')
    return [link['href'] for link in complaint_links]

def main():
    scraper = cloudscraper.create_scraper()
    base_url = "https://www.sikayetvar.com"
    start_url = f"{base_url}/turkcell"
    current_page = 1
    all_complaint_links = []

    while True:
        response = scraper.get(f"{start_url}?page={current_page}")
        if response.status_code != 200:
            print(f"Failed to retrieve page {current_page}")
            break
        
        html_text = response.text
        complaint_links = get_complaint_links(html_text)
        all_complaint_links.extend([base_url + link for link in complaint_links])
        
        current_page += 1

        soup = BeautifulSoup(html_text, 'html.parser')
        next_page_span = soup.find('span', class_='page active').find_next_sibling('span', class_='page')
        if not next_page_span:
            break
    
    print("All complaint links:")
    for link in all_complaint_links:
        print(link)

if __name__ == "__main__":
    main()

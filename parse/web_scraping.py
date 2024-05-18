import http.client
import csv
import re
from bs4 import BeautifulSoup

# Define the function to send the request and get the response
def get_response(path):
    conn = http.client.HTTPSConnection("www.sikayetvar.com")
    
    headers = {
        "Cookie": "svhash=e81a0ec623a712fe10ce1f8c83c594ef; _svuid=s%3AkpzGOEQwSDANyAdpWwQSjZp0W05XChQG.PMdcqouqTC8tDinoERLpbI%2BkWDL6exPbgD1Tu9tLqVg; _ga=GA1.1.1225513788.1715439062; __gads=ID=bcc632712a64e785:T=1715439062:RT=1715439062:S=ALNI_MauTe3Mgnuoj3ownzZ_WO7a7mvrKg; __gpi=UID=00000e18f7f888e5:T=1715439062:RT=1715439062:S=ALNI_MYQLXji7VZsYnLVGvvDIkGbnGGWyQ; __eoi=ID=897aacb7cb4ac4dd:T=1715439062:RT=1715439062:S=AA-AfjYv19H11Abo2ZiBANzyr4Ff; _fbp=fb.1.1715439063661.1668251654; _hjSession_1263098=eyJpZCI6IjI0NTY2ODg2LTBkZTEtNDA5Ny05OTM0LTYzYzJkMzNjZjEyMSIsImMiOjE3MTU0MzkwNjQ1MzUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _cc_id=f7d9c964f5a9bab5386f1488bd197357; panoramaId_expiry=1716043864479; panoramaId=5b4c4f061ce9400be837a08483fc185ca02c93cc186052ecc83e31a2ba772abc; panoramaIdType=panoDevice; _iat_ses=9ABAF6C0E4D01108; CookieConsent={stamp:%279IeQ/mIg1MqFH8kbjbkm7Y339KmcWKKNCSmUPmfwxzIta6pXZkarSA==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:2%2Cutc:1715439086871%2Cregion:%27tr%27}; stats-track=false; showHeader=1; _hjSessionUser_1263098=eyJpZCI6Ijk5ZjA4ZGE3LTRiZDUtNWNkMy1hZGNlLWQ4NGFlYTVlOGRlNyIsImNyZWF0ZWQiOjE3MTU0MzkwNjQ1MzQsImV4aXN0aW5nIjp0cnVlfQ==; FCNEC=%5B%5B%22AKsRol_MRg48Mbv5jrlGvLe6wckTJjsETpr7sviuLbmarRMC7p_pXDWlqPC-eoBJqLZNnSX4qA_Vjz02xTDqG1lQVESlfQYB8FsXp7Yqq-Z-WBXBu3oH2a0exIj5cJJ0GiKl5f0WoDKchXs4ou4NFy3p2jG2oOxo4g%3D%3D%22%5D%5D; __iat_vis=9ABAF6C0E4D01108.3916c4261222b157da9dee4a71f38043.1715439098080.3cb9245983e3ddeb5d1280826fa672fd.IUMRJUJEIB.11111111.1.0; udmsrc=%7B%7D; _sharedid=fe0239a4-2818-40c2-9a84-599de41e0588; udm_edge_floater_fcap=%5B1715439117365%5D; __qca=P0-1339002503-1715439114284; _sharedid_cst=VyxHLMwsHQ%3D%3D; pbjs-unifiedid=%7B%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222024-05-11T14%3A52%3A01%22%7D; pbjs-unifiedid_cst=VyxHLMwsHQ%3D%3D; udm_session=2; udm_session_rad=1; udm_iframeSyncStatus=synced; JSESSIONID=6A5093181FAB751B0854E8F594B8F376; _ga_FXTD430HRD=GS1.1.1715439062.1.1.1715439222.60.0.0; resolved-complaint-count={%22current%22:3155993%2C%22target%22:3155996}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.sikayetvar.com/turkcell"
    }
    
    conn.request("GET", path, headers=headers)
    response = conn.getresponse()
    
    if response.status != 200:
        print(f"Error: {response.status} {response.reason}")
        return None
    
    return response.read().decode("utf-8")

# Define the function to extract complaint details
def get_complaint_details(html):
    soup = BeautifulSoup(html, "html.parser")
    description = soup.find("p", class_="complaint-detail-description")
    if description:
        return description.text.strip()
    else:
        return "Açıklama bulunamadı."

# Define the function to write complaints to a CSV file
def write_to_csv(data, filename="yorumlar.csv"):
    with open(filename, mode="w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow({"description": row})

# Main function to get complaints and write to CSV
def main():
    base_path = "/turkcell"
    page_number = 1
    all_complaints = []

    while True:
        path = f"{base_path}?page={page_number}"
        html = get_response(path)
        if not html:
            break
        
        soup = BeautifulSoup(html, "html.parser")
        complaint_layers = soup.find_all("div", class_="complaint-layer")

        if not complaint_layers:
            break

        for complaint_layer in complaint_layers:
            href = complaint_layer.find("a")["href"]
            complaint_html = get_response(href)
            if complaint_html:
                description = get_complaint_details(complaint_html)
                all_complaints.append(description)

        page_number += 1

    write_to_csv(all_complaints)

if __name__ == "__main__":
    main()

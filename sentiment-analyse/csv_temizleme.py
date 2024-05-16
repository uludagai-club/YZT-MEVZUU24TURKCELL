import csv
import chardet

with open("reviews.csv", 'rb') as dosya:
    kodlama = chardet.detect(dosya.read())['encoding']

dosya_adi = "reviews.csv"

temizlenmis_dosya_adi = "cleaned_reviews.csv"

with open(dosya_adi, "r", newline="", encoding=kodlama) as dosya_in, \
     open(temizlenmis_dosya_adi, "w", newline="", encoding="utf-8") as dosya_out:

    csv_okuyucu = csv.reader(dosya_in)
    csv_yazici = csv.writer(dosya_out)
    
    for satir in csv_okuyucu:
        yeni_satir = satir[0]
        
        csv_yazici.writerow([yeni_satir])

print("CSV dosyası temizlendi ve kaydedildi.")

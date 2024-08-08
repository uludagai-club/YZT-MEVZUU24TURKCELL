import requests

url = "http://localhost:8000/predict/"
data = {
    "text": "Fiber 100mb SuperOnline kullanıcısıyım yaklaşık 2 haftadır @Twitch @Kick_Turkey gibi canlı yayın platformlarında 360p yayın izlerken donmalar yaşıyoruz."
}

response = requests.post(url, json=data)
print(response.json())
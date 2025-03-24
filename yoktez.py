# yoktez.py
import requests
from bs4 import BeautifulSoup

def search_yoktez(query):
    """YÖK Tez Merkezi'nde verilen sorguya göre arama yapar."""
    base_url = "https://tez.yok.gov.tr/UlusalTezMerkezi/tezSorguSonucYeni.jsp"
    params = {"arananKelime": query}
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.post(base_url, data=params, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            for item in soup.select(".tezBaslik a"):
                title = item.text.strip()
                link = "https://tez.yok.gov.tr" + item["href"]
                if any(word.lower() in title.lower() for word in query.split()):
                    results.append({"title": title, "link": link})
            return results if results else {"message": f"YÖK Tez'de '{query}' için sonuç bulunamadı."}
        else:
            return {"error": f"HTTP Hatası: {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"error": "Bağlantı zaman aşımına uğradı."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Bağlantı hatası oluştu: {str(e)}"}

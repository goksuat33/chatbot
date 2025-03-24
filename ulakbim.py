# ulakbim.py
import requests
from bs4 import BeautifulSoup

def search_ulakbim(query, search_type="Anahtar Kelime"):
    """
    ULAKBİM Keşif üzerinden akademik içerik arama.
    """
    base_url = "https://search.ulakbim.gov.tr/tr?q="
    search_types = {
        "Anahtar Kelime": "q",
        "Başlık": "title",
        "Yazar": "author",
        "Tam Metin": "fulltext",
        "Konu Terimleri": "subject",
        "Dergi Adı": "journal",
        "Özet": "abstract",
        "ISSN": "issn",
        "ISBN": "isbn"
    }
    search_param = search_types.get(search_type, "q")
    full_url = f"{base_url}{query}&type={search_param}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(full_url, headers=headers)
    if response.status_code != 200:
        return {"error": f"ULAKBİM bağlantı hatası: {response.status_code}"}
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for item in soup.select("div.search-result-item"):
        title = item.select_one("h3").text.strip() if item.select_one("h3") else "Başlık Yok"
        link = item.select_one("a")["href"] if item.select_one("a") else "#"
        results.append({"title": title, "link": link})
    return results if results else {"message": "Sonuç bulunamadı."}

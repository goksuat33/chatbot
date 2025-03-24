# harman.py
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://harman.ulakbim.gov.tr"

def search_harman_oai(query):
    """
    Harman (ULAKBİM) üzerinden verilen sorgu ile akademik makale araması yapar.
    
    Args:
        query (str): Kullanıcının aramak istediği terim.
    
    Returns:
        list: Makale başlıkları ve bağlantıları içeren sözlük listesi.
    """
    search_url = f"{BASE_URL}/index.php/search"
    params = {"q": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.Timeout:
        return {"error": "Harman API isteği zaman aşımına uğradı."}
    except requests.RequestException as e:
        return {"error": f"Harman API isteği başarısız oldu: {str(e)}"}
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    articles = soup.find_all("a", class_="link-effect record--header ng-binding")
    for article in articles:
        title = article.get_text(strip=True)
        link = f"{BASE_URL}{article['href']}" if article.has_attr("href") else "Bağlantı bulunamadı"
        results.append({"title": title, "link": link})
    if not results:
        return {"message": f"Harman'da '{query}' ile ilgili sonuç bulunamadı."}
    return results
# dergipark.py
import requests
from bs4 import BeautifulSoup

def search_dergipark_oai(query: str, max_results=10):
    """
    DergiPark üzerinden anahtar kelime ile makale başlığı arar.
    
    Args:
        query (str): Aranacak anahtar kelime.
        max_results (int): Döndürülecek maksimum sonuç sayısı.
    
    Returns:
        dict: Makale başlıkları listesi veya bilgilendirme mesajı.
    """
    results = []
    try:
        base_url = "https://dergipark.org.tr/tr/search"
        params = {"q": query, "section": "articles"}
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        if response.status_code != 200:
            return {"error": f"🔌 Bağlantı hatası: {response.status_code}"}
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("a", class_="card-title", limit=max_results)
        for article in articles:
            title = article.text.strip()
            link = "https://dergipark.org.tr" + article.get("href", "")
            results.append({"title": title, "link": link})
        if not results:
            return {"message": f"Dergipark'ta '{query}' için doğrudan sonuç bulunamadı."}
        return results
    except Exception as e:
        return {"error": f"DergiPark araması sırasında hata oluştu: {str(e)}"}
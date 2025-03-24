# earsiv.py
import requests
from bs4 import BeautifulSoup

def search_earsiv(query: str, max_results: int = 10):
    """
    Batman Üniversitesi E-Arşiv sistemi üzerinde verilen terime göre arama yapar.
    
    Args:
        query (str): Aranacak kelime veya cümle.
        max_results (int): Döndürülecek maksimum sonuç sayısı.
    
    Returns:
        list: Bulunan makale başlıkları ve bağlantıları.
    """
    results = []
    try:
        base_url = "https://earsiv.batman.edu.tr/xmlui/discover"
        params = {"query": query}
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        if response.status_code != 200:
            return {"error": f"Bağlantı hatası: {response.status_code}"}
        soup = BeautifulSoup(response.text, "html.parser")
        records = soup.find_all("div", class_="artifact-description", limit=max_results)
        for record in records:
            title_element = record.find("a")
            if title_element:
                title = title_element.text.strip()
                link = "https://earsiv.batman.edu.tr" + title_element.get("href", "")
                results.append({"title": title, "link": link})
        if not results:
            return {"message": f"YÖK Arşiv'de '{query}' ile ilgili sonuç bulunamadı."}
        return results
    except Exception as e:
        return {"error": f"E-Arşiv araması sırasında hata oluştu: {str(e)}"}
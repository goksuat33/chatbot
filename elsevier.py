# elsevier.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELSEVIER_API_KEY")

def search_elsevier(query):
    """
    Elsevier API ile makale arama yapar.
    Scopus ve ScienceDirect bağlantılarını içeren sonuçları döndürür.
    
    Args:
        query (str): Arama terimi.
    
    Returns:
        list/dict: Arama sonuçları veya hata mesajı.
    """
    if not API_KEY:
        return {"error": "API anahtarı bulunamadı. Lütfen .env dosyanızı kontrol edin."}
    url = f"https://api.elsevier.com/content/search/scopus?query={query}"
    headers = {
        "X-ELS-APIKey": API_KEY,
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = []
            for entry in data.get("search-results", {}).get("entry", []):
                title = entry.get("dc:title", "Başlık Bulunamadı")
                scopus_id = entry.get("dc:identifier", "").replace("SCOPUS_ID:", "")
                scopus_link = f"https://www.scopus.com/record/display.uri?eid={scopus_id}&origin=resultslist"
                sciencedirect_link = entry.get("prism:url", "")
                results.append({
                    "title": title,
                    "scopus_link": scopus_link,
                    "sciencedirect_link": sciencedirect_link if sciencedirect_link else "ScienceDirect bağlantısı yok"
                })
            return results if results else {"message": f"Elsevier'de '{query}' için sonuç bulunamadı."}
        elif response.status_code == 401:
            return {"error": "Elsevier API Anahtarı Geçersiz. Lütfen API anahtarınızı kontrol edin."}
        else:
            return {"error": f"Elsevier API hatası: {response.status_code}, {response.text}"}
    except requests.exceptions.Timeout:
        return {"error": "Elsevier API bağlantısı zaman aşımına uğradı."}
    except requests.exceptions.RequestException as e:
        return {"error": f"API bağlantı hatası: {str(e)}"}
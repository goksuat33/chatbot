# googlescholar.py
import requests
from bs4 import BeautifulSoup

def search_google_scholar(query):
    """
    Google Scholar üzerinde verilen sorguya göre makale araması yapar.
    
    Parametre:
        query (str): Kullanıcının arama sorgusu.
    
    Dönüş:
        list: Bulunan makalelerin başlıkları ve bağlantıları.
        dict: Hata mesajı veya sonuç bulunamadı mesajı.
    """
    base_url = "https://scholar.google.com/scholar"
    params = {"q": query, "hl": "tr"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for item in soup.select(".gs_r.gs_or.gs_scl"):
            title_tag = item.select_one(".gs_rt a")
            if title_tag:
                title = title_tag.text.strip()
                link = title_tag["href"]
                results.append({"title": title, "link": link})
        if not results:
            return {"message": f"Google Scholar'da '{query}' için sonuç bulunamadı."}
        return results
    except requests.exceptions.Timeout:
        return {"error": "Google Scholar bağlantısı zaman aşımına uğradı. Lütfen tekrar deneyiniz."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Google Scholar'a bağlanırken hata oluştu: {str(e)}"}
    except Exception as e:
        return {"error": f"Bilinmeyen bir hata oluştu: {str(e)}"}
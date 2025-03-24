# semanticscholar.py
import requests
import urllib.parse

def search_semantic_scholar(query):
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    try:
        safe_query = urllib.parse.quote_plus(query, encoding="utf-8", errors="ignore")
        params = {
            "query": safe_query,
            "fields": "title,url,authors",
            "limit": 5
        }
        headers = {
            "x-api-key": "YOUR_API_KEY_HERE",  # Kendi API anahtarınızı buraya ekleyin.
            "Accept": "application/json",
            "Accept-Charset": "utf-8"
        }
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.encoding = "utf-8"
        if response.status_code == 200:
            data = response.json()
            results = [
                {"title": paper["title"], "link": paper["url"]}
                for paper in data.get("data", [])
            ]
            return results if results else {"message": f"Semantic Scholar'da '{query}' için sonuç bulunamadı."}
        else:
            return {"error": f"Semantic Scholar API hatası: {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"error": "Semantic Scholar API bağlantısı zaman aşımına uğradı. Lütfen tekrar deneyin."}
    except Exception as e:
        return {"error": f"Hata oluştu: {str(e)}"}

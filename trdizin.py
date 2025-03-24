# trdizin.py
import requests
from requests.utils import quote

BASE_URL = "https://search.trdizin.gov.tr/api/defaultSearch"

def search_trdizin(query, search_type="publication", page=1, limit=20):
    """TR Dizin API üzerinden arama yapar ve hataları yönetir."""
    encoded_query = quote(query)
    url = f"{BASE_URL}/{search_type}/?q={encoded_query}&order=publicationYear-DESC&page={page}&limit={limit}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        try:
            data = response.json()
        except ValueError:
            return {"error": "Yanıt JSON formatında değil", "status_code": response.status_code}
        return data
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP hatası: {http_err}", "status_code": response.status_code}
    except requests.exceptions.Timeout:
        return {"error": "Bağlantı zaman aşımına uğradı."}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Bilinmeyen bir istek hatası oluştu: {req_err}"}

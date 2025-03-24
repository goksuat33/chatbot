# googlebooks.py
import requests

def search_google_books(query):
    """
    Google Books API üzerinden verilen sorguya göre kitap araması yapar.
    
    Parametre:
        query (str): Kullanıcının aradığı kitap veya konu başlığı.
    
    Döndürür:
        list/dict: Bulunan kitapları içeren liste veya hata mesajı.
    """
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": query,
        "maxResults": 5
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = [
                {
                    "title": book["volumeInfo"].get("title", "Başlık bilgisi yok"),
                    "authors": book["volumeInfo"].get("authors", ["Yazar bilgisi yok"]),
                    "link": book["volumeInfo"].get("infoLink", "Bağlantı yok")
                }
                for book in data.get("items", [])
            ]
            return results if results else {"message": f"Google Books'ta '{query}' için sonuç bulunamadı."}
        else:
            return {"error": f"Google Books API'de hata oluştu. HTTP Durum Kodu: {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"error": "Google Books API bağlantısı zaman aşımına uğradı."}
    except Exception as e:
        return {"error": f"Beklenmeyen bir hata oluştu: {str(e)}"}
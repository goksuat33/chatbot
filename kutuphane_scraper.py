# kutuphane_scraper.py
import requests
from bs4 import BeautifulSoup

URL = "https://batman.edu.tr/Birimler/kutuphane"

def scrape_batman_universitesi_kutuphane():
    """
    Batman Üniversitesi Kütüphane sayfasından duyurular ve menü başlıklarını çeker.
    
    Returns:
        dict: Sayfa başlığı, duyurular ve menüler içeren sözlük.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"Sayfa yüklenemedi, hata: {str(e)}"}
    soup = BeautifulSoup(response.text, "html.parser")
    results = {"sayfa_basligi": soup.title.string.strip() if soup.title else "Başlık Yok"}
    menu_items = soup.find_all("a")
    results["menuler"] = [
        {"name": item.text.strip(), "link": item["href"]}
        for item in menu_items if item.text.strip() and item.has_attr("href")
    ]
    announcements = soup.find_all("a", href=True)
    results["duyurular"] = [
        {"baslik": item.text.strip(), "link": f"https://batman.edu.tr{item['href']}"}
        for item in announcements if "haberler" in item["href"] and item.text.strip()
    ]
    return results
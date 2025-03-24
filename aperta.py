# aperta.py
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def search_aperta(query: str):
    """
    Aperta Ulakbim Açık Arşiv üzerinden makale araması yapar.
    
    Args:
        query (str): Aranacak anahtar kelime.
    
    Returns:
        list: Bulunan sonuçlar (başlık ve link bilgisi).
    """
    results = []
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        search_url = f"https://aperta.ulakbim.gov.tr/search?ln=tr&p={query.replace(' ', '+')}&action_search=Search&sf=all"
        driver.get(search_url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        records = soup.find_all("td", class_="summary")
        for record in records:
            title_tag = record.find("a")
            if title_tag:
                title = title_tag.text.strip()
                href = title_tag.get("href")
                full_link = "https://aperta.ulakbim.gov.tr" + href
                results.append({"title": title, "link": full_link})
        driver.quit()
        if not results:
            return {"message": f"Aperta'da '{query}' ile ilgili sonuç bulunamadı."}
        return results
    except Exception as e:
        return {"error": f"Aperta aramasında hata oluştu: {str(e)}"}
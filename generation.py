# generation.py
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    raise ValueError("❌ OpenAI API anahtarı bulunamadı! Lütfen .env dosyanızı kontrol edin.")

def generate_response(query):
    """
    Kullanıcının sorgusuna göre OpenAI modelinden cevap üretir.
    
    :param query: Kullanıcının sorduğu soru
    :return: OpenAI tarafından üretilen yanıt veya hata mesajı
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sen bir akademik araştırma asistanısın."},
                {"role": "user", "content": query}
            ]
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        return f"❌ OpenAI API hatası: {str(e)}"

if __name__ == "__main__":
    user_query = "Yapay zeka nasıl çalışır?"
    print(f"Üretilen Cevap: {generate_response(user_query)}")
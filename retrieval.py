# retrieval.py
import os
from vector_db import query_document
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # .env dosyasından OpenAI API anahtarını yükler

# 📌 OpenAI API Anahtarını Al
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# 📌 Belge Getirme Fonksiyonu
def retrieve_documents(query, top_k=3):
    """Kullanıcının sorgusuna en uygun belgeleri getirir."""
    results = query_document(query, top_k=top_k)

    if "error" in results:
        return {"message": "⚠️ Hata oluştu: " + results["error"]}
    
    # results["ids"] ve results["metadatas"] listelerinin ilk elemanını kullanıyoruz.
    retrieved_docs = [
        {"id": doc_id, "text": doc_text}
        for doc_id, doc_text in zip(results.get("ids", [[]])[0], results.get("metadatas", [[]])[0])
    ]
    
    return {"retrieved_documents": retrieved_docs} if retrieved_docs else {"message": "🔍 Uygun belge bulunamadı."}

# 📌 OpenAI ile RAG Yanıtı Üretme Fonksiyonu
def generate_rag_response(query, top_k=3):
    """RAG modeli kullanarak OpenAI üzerinden yanıt üretir."""
    retrieved_docs = retrieve_documents(query, top_k)

    if "retrieved_documents" not in retrieved_docs:
        return {"response": "💡 Uygun bilgi bulunamadı. Lütfen daha spesifik bir sorgu girin."}

    context = "\n".join([doc["text"] for doc in retrieved_docs["retrieved_documents"]])

    prompt = f"Kullanıcının sorusuna en iyi yanıtı oluştur:\n\nSoru: {query}\n\nİlgili Belgeler:\n{context}\n\nYanıt:"

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sen bir akademik araştırma asistanısın."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
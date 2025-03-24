# vector_db.py
import os
import chromadb
from sentence_transformers import SentenceTransformer

# 📌 Vektör Veritabanı Yapılandırması
DB_PATH = "./vector_db"
os.makedirs(DB_PATH, exist_ok=True)

# 📌 Sentence Transformer Modeli Yükleme
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

# 📌 ChromaDB Bağlantısı
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name="document_embeddings")

# 📌 Belge Ekleme Fonksiyonu
def add_document(doc_id, text):
    """Belgeyi ChromaDB'ye ekler"""
    if not doc_id or not text:
        return "⚠️ Hata: Geçersiz belge bilgisi!"
    
    embedding = model.encode(text).tolist()
    
    try:
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            metadatas=[{"text": text}]
        )
        return f"✅ Belge eklendi: {doc_id}"
    except Exception as e:
        return f"❌ Hata oluştu: {str(e)}"

# 📌 Benzer Belgeleri Getirme Fonksiyonu
def query_document(query_text, top_k=3):
    """Sorguya en yakın belgeleri getirir"""
    if not query_text:
        return {"message": "⚠️ Hata: Geçersiz sorgu!"}

    query_embedding = model.encode(query_text).tolist()
    
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results
    except Exception as e:
        return {"error": str(e)}

# 📌 Veritabanını Temizleme Fonksiyonu
def clear_database():
    """Tüm belgeleri veritabanından siler"""
    try:
        collection.delete(ids=[])
        return "🗑️ Veritabanı temizlendi!"
    except Exception as e:
        return f"❌ Hata oluştu: {str(e)}"

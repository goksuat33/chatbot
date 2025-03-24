# rag.py
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from vector_db import query_document  # Vektör DB entegrasyonu

# 📌 OpenAI Model Yapılandırması
OPENAI_MODEL = "gpt-4"
model = ChatOpenAI(model=OPENAI_MODEL)

def retrieve_and_generate(query):
    """
    Kullanıcının sorgusuna en uygun belgeleri vektör veritabanından çeker
    ve bu belgelerle bir dil modeli (GPT-4) üzerinden mantıklı bir yanıt oluşturur.
    """
    retrieved_docs = query_document(query, top_k=3)
    if not retrieved_docs or "metadatas" not in retrieved_docs:
        return "⚠️ Uygun belge bulunamadı, lütfen farklı bir sorgu deneyin."
    
    # metadatas listesinin ilk elemanındaki belgelerden 'text' bilgilerini çıkarıyoruz.
    docs = retrieved_docs["metadatas"][0]
    texts = [doc.get("text", "") for doc in docs if "text" in doc]
    context = "\n".join(texts) if texts else "Belge bulunamadı."
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "Aşağıdaki bilgileri kullanarak mantıklı bir yanıt oluştur:\n\n{context}"),
        ("user", "{query}")
    ])
    
    try:
        parser = StrOutputParser()
        chain = prompt_template | model | parser
        response = chain.invoke({"context": context, "query": query})
        return response
    except Exception as e:
        return f"❌ Hata: {str(e)}"

if __name__ == "__main__":
    test_query = "Yapay zeka nedir?"
    print(retrieve_and_generate(test_query))
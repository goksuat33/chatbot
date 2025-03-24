# ai.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from retrieval import retrieve_documents
from dotenv import load_dotenv

load_dotenv()  # .env dosyasından OpenAI API anahtarını yükler

# ✅ LLM modelini başlat (gpt-4 veya gpt-3.5-turbo)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.4)

# ✅ Prompt formatı (Sistem mesajı + kullanıcı sorgusu)
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Aşağıda verilen kaynak bilgileriyle kullanıcı sorusuna akademik ve açıklayıcı bir yanıt ver.\n\n{context}"),
    ("user", "{question}")
])

# ✅ Çıktı dönüştürücü (Sadece yanıt metni döner)
output_parser = StrOutputParser()

def generate_rag_response(query: str, top_k: int = 3) -> dict:
    """
    Kullanıcının sorgusuna RAG tabanlı bir yanıt üretir.
    
    Args:
        query (str): Kullanıcının metin sorgusu.
        top_k (int): Vektör veritabanından getirilecek belge sayısı.
    
    Returns:
        dict: {"response": "..."} şeklinde model yanıtı.
    """
    try:
        result = retrieve_documents(query, top_k=top_k)
        if "retrieved_documents" in result:
            docs = result["retrieved_documents"]
        else:
            return result  # Hata veya bilgi bulunamadı mesajını döndürür.
        
        context = "\n\n".join([doc['text'] for doc in docs]) if docs else "Bilgi bulunamadı."
        chain = prompt_template | llm | output_parser
        response = chain.invoke({
            "context": context,
            "question": query
        })
        return {"response": response.strip()}
    
    except Exception as e:
        return {"error": f"❌ RAG yanıt üretiminde hata: {str(e)}"}
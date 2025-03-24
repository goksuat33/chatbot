# answer_grader.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# ✅ Model tanımı (gpt-4 veya gpt-3.5-turbo kullanılabilir)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# ✅ Prompta değerlendirme talimatı
prompt = ChatPromptTemplate.from_template("""
Kullanıcının sorgusu ile verilen cevabı değerlendir.

Soru:
{question}

Cevap:
{answer}

Lütfen cevabın aşağıdaki kriterlere göre kalitesini değerlendir:
1. Anlaşılır mı?
2. Konuya ne kadar uygun?
3. Yeterince detaylı mı?
4. Eksik veya yanlış bilgi içeriyor mu?
5. Akademik bir cevap mı?

Yalnızca değerlendirme sonucunu açıkla (maksimum 100 kelimeyle).
""")

parser = StrOutputParser()

# ✅ Değerlendirme zinciri (Prompt -> Model -> Çıktı)
grade_chain = prompt | llm | parser

def grade_answer(question: str, answer: str) -> str:
    """
    Yanıtın kalitesini değerlendiren bir analiz üretir.
    
    Args:
        question (str): Kullanıcının sorduğu soru.
        answer (str): Modelin verdiği cevap.
    
    Returns:
        str: Değerlendirme metni.
    """
    try:
        result = grade_chain.invoke({
            "question": question,
            "answer": answer
        })
        return result.strip()
    except Exception as e:
        return f"❌ Değerlendirme hatası: {str(e)}"

# ✅ Örnek test
if __name__ == "__main__":
    q = "Yapay zeka eğitimde nasıl kullanılır?"
    a = "Yapay zeka, öğrenci performansını analiz etmek, kişiselleştirilmiş öğrenme materyalleri sunmak ve öğretmenlere önerilerde bulunmak için kullanılabilir."
    print(grade_answer(q, a))
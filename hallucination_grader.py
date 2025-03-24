# hallucination_grader.py
from sentence_transformers import SentenceTransformer, util

# 📌 Sentence Transformer Modeli Yükle
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def check_hallucination(generated_answer, retrieved_context):
    """
    Modelin verdiği cevabın gerçek bilgilerle ne kadar uyumlu olduğunu kontrol eder.
    
    :param generated_answer: Modelin ürettiği cevap
    :param retrieved_context: Kaynaklardan getirilen gerçek bilgiler
    :return: 0-1 arasında bir doğruluk skoru (1: Gerçek bilgilerle tam uyumlu, 0: Uyum yok)
    """
    if not retrieved_context:
        return 0.0
    embedding1 = model.encode(generated_answer, convert_to_tensor=True)
    embedding2 = model.encode(retrieved_context, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embedding1, embedding2).item()
    return round(similarity, 2)
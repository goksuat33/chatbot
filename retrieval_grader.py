# retrieval_grader.py
import difflib

def grade_retrieval(query, retrieved_text):
    """
    Getirilen bilginin sorgu ile ne kadar alakalı olduğunu ölçer.
    
    :param query: Kullanıcının arama sorgusu
    :param retrieved_text: Sistemin getirdiği bilgi
    :return: 0-1 arasında bir skor (1: Çok alakalı, 0: Hiç alakalı değil)
    """
    if not retrieved_text:
        return 0.0
    similarity = difflib.SequenceMatcher(None, query.lower(), retrieved_text.lower()).ratio()
    return round(similarity, 2)

if __name__ == "__main__":
    query = "yapay zeka ile ilgili makaleler"
    retrieved_text = "Yapay zeka, insan zekasını taklit eden sistemlerdir."
    print(f"Alaka Skoru: {grade_retrieval(query, retrieved_text)}")

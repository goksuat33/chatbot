# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from retrieval import generate_rag_response, retrieve_documents
from vector_db import add_document, clear_database
from fine_tuning import fine_tune_model, predict_text
import os

app = Flask(__name__)
CORS(app)  # Frontend entegrasyonu için CORS desteği

@app.route("/search/rag", methods=["GET"])
def search_rag():
    """RAG modeli kullanarak OpenAI üzerinden yanıt üretir."""
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "⚠️ Arama terimi girilmedi."}), 400
    try:
        response = generate_rag_response(query)
        if "response" not in response:
            return jsonify({"error": "❌ RAG modeli yanıt üretemedi."}), 500
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"⚠️ Hata oluştu: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🚀 Flask API Çalışıyor!"}), 200

@app.route("/train", methods=["POST"])
def train_model():
    """Model eğitimi başlatır."""
    data = request.get_json()
    dataset_path = data.get("dataset_path", "training_data.jsonl").strip()
    if not os.path.exists(dataset_path):
        return jsonify({"error": f"❌ Dosya bulunamadı: {dataset_path}"}), 400
    try:
        result = fine_tune_model(dataset_path=dataset_path)
        return jsonify({"message": "✅ Model eğitimi tamamlandı!", "result": result})
    except Exception as e:
        return jsonify({"error": f"⚠️ Model eğitimi sırasında hata oluştu: {str(e)}"}), 500

@app.route("/predict", methods=["POST"])
def predict():
    """Eğitilmiş model ile tahmin yapar."""
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "⚠️ Tahmin için geçerli bir metin girilmedi."}), 400
    try:
        prediction = predict_text(text)
        return jsonify({"response": prediction})
    except Exception as e:
        return jsonify({"error": f"⚠️ Tahmin işlemi sırasında hata oluştu: {str(e)}"}), 500

@app.route("/clear_db", methods=["POST"])
def clear_db():
    """Vektör veritabanını temizler."""
    try:
        clear_database()
        return jsonify({"message": "🗑️ Vektör veritabanı başarıyla temizlendi!"})
    except Exception as e:
        return jsonify({"error": f"⚠️ Veritabanı temizleme sırasında hata oluştu: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
# router.py
from flask import Flask, request, jsonify
from retrieval import retrieve_documents
from generation import generate_response

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Arama terimi girilmedi."}), 400
    retrieved_docs = retrieve_documents(query)
    response = generate_response(query)
    return jsonify({
        "retrieved_documents": retrieved_docs,
        "generated_response": response
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

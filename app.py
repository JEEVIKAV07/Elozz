from flask import Flask, render_template, request, jsonify
import requests
import os

from pdf_utils import extract_pdf_pages
from rag_utils import create_embeddings, search_chunks

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():

    try:

        file = request.files["pdf"]

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        pdf_pages = extract_pdf_pages(filepath)

        create_embeddings(pdf_pages)

        return jsonify({
            "message": "PDF uploaded and processed successfully!"
        })

    except Exception as e:

        return jsonify({
            "message": str(e)
        })


@app.route("/chat", methods=["POST"])
def chat():

    try:

        user_message = request.json["message"]

        results = search_chunks(user_message)

        if len(results) == 0:

            return jsonify({
                "response": "Please upload a PDF first."
            })

        context = ""

        pages = set()

        for item in results:

            context += item["text"] + "\n"

            pages.add(item["page"])

        prompt = f"""
Answer the question using ONLY the PDF information below.

PDF Information:
{context}

Question:
{user_message}

Answer:
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:latest",
                "prompt": prompt,
                "stream": False
            }
        )

        bot_response = response.json()["response"]

        page_text = ", ".join(
            [str(page) for page in sorted(pages)]
        )

        bot_response += f"\n\n📄 Source Page(s): {page_text}"

        return jsonify({
            "response": bot_response
        })

    except Exception as e:

        return jsonify({
            "response": f"Error: {str(e)}"
        })


if __name__ == "__main__":
    app.run(debug=True)
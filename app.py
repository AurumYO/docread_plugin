import os
from waitress import serve
from flask import Flask, request, jsonify, send_from_directory
import docx
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/")
def index():
    return "Hello world!  Your web application is working!"


# Function to extract text from a .docx file
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)


# Route to upload the document and generate summary
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith(".docx"):
        text = extract_text_from_docx(file)

        # Call the OpenAI API for summarization
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Summarize the following document: {text}",
                },
            ],
            max_tokens=300,
        )

        summary = response.choices[0].message["content"]
        return jsonify({"summary": summary}), 200

    return jsonify({"error": "Unsupported file type"}), 400


@app.route("/.well-known/ai-plugin.json")
def serve_manifest():
    return send_from_directory("./", "ai-plugin.json")


@app.route("/openapi.json")
def serve_openapi():
    return send_from_directory("./", "openapi.json")


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)

import os
from waitress import serve
from flask import Flask, request, jsonify, send_from_directory, render_template
import docx
import openai
from openai.error import RateLimitError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

template_dir = os.path.abspath("./templates")
app = Flask(__name__, template_folder=template_dir)

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/")
def index():
    print("Index page")
    return render_template("upload_form.html")


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
        return render_template("upload_form.html", error="No file provided")

    file = request.files["file"]

    if file.filename == "":
        return render_template("upload_form.html", error="No selected file")

    if file and file.filename.endswith(".docx"):
        text = extract_text_from_docx(file)

        try:
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
            return render_template("upload_form.html", summary=summary)
        except RateLimitError as e:
            return render_template(
                "upload_form.html",
                error="We have reached our API limit. Please try again later.",
            )

    return render_template("upload_form.html", error="Unsupported file type")


@app.route("/.well-known/ai-plugin.json")
def serve_manifest():
    return send_from_directory("./", "ai-plugin.json")


@app.route("/openapi.json")
def serve_openapi():
    return send_from_directory("./", "openapi.json")


if __name__ == "__main__":
    app.run(debug=True)
    # serve(app, host="0.0.0.0", port=8080)

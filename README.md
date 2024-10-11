# Document Summarization App

This is a Flask web application that allows users to upload `.docx` files, extracts text from the document, and generates a summary using OpenAI's GPT-3.5-turbo model.

## Features

- Upload a `.docx` file.
- Extracts and processes the text from the uploaded document.
- Generates a concise summary of the document's content using OpenAI's GPT-3.5-turbo.
- Simple REST API with two routes:
  - `/`: Basic index route for testing the app.
  - `/upload`: Accepts `.docx` files, extracts the text, and provides a summary.

## Requirements

Ensure you have the following dependencies installed in your environment. These are listed in the `requirements.txt` file:

- Flask
- python-docx
- openai
- python-dotenv
- black (for code formatting)

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

Run the app locally to test with

```bash
python app.py
```

Upload a document and get a summary locally with:

```bash
curl -F "file=@path_to_your_file.docx" http://127.0.0.1:5000/upload
```

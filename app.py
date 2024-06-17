from flask import Flask, request, render_template, send_file, session
from PyPDF2 import PdfReader
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'filename' not in session:
        session['filename'] = None

    pdf_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.pdf')]

    if request.method == 'POST':
        search_term = request.form['search_term']
        selected_file = request.form['pdf_file']
        if selected_file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], selected_file)
            session['filename'] = selected_file

            # Extract pages containing the search term
            pages = find_pages_with_term(filepath, search_term)
            return render_template('index.html', pages=pages, search_term=search_term, filename=selected_file, pdf_files=pdf_files, highlight_text=highlight_text)
    return render_template('index.html', filename=session['filename'], pdf_files=pdf_files)

def find_pages_with_term(filepath, search_term):
    reader = PdfReader(filepath)
    pages_with_term = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if search_term.lower() in text.lower():
            pages_with_term.append((i+1, text))
    return pages_with_term

def highlight_text(text, search_term):
    highlighted_text = text.replace(search_term, f'<span class="highlight">{search_term}</span>')
    return highlighted_text

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

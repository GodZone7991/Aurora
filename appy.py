from flask import Flask, render_template, request, redirect, url_for
import time
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['csvFile']
    current_directory = os.path.dirname(os.path.abspath(__file__))
    upload_folder = os.path.join(current_directory, "uploads")
    filename = uploaded_file.filename

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, filename)  # <- This line was missing in your code
    uploaded_file.save(file_path)

    questions = []
    for key, value in request.form.items():
        if key.startswith('question'):
            questions.append(value)

    time.sleep(5)  # Simulate processing time
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return "File uploaded successfully"

if __name__ == '__main__':
    app.run(debug=True)

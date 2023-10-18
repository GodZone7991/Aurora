from flask import Flask, render_template, request
import time
import tempfile
import os



app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')

@app.route('/upload', methods=['POST'])
def upload_file(): 
    uploaded_file = request.files['csvFile']
    # Specify the directory where you want to save the uploaded file
    # Create a temporary directory in the current working directory
    temp_dir = tempfile.mkdtemp(dir=os.getcwd())

    # Get the filename of the uploaded file
    filename = uploaded_file.filename

    # Save the uploaded file in the temporary directory
    file_path = os.path.join(temp_dir, filename)
    uploaded_file.save(file_path)



    questions = []
    for key, value in request.form.items():
        if key.startswith('question'):
            questions.append(value)
    # Simulate processing time
    time.sleep(5)
    return f"File uploaded and questions received: {', '.join(questions)}"

if __name__ == '__main__':
    app.run(debug=True)

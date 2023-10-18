import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pandas as pd
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from flask import send_from_directory, send_file


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
progress = 0  # Global variable to track progress

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'  # for flashing messages

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # Check if the file is valid
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            flash('File successfully uploaded and saved')
            return redirect(request.url)
    return render_template('index.html')

@app.route('/progress')
def progress_status():
    global progress
    return jsonify({"progress": progress})


@app.route('/download', methods=['GET'])
def download():
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'enriched.csv')
    response = send_file(file_path, as_attachment=True)
    response.headers["Content-Disposition"] = "attachment; filename=enriched.csv"
    return response

@app.route('/sniffer', methods=['GET', 'POST'])
def sniffer():
    print("Entered sniffer route")

    global progress
    if request.method == 'GET':
        progress = 0  # Reset the progress when the page is loaded or reloaded
        return render_template('sniffer.html', result=None)
    
    if request.method == 'POST':
        print(request.form)
        # Handle the CSV file upload
        file = request.files['file']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        df = pd.read_csv(filepath)

        # Extract all the prompt values from the form
        prompts = [val for key, val in request.form.items() if "prompt" in key]

        print('starting prompts')
        print(prompts)


        # Initialize llm chain outside the loop, we just need to update the prompt
        llm = ChatOpenAI(openai_api_key='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',
                        temperature=0, model_name="gpt-3.5-turbo-16k")

        # Process each prompt
        for prompt_text in prompts:
            prompt_template = prompt_text + '\n"{text}"\nCONCISE SUMMARY:'
            prompt = PromptTemplate.from_template(prompt_template)
            llm_chain = LLMChain(llm=llm, prompt=prompt)
            stuff_chain = StuffDocumentsChain(
                llm_chain=llm_chain, document_variable_name="text"
            )

            for link in df['Links']:
                print(f"Processing link: {link}")
    
 

            results = []
            total_links = len(df['Links'])
            for index, link in enumerate(df['Links']):
                loader = WebBaseLoader(link)
                docs = loader.load()
                result = stuff_chain.run(docs)
                results.append(result)

                # Update progress after processing each link
                progress = (index + 1) / total_links * 100

            # Add the results of the current prompt as a new column to the DataFrame
            column_name = f"Result_{prompt_text[:10]}..."  # Using the first 10 chars of prompt as column name for brevity
            df[column_name] = results

        save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'enriched.csv')
        df.to_csv(save_path, index=False)

        if not prompts:
            return render_template('sniffer.html', result="No prompts provided.", file_ready=False)
        else:
            return render_template('sniffer.html', result="Processing completed.", file_ready=True)

    return render_template('sniffer.html', result=None)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):  # Create upload folder if it doesn't exist
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
import os

import os
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

from flask import make_response

app = Flask(__name__)
progress = 0

# Declare a variable to hold the path of the processed CSV file
processed_csv_path = None



@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global processed_csv_path 
    global progress  # Declare the variable as global
    #progress = 0  # Reset progress at the start of an upload


    uploaded_file = request.files['csvFile']
    current_directory = os.path.dirname(os.path.abspath(__file__))
    upload_folder = os.path.join(current_directory, "uploads")
    filename = uploaded_file.filename

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, filename)  
    uploaded_file.save(file_path)

    # Read the uploaded CSV file using pandas
    df = pd.read_csv(file_path)
    links = df['Links'].tolist()

    questions = []
    for key, value in request.form.items():
        if key.startswith('question'):
            questions.append(value)

    total_links = len(links)
    total_questions = len(questions)
    total_operations = total_links * total_questions

    # Create a dictionary to store results
    results_dict = {question: [] for question in questions}

    model_name_p = request.form.get('model_name')
    temperature_p = float(request.form.get('temperature'))

    llm = ChatOpenAI(openai_api_key='',
                        temperature=temperature_p, model_name=model_name_p)

    for link in links:
        for question in questions:

            prompt_template = question + '\n"{text}"\nCONCISE SUMMARY:'     
            prompt = PromptTemplate.from_template(prompt_template)
            llm_chain = LLMChain(llm=llm, prompt=prompt)
            stuff_chain = StuffDocumentsChain(
                            llm_chain=llm_chain, document_variable_name="text"
                    )
            loader = WebBaseLoader(link)
            docs = loader.load()
            result = stuff_chain.run(docs)
            results_dict[question].append(result)

            progress += (1 / total_operations) * 100  # Increment by the percentage of one operation

            print(progress)


# Convert results_dict to DataFrame and concatenate with original DataFrame
    results_df = pd.DataFrame(results_dict)
    updated_df = pd.concat([df, results_df], axis=1)

    # Save the updated DataFrame back to CSV
    updated_df.to_csv(file_path, index=False)

    processed_csv_path = file_path  # This line is new

    time.sleep(5)  # Simulate processing time
    return redirect(url_for('success'))

@app.route('/progress')
def progress_route():
    global progress  # access the global variable
    return jsonify({"progress": progress})


@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/download')
def download():
    global processed_csv_path
    if processed_csv_path:
        return send_file(processed_csv_path, as_attachment=True)
    else:
        return "No file to download"


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
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

    file_path = os.path.join(upload_folder, filename)  
    uploaded_file.save(file_path)

    # Read the uploaded CSV file using pandas
    df = pd.read_csv(file_path)
    links = df['Links'].tolist()

    questions = []
    for key, value in request.form.items():
        if key.startswith('question'):
            questions.append(value)

    # Create a dictionary to store results
    results_dict = {question: [] for question in questions}
    llm = ChatOpenAI(openai_api_key='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',
                        temperature=0, model_name="gpt-3.5-turbo-16k")

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


# Convert results_dict to DataFrame and concatenate with original DataFrame
    results_df = pd.DataFrame(results_dict)
    updated_df = pd.concat([df, results_df], axis=1)

    # Save the updated DataFrame back to CSV
    updated_df.to_csv(file_path, index=False)

    time.sleep(5)  # Simulate processing time
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return "File uploaded successfully"

if __name__ == '__main__':
    app.run(debug=True)
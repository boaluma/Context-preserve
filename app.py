
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import pickle
from streamlit_extras.add_vertical_space import add_vertical_space
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI 
from langchain.chains.question_answering import load_qa_chain
import openai
 
# Sidebar contents
with st.sidebar:
    st.title('PDF Chat App')
    st.markdown('''
    ## About
    A chat app that takes in PDF and answers user query based on the info in the PDF file uploded \n
    Made using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model
 
    ''')
    add_vertical_space(5)
    st.write('Made with by Kunal Bitey')
 
os.environ["OPENAI_API_KEY"] = st.secrets["key"]
openai.api_key=os.environ["OPENAI_API_KEY"]
load_dotenv()

previous_conversation = []

def ask_question(question, context):
    global previous_conversation
    input_text = ''
    if previous_conversation:
        input_text = '\n'.join(f'Q: {q}\nA: {a}' for q, a in previous_conversation)
        input_text += f'\nQ: {question}\n'
    else:
        input_text = f'Q: {question}\n'

    input_text += context

    response = openai.Completion.create(
        engine="davinci", 
        prompt=input_text, 
        max_tokens=100
    )

    answer = response.choices[0].text.strip()
    previous_conversation.append((question, answer))
    return answer

 
def main():
    st.header("PDF Q&A app")
    
 
 
    # upload a PDF file
    pdf = st.file_uploader("Upload your PDF here", type='pdf')
 
    # st.write(pdf)
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
 
        # text_splitter = RecursiveCharacterTextSplitter(
        #     chunk_size=1000,
        #     chunk_overlap=200,
        #     length_function=len
        #     )
        # chunks = text_splitter.split_text(text=text)
 
        # # # embeddings
        # store_name = pdf.name[:-4]
        # st.write(f'{store_name}')
 
        # if os.path.exists(f"{store_name}.pkl"):
        #     with open(f"{store_name}.pkl", "rb") as f:
        #         VectorStore = pickle.load(f)
            
        # else:
        #     embeddings = OpenAIEmbeddings()
        #     VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
        #     with open(f"{store_name}.pkl", "wb") as f:
        #         pickle.dump(VectorStore, f)
 
        # Input user query
        query = st.text_input("Enter the question regarding your PDF :")
 
        if query:
            response = ask_question(query, text)
            st.write(response)
            # docs = VectorStore.similarity_search(query=query, k=5)
            # llm = OpenAI()
            # chain = load_qa_chain(llm=llm, chain_type="stuff")
            # response = chain.run(input_documents=docs, question=query)
            # st.write(response)
            
         
 
if __name__ == '__main__':
    main()

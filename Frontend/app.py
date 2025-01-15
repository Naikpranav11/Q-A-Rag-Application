import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.title("Q&A Chatbot with RAG")
st.sidebar.header("Upload PDF")
file_uploader = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])

if file_uploader:
    with open(file_uploader.name, "wb") as f:
        f.write(file_uploader.getbuffer())
    response = requests.post(f"{API_BASE}/upload/", json={"file_path": file_uploader.name})
    if response.status_code == 200:
        st.sidebar.success("PDF uploaded successfully!")
    else:
        st.sidebar.error("Failed to upload PDF.")

st.header("Ask a Question")
question = st.text_input("Your question")
if st.button("Submit"):
    response = requests.post(f"{API_BASE}/query/", json={"question": question})
    if response.status_code == 200:
        st.write("Answer:", response.json()["answer"])
    else:
        st.error("Failed to get an answer.")

#pdf loader aand other operations
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

#check pdf loading
def load_pdf_resume(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    resume_content = ""
    for page in docs:
        resume_content += page.page_content
    metadata = {
        "source": pdf_path,
        "page_count": len(docs)
    }
    return resume_content, metadata

#function to split the loaded pdf resume
def split_resume_text(resume_text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50,
                                                   separators=["\n\n", "\n", " ", ""])
    
    texts = text_splitter.split_text(resume_text)
    return texts

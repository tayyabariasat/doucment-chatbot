from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import PyPDF2
import spacy
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Tuple
from typing_extensions import Annotated

class Question(BaseModel):
    text: str
    
    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    answer: str
    confidence: float
    
    class Config:
        from_attributes = True

class DocumentProcessor:
    def __init__(self):
        self.documents = {}
        self.nlp = spacy.load('en_core_web_sm')
        self.vectorizer = TfidfVectorizer(stop_words='english')
        nltk.download('punkt', quiet=True)
        self.vectors = {}

    def extract_text(self, pdf_file: UploadFile) -> str:
        pdf_reader = PyPDF2.PdfReader(pdf_file.file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    def process_document(self, doc_id: str, text: str) -> None:
        sentences = nltk.sent_tokenize(text)
        # Create TF-IDF vectors for sentences
        vectors = self.vectorizer.fit_transform(sentences)
        
        self.documents[doc_id] = {
            'text': text,
            'sentences': sentences
        }
        self.vectors[doc_id] = vectors

    def get_answer(self, question: str, doc_id: str) -> Tuple[str, float]:
        if doc_id not in self.documents:
            raise HTTPException(status_code=404, detail="Document not found")
        # Transform question using the same vectorizer
        question_vector = self.vectorizer.transform([question])
        
        # Calculate similarity with all sentences
        similarities = cosine_similarity(question_vector, self.vectors[doc_id])[0]
        
        # Get the most similar sentence
        best_idx = np.argmax(similarities)
        confidence = float(similarities[best_idx])
        
        return self.documents[doc_id]['sentences'][best_idx], confidence

app = FastAPI()
processor = DocumentProcessor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_document(file: Annotated[UploadFile, File()]):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    doc_id = file.filename.replace('.pdf', '')
    text = processor.extract_text(file)
    processor.process_document(doc_id, text)
    
    return {"message": "Document processed successfully", "doc_id": doc_id}

@app.post("/chat/{doc_id}")
async def chat(doc_id: str, question: Question):
    answer, confidence = processor.get_answer(question.text, doc_id)
    return ChatResponse(answer=answer, confidence=confidence)

# Mount the static files directory
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

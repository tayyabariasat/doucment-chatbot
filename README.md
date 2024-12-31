# Document-based AI Chatbot

An AI-powered chatbot that answers questions based on uploaded PDF documents. This application uses state-of-the-art NLP models to provide accurate, contextual responses to user queries.

## Features

- PDF document upload and processing
- AI-powered question answering using RoBERTa model
- Real-time chat interface
- Docker support for easy deployment
- RESTful API endpoints

## Technical Stack

- Backend: FastAPI (Python)
- Frontend: HTML, CSS, JavaScript
- AI/ML: PyTorch, Transformers (RoBERTa)
- Document Processing: PyPDF2, NLTK
- Deployment: Docker

## Project Structure
```
document-chatbot/
├── app/
│   └── main.py
├── static/
│   └── index.html
├── Dockerfile
├── requirements.txt
└── README.md
```

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app/main.py
```


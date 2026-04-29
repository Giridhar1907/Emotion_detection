from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import predict_paragraph, get_labels
import nltk

# Ensure tokenizers are available
nltk.download('punkt', quiet=True)
try:
    nltk.download('punkt_tab', quiet=True)
except Exception:
    pass # just in case old nltk version

app = FastAPI()

# Add CORS middleware to allow requests from the extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    text: str


@app.post("/analyze")
def analyze(req: Request):
    probs, chunks = predict_paragraph(req.text)
    labels = get_labels(probs)

    return {
        "overall_emotions": labels,
        "chunks": chunks
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
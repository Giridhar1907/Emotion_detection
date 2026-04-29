from nltk.tokenize import sent_tokenize
import numpy as np
from model_loader import predict, label_names


def chunk_text(text, max_words=80):
    """Splits text into chunks of at most max_words to fit within transformer bounds."""
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        words = sentence.split()
        if current_length + len(words) > max_words and current_chunk:
            # Yield current chunk and reset
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
            
        # If a single sentence is incredibly long (e.g., no punctuation), we still try to chunk it
        if len(words) > max_words:
            # chunk the sentence itself
            for i in range(0, len(words), max_words):
                chunks.append(" ".join(words[i:i+max_words]))
        else:
            current_chunk.extend(words)
            current_length += len(words)
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks

def predict_paragraph(text):
    if not text.strip():
        # fallback for empty text
        return np.zeros(len(label_names)), []
        
    chunks = chunk_text(text)
    all_probs = []

    for chunk in chunks:
        probs = predict(chunk)
        all_probs.append(probs)

    if not all_probs:
         return np.zeros(len(label_names)), []

    # Aggregate using max and mean to favor the strongest emotion signal but temper it with mean
    final_probs = 0.7 * np.max(all_probs, axis=0) + 0.3 * np.mean(all_probs, axis=0)
    return final_probs, chunks


def get_labels(probs, top_k=5, min_score=0.1): 
    indices = probs.argsort()[::-1]

    results = []
    for i in indices:
        if probs[i] >= min_score:
            results.append({
                "label": label_names[i],
                "score": float(probs[i])
            })
        if len(results) == top_k:
            break

    return results
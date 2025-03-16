import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from retrieval import get_relevant_docs

DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_NAME = os.getenv("DATABASE_NAME", "rag_pg_db")
DB_USER = os.getenv("DATABASE_USER", "postgres")
DB_PASS = os.getenv("DATABASE_PASSWORD", "postgres")

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
gen_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

# Combine retrieved docs and query for input to LLM
def generate_answer(query, docs):
    context_str = "\n\n".join(docs)
    prompt = f"Context:\n{context_str}\n\nQuestion: {query}\nAnswer:"
    inputs = tokenizer(prompt, return_tensors='pt')
    outputs = gen_model.generate(
        **inputs,
        temperature=0.6,
        do_sample=True,
        max_new_tokens=80,
        num_beams=4,
        early_stopping=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Perform RAG
if __name__ == "__main__":
    rag_questions = [
    "What are examples of dynamically typed functional languages?",
    "Why is immutability important in functional programming?",
    "How do pure functional data structures prevent exponential memory growth?"]

    for question in rag_questions:
      docs = get_relevant_docs(question, k=1)
      answer = generate_answer(question, docs)
      print("\nQuery question: ", question)
      # print("Retrieved Docs:", docs, "\n\n") # optional see doc selections
      print("RAG answer: ", answer)
from retrieval import get_relevant_docs

if __name__ == "__main__":
    retrieval_questions = [
       "What are examples of dynamically typed functional languages?",
       "Why is immutability important in functional programming?",
       "How do pure functional data structures prevent exponential memory growth?"]

    for question in retrieval_questions:
      docs = get_relevant_docs(question, k=1)
      print("Query question: ", question)
      print("Query result (relevant chunk): ", docs, "\n\n")

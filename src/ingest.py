import os
import psycopg2
from sentence_transformers import SentenceTransformer

DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_NAME = os.getenv("DATABASE_NAME", "rag_poc_db")
DB_USER = os.getenv("DATABASE_USER", "postgres")
DB_PASS = os.getenv("DATABASE_PASSWORD", "postgres")

def main():
    # pgvector connection and init
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    create_table_query = """
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding vector(384)  -- or 768, etc.
    );
    """
    cur.execute(create_table_query)

    # Embedding model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Chunk synthetic text
    with open('./data/synthetic_wiki.txt', 'r') as f:
        text = f.read()
    chunk_size = 500
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start = end

    # Embeddings to Postgres
    embeddings = model.encode(chunks)
    insert_query = """
    INSERT INTO documents (content, embedding)
    VALUES (%s, %s::vector)
    """
    for chunk, emb in zip(chunks, embeddings):
        emb_str = "[" + ",".join(str(x) for x in emb) + "]"
        cur.execute(insert_query, (chunk, emb_str))

    # Clean up
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()

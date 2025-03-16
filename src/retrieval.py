import os
import psycopg2
from sentence_transformers import SentenceTransformer

DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_NAME = os.getenv("DATABASE_NAME", "rag_poc_db")
DB_USER = os.getenv("DATABASE_USER", "postgres")
DB_PASS = os.getenv("DATABASE_PASSWORD", "postgres")

embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Vector similarity search in postgres w/ pgvector
def get_relevant_docs(query, k=3):
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()

    q_emb = embedding_model.encode([query])[0]
    q_emb_str = "[" + ",".join([str(x) for x in q_emb]) + "]"

    sql = f"""
    SELECT content
    FROM documents
    ORDER BY embedding <-> %s::vector
    LIMIT {k};
    """
    cur.execute(sql, (q_emb_str,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [r[0] for r in rows]

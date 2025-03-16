import os
import psycopg2

DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_NAME = os.getenv("DATABASE_NAME", "rag_pg_db")
DB_USER = os.getenv("DATABASE_USER", "postgres")
DB_PASS = os.getenv("DATABASE_PASSWORD", "postgres")

def dump_embeddings_to_txt(output_file="./out/embedding_dump.txt", max_content_length=100):
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()
    cur.execute("SELECT id, content, embedding FROM documents;")
    rows = cur.fetchall()

    with open(output_file, "w", encoding="utf-8") as f:
        for (doc_id, content, embedding_str) in rows:
            embedding_vals = embedding_str.strip("[]").split(",")
            embedding_list = [float(x) for x in embedding_vals]
            structured_content = content[:max_content_length]
            if len(content) > max_content_length:
                structured_content += "..."
            f.write(f"ID: {doc_id}\n")
            f.write(f"Content: {structured_content}\n")
            f.write(f"Embedding: {embedding_list}\n")
            f.write("-" * 40 + "\n")

    cur.close()
    conn.close()
    print(f"Embedding dump written to {output_file}")

if __name__ == "__main__":
    dump_embeddings_to_txt()

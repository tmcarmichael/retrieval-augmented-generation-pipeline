# Retrieval Augmented Generation POC

Dockerized [RAG](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) pipeline testing retrieval of synthetic text injected into a Wikipedia article. Processes text with chunking and embedding [SentenceTransformers](https://sbert.net/), storing it in [Postgres](https://github.com/postgres/postgres) & [pgvector](https://github.com/pgvector/pgvector) for [similarity search](https://en.wikipedia.org/wiki/Similarity_search). Retrieves modified content and verifies synthetic insertions are returned. Feeds retrieved chunks into [huggingface google/flan-t5-small](https://huggingface.co/google/flan-t5-small) for query generation. `flan-t5-small` was chosen for [CPU support and efficiency in POC](https://huggingface.co/google/flan-t5-small#running-the-model-on-a-cpu). LLM APIs or GPU LLMs could further enhance augmented generation.

---

## Steps:

### Retrieval

_Pre-requisite: Docker Desktop (Windows, macOS, or Linux)_

1. Clone repo

2. Build and start containers

```bash
docker-compose up -d --build
```

3. Chunk and create embeddings

```bash
docker-compose exec app python ./src/ingest.py
```

4. Query the data (Retrieval without augmented generation)

```bash
docker-compose exec app python ./src/query.py
```

_For RAG, skip to step 5 in the section below._

5. **Optional**: Use custom query

```bash
docker-compose exec app python query.py "Why is immutability important in functional programmning"
```

6. **Optional**: Dump the embeddings

```bash
docker-compose exec app python ./src/dump_embeddings.py
```

7. **Optional**: Clean up

```bash
docker-compose down -v
```

### RAG with LLM

After embedding the query, retrieving the chunks, we feed these into a LLM for generating an answer using the chunks found. Follow steps 1-4 above and then:

5. RAG with LLM

```bash
docker-compose exec app python ./src/rag.py
```

6. **Optional**: Dump the embeddings

```bash
docker-compose exec app python ./src/dump_embeddings.py
```

_View in ./src/dump_embeddings.py or cat out._

7. **Optional**: Clean up

```bash
docker-compose down -v
```

# Retrieval Augmented Generation POC

[Retrieval Augmented Generation](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) Dockerized for POC. Synthetic text is injected into a Wikipedia article for testing retrieval and RAG.

Chunking and embedding with [SentenceTransformers](https://sbert.net/), and stores text in a Postgres & [pgvector vector DB](https://github.com/pgvector/pgvector). Queries the modified content via similarity search. Verifies synthetic insertions are actually retrieved and returned.

Finally, we feed the returned chunks to a small pretrained LLM, [huggingface google/flan-t5-small](https://huggingface.co/google/flan-t5-small), for RAG queries. 'flan-t5-small' is chosen as it can [run on CPU without significant hardware requirements](https://huggingface.co/google/flan-t5-small#running-the-model-on-a-cpu) for POC, however, APIs or GPU LLMs can be used for improved augmented generation.

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

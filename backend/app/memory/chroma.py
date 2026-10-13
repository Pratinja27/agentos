import chromadb

from ..config import settings


def _collection():
    client = chromadb.PersistentClient(path=settings.chroma_dir)
    return client.get_or_create_collection("agentos_memory")


def upsert_memory(item_id: int, kind: str, title: str, content: str) -> None:
    collection = _collection()
    collection.upsert(
        ids=[str(item_id)],
        documents=[f"{title}. {content}"],
        metadatas=[{"kind": kind, "title": title}],
    )


def query_memory(query: str, limit: int = 4) -> list[int]:
    collection = _collection()
    if collection.count() == 0:
        return []
    result = collection.query(query_texts=[query], n_results=min(limit, collection.count()))
    ids = result.get("ids", [[]])[0]
    return [int(item_id) for item_id in ids]

from src.ticket_agent.db.session import get_database
from src.ticket_agent.models.kb import KBDocument, KBSearchResult
from typing import List
from src.ticket_agent.config import settings

async def insert_kb_documents(kb_entries: List[KBDocument]) -> None:
    """
    Inserts a list of knowledge base entries into the MongoDB collection.

    Args:
        kb_entries (List[KBDocument]): A list of knowledge base documents to be inserted.
    """
    db = get_database()
    collection = db[settings.mongo.kb_collection]
    await collection.insert_many([entry.dict() for entry in kb_entries])


async def search_kb_documents(query_vector: List[float], top_k: int = 5) -> List[KBSearchResult]:
    db=get_database()
    collection = db[settings.mongo.kb_collection]
    pipeline = [
    {
        "$vectorSearch": {
            "index": "kb_vector_index",       # name of the Atlas Search index you create on this collection
            "path": "embedding",              # the field in your documents holding the vector
            "queryVector": query_vector,   # the embedding you're searching with
            "numCandidates": top_k * 10,      # how many candidates Mongo considers before narrowing down
            "limit": top_k,                   # how many results you actually want back
        }
    },
    {
        "$project": {
            "_id": 1,
            "title": 1,
            "content": 1,
            "category": 1,
            "score": {"$meta": "vectorSearchScore"},  # the similarity score gets attached here
        }
    },
]
    cursor = collection.aggregate(pipeline)
    results = []
    async for doc in cursor:
        # build a KBSearchResult from each returned doc
        result = KBSearchResult(document=KBDocument(**doc), similarity_score=doc["score"])
        results.append(result)
    return results

   


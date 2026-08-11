from src.ticket_agent.db.session import get_database

from src.ticket_agent.models.ticket import Ticket
from typing import List
from src.ticket_agent.config import settings

async def get_similar_tickets(query_vector: List[float],top_k: int = 5) -> List[Ticket]:
    """
    Retrieves tickets that are similar to the provided knowledge base entries.

    Args:
        kb_entries (List[KBDocument]): A list of knowledge base documents to find similar tickets for.

    Returns:
        List[Ticket]: A list of tickets that are similar to the provided knowledge base entries.
    """
    db = get_database()
    collection = db[settings.mongo.ticket_collection]
    
    # Extract the document IDs from the knowledge base entries
    pipeline = [
        {
            "$vectorSearch": {
                "index": "ticket_vector_index",       # name of the Atlas Search index you create on this collection
                "path": "embedding",              # the field in your documents holding the vector
                "queryVector": query_vector,   # the embedding you're searching with
                "numCandidates": top_k * 10,      # how many candidates Mongo considers before narrowing down
                "limit": top_k,                   # how many results you actually want back
            }
        },
        {
            "$project": {
               
                "ticket_id": 1,
                "title": 1,
                "description": 1,
                "status": 1,
                "priority": 1,
                "created_at": 1,
                "updated_at": 1,
               
            }
        },
    ]
    
    # Query the ticket collection for tickets that reference any of the provided document IDs
    cursor = collection.aggregate(pipeline)
    
    similar_tickets = []
    async for ticket_doc in cursor:
        similar_tickets.append(Ticket(**ticket_doc))
    
    return similar_tickets


async def insert_tickets(tickets: List[Ticket]) -> None:
    """
    Inserts a list of tickets into the MongoDB collection.

    Args:
        tickets (List[Ticket]): A list of tickets to be inserted.
    """
    db = get_database()
    collection = db[settings.mongo.ticket_collection]
    await collection.insert_many([ticket.model_dump() for ticket in tickets])
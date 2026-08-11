
from src.ticket_agent.db.ticket_store import get_similar_tickets
from src.ticket_agent.models.ticket import Ticket
from src.ticket_agent.tools.kb_retriever import generate_embeddings





async def search_similar_tickets(ticket: str,top_k: int) -> list[Ticket]:
    """
    Searches for similar tickets based on the provided ticket description.

    Args:
        ticket (str): A single ticket description for which embeddings are to be generated.
        top_k (int): The number of top matching tickets to retrieve.
    """
    embedings = await generate_embeddings(ticket)
    retrived_tickets = await get_similar_tickets(embedings, top_k)
    return retrived_tickets
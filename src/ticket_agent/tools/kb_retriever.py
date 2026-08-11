from src.config import settings
import cohere

from src.ticket_agent.models.kb import KBSearchResult

co = cohere.AsyncClient(settings.llm.cohere_api_key)

from src.ticket_agent.db.kb_store import search_kb_documents

async def generate_embeddings(text_input: str,input_type: str = "search_query") -> list[float]:
    """
    Generates embeddings for the provided text inputs using the Cohere API.

    Args:
        text_input (str): A single text input for which embeddings are to be generated.
    """
    response = await co.embed(
        inputs=[text_input],
        model="embed-v4.0",                 # Required: Choose your embedding model
        input_type=input_type,       # Required for semantic search (e.g., search_document, search_query, classification)
        embedding_types=["float"],          # Required: Output format (e.g., "float", "int8", "uint8", "binary")
    )
    return response.embeddings.float_[0]


async def search_knowledge_base(ticket: str, top_k: int) -> list[KBSearchResult]:
    """
    Generates embeddings for the provided ticket descriptions using the Cohere API.

    Args:
        ticket (str): A single ticket description for which embeddings are to be generated.
        top_k (int): The number of top matching tickets to retrieve.
    """
    embedings = await generate_embeddings(ticket)


    retrived_tickets = await search_kb_documents(embedings, top_k)
    return retrived_tickets
from typing import TypedDict, Annotated

from src.ticket_agent.models.ticket import Ticket, TicketPriority, TicketStatus
from src.ticket_agent.models.rca import RcaResponse
from src.ticket_agent.models.kb import KBSearchResult


class TriageWorkerState(TypedDict):
    """
    Represents the state of the Triage Worker agent in the triage process.
    """
    ticket_id: Annotated[str, "The unique identifier of the ticket being triaged."]
    ticket: Annotated[Ticket, "The ticket object containing details about the issue."]
    kb_search_results: Annotated[list[KBSearchResult], "A list of knowledge base search results relevant to the ticket."]
    similar_tickets: Annotated[list[Ticket], "A list of tickets that are similar to the current ticket based on embeddings."]
    rca: Annotated[RcaResponse, "Root Cause Analysis (RCA) for the ticket, if available."]
    error: Annotated[str, "Any error message encountered during the triage process, if applicable."]
    current_ticket_status: Annotated[TicketStatus, "The current status of the ticket (e.g., 'open', 'in_progress', 'resolved')."]
    triage_result: Annotated[TicketPriority, "The result of the triage process."]
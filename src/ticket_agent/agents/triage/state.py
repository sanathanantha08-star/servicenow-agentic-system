from typing import TypedDict, Annotated

from src.ticket_agent.models.ticket import Ticket, TicketPriority



class TriageWorkerState(TypedDict):
    """
    Represents the state of the Triage Worker agent in the triage process.
    """
    ticket: Annotated[Ticket, "The ticket object containing details about the issue."]
    triage_reason: Annotated[str, "The reason for the triage decision made by the agent."]
    triage_result: Annotated[TicketPriority, "The result of the triage process, indicating the priority level assigned to the ticket."]
    triage_error: Annotated[str, "Any error message encountered during the triage process, if applicable."]
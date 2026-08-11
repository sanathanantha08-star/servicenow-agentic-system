from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class TicketStatus(str,Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class TicketPriority(str,Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Ticket(BaseModel):
    ticket_id: str = Field(..., description="Unique identifier for the ticket")
    title: str = Field(..., description="Title of the ticket")
    description: str = Field(..., description="Detailed description of the ticket")
    status: TicketStatus= Field(..., description="Current status of the ticket (e.g., open, in_progress, resolved, closed)")
    priority: TicketPriority | None = Field(default=None, description="...")
    created_at: datetime = Field(..., description="Timestamp when the ticket was created")
    updated_at: datetime = Field(..., description="Timestamp when the ticket was last updated")
    embedding: list[float] | None = Field(default=None, description="Vector representation of the ticket for semantic search")
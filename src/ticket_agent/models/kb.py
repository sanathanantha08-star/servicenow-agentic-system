from pydantic import BaseModel, Field
from datetime import datetime

class KBDocument(BaseModel):
    document_id: str = Field(..., description="Unique identifier for the knowledge base document")
    title: str = Field(..., description="Title of the knowledge base document")
    content: str = Field(..., description="The main content of the knowledge base document")
    vectors: list[float] = Field(..., description="Vector representation of the document for semantic search")
    created_at: datetime = Field(..., description="Timestamp when the document was created")
    updated_at: datetime = Field(..., description="Timestamp when the document was last updated")
    category: str | None = Field(default=None, description="Category or tag associated with the document")

class KBSearchResult(BaseModel):
    document: KBDocument
    similarity_score: float = Field(..., description="Similarity score between the query and the document")
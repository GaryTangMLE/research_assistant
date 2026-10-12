"""State schema definition tracking the contextual timeline of the execution execution graph."""

from typing import TypedDict, List, Dict, Any, Optional, Literal
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field

class AgentVariables(BaseModel):
    """Internal control variables representing quality gates and path telemetry."""
    clarity_status: Literal["clear", "needs_clarification"] = "clear"
    confidence_score: float = Field(default=0.0, ge=0.0, le=10.0)
    validation_result: Literal["sufficient", "insufficient"] = "sufficient"
    research_attempts: int = Field(default=0, ge=0)
    identified_company: Optional[str] = None

class ResearchState(TypedDict):
    """The central state pattern shared dynamically between all graph nodes."""
    messages: List[BaseMessage]
    variables: AgentVariables
    raw_findings: Optional[Dict[str, Any]]
    final_summary: Optional[str]

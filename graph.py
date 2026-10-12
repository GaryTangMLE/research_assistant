"""Workflow orchestration layer establishing edge topologies and state serialization models."""

from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from state import ResearchState
from agents import ClarityAgent, ResearchAgent, ValidatorAgent, SynthesisAgent
from config import MAXIMUM_RESEARCH_ATTEMPTS
import logging

logger = logging.getLogger("MultiAgentSystem")

# Define explicit router logic maps
def route_clarity(state: ResearchState) -> Literal["__interrupt__", "research"]:
    """Conditional router pointing to an interaction breakpoint or a background query runner."""
    if state["variables"].clarity_status == "needs_clarification":
        return "__interrupt__"
    return "research"

def route_research(state: ResearchState) -> Literal["validator", "synthesis"]:
    """Inspects research confidence score metric lines to optimize processing."""
    if state["variables"].confidence_score < 6.0:
        return "validator"
    return "synthesis"

def route_validation(state: ResearchState) -> Literal["research", "synthesis"]:
    """Manages loops back to extraction, tracking boundaries via the counter state properties."""
    v_vars = state["variables"]
    if v_vars.validation_result == "insufficient" and v_vars.research_attempts < MAXIMUM_RESEARCH_ATTEMPTS:
        logger.info(f" -> Quality check failed. Retrying extraction loop: Attempt {v_vars.research_attempts} of {MAXIMUM_RESEARCH_ATTEMPTS}")
        return "research"
    return "synthesis"

# Initialize graph design
workflow = StateGraph(ResearchState)

# Append executable execution nodes
workflow.add_node("clarity", ClarityAgent.process)
workflow.add_node("research", ResearchAgent.process)
workflow.add_node("validator", ValidatorAgent.process)
workflow.add_node("synthesis", SynthesisAgent.process)

# Form mapping connections
workflow.add_edge(START, "clarity")

workflow.add_conditional_edges(
    "clarity",
    route_clarity,
    {
        "__interrupt__": "clarity",  # Loops back upon state resumption
        "research": "research"
    }
)

workflow.add_conditional_edges(
    "research",
    route_research,
    {
        "validator": "validator",
        "synthesis": "synthesis"
    }
)

workflow.add_conditional_edges(
    "validator",
    route_validation,
    {
        "research": "research",
        "synthesis": "synthesis"
    }
)

workflow.add_edge("synthesis", END)

# Configure internal memory layer
memory_checkpoint = MemorySaver()

# Compile the final execution engine runtime graph configuration
compiled_graph = workflow.compile(
    checkpointer=memory_checkpoint,
    interrupt_before=["clarity"]  # Enforces a step checkpoint interrupt gateway option
)

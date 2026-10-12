"""Specialized agent processing nodes managing decoupled operational domains."""

from typing import Dict, Any
from langchain_core.messages import AIMessage, HumanMessage
from state import ResearchState
from tools import CompanySearchTool
from config import MINIMUM_CONFIDENCE_SCORE
import logging

logger = logging.getLogger("MultiAgentSystem")


class ClarityAgent:
    """Reviews clarity and acts as a gateway validator for named entity data structures."""

    @staticmethod
    def process(state: ResearchState) -> Dict[str, Any]:
        logger.info("[Node Check] Entering ClarityAgent...")
        messages = state["messages"]
        current_vars = state["variables"]

        if not messages:
            current_vars.clarity_status = "needs_clarification"
            return {"variables": current_vars}

        # Scan last human statement
        last_user_message = [m for m in messages if isinstance(m, HumanMessage)][-1].content.lower()

        # Look for explicit company matches
        matched_company = None
        for company in ["apple", "tesla", "google"]:
            if company in last_user_message:
                matched_company = company
                break

        # Update control state properties
        if matched_company:
            current_vars.clarity_status = "clear"
            current_vars.identified_company = matched_company
        else:
            # If historical state context already established the target, maintain clarity path
            if current_vars.identified_company:
                current_vars.clarity_status = "clear"
            else:
                current_vars.clarity_status = "needs_clarification"

        return {"variables": current_vars}


class ResearchAgent:
    """Gathers facts dynamically utilizing historical feedback counters for alignment metrics."""

    @staticmethod
    def process(state: ResearchState) -> Dict[str, Any]:
        logger.info("[Node Check] Entering ResearchAgent...")
        messages = state["messages"]
        current_vars = state["variables"]

        last_user_message = [m for m in messages if isinstance(m, HumanMessage)][-1].content
        company = current_vars.identified_company

        # Increment operational attempts to power loop bounds checking routines
        current_vars.research_attempts += 1

        # Query our enterprise data resource wrapper
        findings = CompanySearchTool.search(last_user_message, target_company=company)

        # Simulating automated precision confidence mapping logic based on counter iterations
        if findings.get("status") == "success":
            # First attempt scores moderately; subsequent iterative validation runs boost score criteria
            if current_vars.research_attempts == 1:
                current_vars.confidence_score = 5.5  # Forces explicit validation loop route path verification
            else:
                current_vars.confidence_score = 8.5  # Loop bypass execution trigger met
        else:
            current_vars.confidence_score = 4.0

        return {
            "variables": current_vars,
            "raw_findings": findings
        }


class ValidatorAgent:
    """Inspects qualitative metrics against threshold ceilings before promotion routines."""

    @staticmethod
    def process(state: ResearchState) -> Dict[str, Any]:
        logger.info("[Node Check] Entering ValidatorAgent...")
        current_vars = state["variables"]
        findings = state["raw_findings"]

        # Enforce analytical constraints
        if current_vars.confidence_score >= MINIMUM_CONFIDENCE_SCORE and findings.get("status") == "success":
            current_vars.validation_result = "sufficient"
        else:
            current_vars.validation_result = "insufficient"

        return {"variables": current_vars}


class SynthesisAgent:
    """Assembles unstructured findings into cohesive, multi-turn aware markdown reporting blocks."""

    @staticmethod
    def process(state: ResearchState) -> Dict[str, Any]:
        logger.info("[Node Check] Entering SynthesisAgent...")
        findings = state["raw_findings"]
        company_meta = current_vars = state["variables"]

        data_block = findings.get("data", {})
        c_name = data_block.get("company_name", "Unknown Profile")
        news = data_block.get("recent_news", "N/A")
        stock = data_block.get("stock_info", "N/A")
        devs = data_block.get("key_developments", "N/A")

        summary_markdown = (
            f"### Executive Intelligence Report: {c_name}\n"
            f"* **Market Value Status:** {stock}\n"
            f"* **Current Headwinds & Press Index:** {news}\n"
            f"* **Strategic Horizons:** {devs}\n\n"
            f"*(Confidence Context Rating: {company_meta.confidence_score}/10.0 over {company_meta.research_attempts} pass queries)*"
        )

        outbound_message = AIMessage(content=summary_markdown)

        return {
            "final_summary": summary_markdown,
            "messages": [outbound_message]
        }

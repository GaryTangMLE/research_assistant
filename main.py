"""Execution runner verifying state tracking, manual injection overrides, and multi-turn loops."""

import uuid
from langchain_core.messages import HumanMessage
from graph import compiled_graph
from state import AgentVariables
import logging

# --- Configure Centralized Logging Architecture ---
logging.basicConfig(
    level=logging.INFO,
    # This format forces the ASCII timestamp to be the absolute first entry on every log line
    format="%(asctime)s | [%(levelname)s] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",  # Standardizes timestamp format explicitly
    handlers=[
        logging.FileHandler("research_assistant.log", mode="w"),  # Refreshes clean per run
        logging.StreamHandler()  # Keeps outputs real-time visible in PyCharm console
    ]
)
logger = logging.getLogger("MultiAgentSystem")


def display_latest_response(state_output: dict):
    """Helper method to display feedback."""
    if "final_summary" in state_output and state_output["final_summary"]:
        logger.info(f"\n[SYSTEM RESPONSE]\n{state_output['final_summary']}\n")
    else:
        logger.warning("\n[SYSTEM ALERT] Execution halted. System requires clearer inputs from user context loop.")


def execute_session_turn(thread_id: str, user_input: str):
    """Handles updating state data vectors across active communication execution configurations."""
    config = {"configurable": {"thread_id": thread_id}}

    # 1. Inspect current state status values
    current_state = compiled_graph.get_state(config)

    # If the system is currently paused at an interrupt checkpoint, update the conversation history
    if current_state.next:
        logger.info(f"\n--- Resuming Active Thread State: Input received -> '{user_input}' ---")
        compiled_graph.update_state(
            config,
            {"messages": [HumanMessage(content=user_input)]},
            as_node="clarity"
        )
        # Proceed with execution from the current execution checkpoint forward
        events = compiled_graph.stream(None, config, stream_mode="values")
    else:
        logger.info(f"\n--- Starting New Graph Path Pipeline Turn -> '{user_input}' ---")
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "variables": AgentVariables(),
            "raw_findings": None,
            "final_summary": None
        }
        events = compiled_graph.stream(initial_state, config, stream_mode="values")

    # 2. Iterate graph node operations processing execution passes
    final_output = {}
    for event in events:
        final_output = event

    # 3. Check for structural interrupts following the processing pass
    post_state = compiled_graph.get_state(config)
    if post_state.next:
        logger.warning(
            "\n[HUMAN IN THE LOOP INTERRUPT]: The query provided is too ambiguous. Please specify a targeted company profile.")
    else:
        display_latest_response(final_output)


def run_simulation():
    """Simulates a multi-turn user conversation scenario."""
    session_token = str(uuid.uuid4())
    logger.info(f"Initializing Multi-Agent Intelligence Network Thread: {session_token}")

    # --- TURN 1: Ambiguous Input (Triggers Clarity Interrupt Checkpoint) ---
    execute_session_turn(session_token, "Can you look up some general market stock details for me?")

    # --- TURN 2: Manual Injection Clarification (Resumes and Resolves Loop) ---
    execute_session_turn(session_token, "Oh sorry, I meant Apple please.")

    # --- TURN 3: Continuous Follow-up Tracking Context History ---
    execute_session_turn(session_token, "Excellent, now what are their key developments and news details?")


if __name__ == "__main__":
    run_simulation()

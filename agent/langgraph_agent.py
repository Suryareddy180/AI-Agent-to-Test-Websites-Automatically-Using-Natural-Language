"""
LangGraph Agent Module
Implements the agent workflow using LangGraph StateGraph.
Connects instruction parser → code generator pipeline.
"""

from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

from agent.instruction_parser import parse_instruction
from agent.code_generator import generate_playwright_code, generate_assertions


class AgentState(TypedDict):
    """State definition for the LangGraph workflow."""
    instruction: str
    parsed_actions: List[Dict[str, Any]]
    generated_code: str
    assertions: List[Dict[str, Any]]
    status: str
    error: str


def parse_node(state: AgentState) -> AgentState:
    """
    Node 1: Parse natural language instruction into structured actions.
    """
    try:
        instruction = state.get("instruction", "")
        parsed_actions = parse_instruction(instruction)
        
        return {
            **state,
            "parsed_actions": parsed_actions,
            "status": "parsed"
        }
    except Exception as e:
        return {
            **state,
            "error": f"Parse error: {str(e)}",
            "status": "error"
        }


def generate_code_node(state: AgentState) -> AgentState:
    """
    Node 2: Generate Playwright code from parsed actions.
    """
    try:
        parsed_actions = state.get("parsed_actions", [])
        
        # Generate Playwright script
        generated_code = generate_playwright_code(parsed_actions)
        
        # Generate assertions
        assertions = generate_assertions(parsed_actions)
        
        return {
            **state,
            "generated_code": generated_code,
            "assertions": assertions,
            "status": "code_generated"
        }
    except Exception as e:
        return {
            **state,
            "error": f"Code generation error: {str(e)}",
            "status": "error"
        }


def create_workflow() -> StateGraph:
    """
    Create and configure the LangGraph workflow.
    
    Pipeline: instruction → parse → generate_code → END
    """
    # Initialize the workflow with state schema
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("parse", parse_node)
    workflow.add_node("generate_code", generate_code_node)
    
    # Define edges (workflow connections)
    workflow.set_entry_point("parse")
    workflow.add_edge("parse", "generate_code")
    workflow.add_edge("generate_code", END)
    
    return workflow


# Compile the workflow once at module load
_workflow = create_workflow()
_compiled_workflow = _workflow.compile()


def handle_instruction(instruction: str) -> Dict[str, Any]:
    """
    Main entry point for processing natural language test instructions.
    
    Args:
        instruction: Natural language test case description
    
    Returns:
        Dictionary containing parsed actions, generated code, and assertions
    """
    # Initialize state
    initial_state: AgentState = {
        "instruction": instruction,
        "parsed_actions": [],
        "generated_code": "",
        "assertions": [],
        "status": "started",
        "error": ""
    }
    
    # Run the workflow
    try:
        result = _compiled_workflow.invoke(initial_state)
        
        return {
            "message": "Instruction processed successfully",
            "parsed_actions": result.get("parsed_actions", []),
            "generated_code": result.get("generated_code", ""),
            "assertions": result.get("assertions", []),
            "status": result.get("status", "unknown")
        }
    except Exception as e:
        return {
            "message": "Error processing instruction",
            "error": str(e),
            "status": "error"
        }

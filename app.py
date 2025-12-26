"""
Flask Application
Main entry point for the AI Web Testing Agent.
Provides REST API and serves the web interface.
"""

from flask import Flask, render_template, request, jsonify
from agent.langgraph_agent import handle_instruction

app = Flask(__name__)


@app.route("/")
def home():
    """Serve the main web interface."""
    return render_template("index.html")


@app.route("/test", methods=["POST"])
def test():
    """
    Process natural language test instruction.
    
    Request JSON: { "instruction": "natural language test case" }
    
    Returns:
        JSON with parsed actions, generated Playwright code, and assertions
    """
    data = request.get_json()
    instruction = data.get("instruction", "")
    
    if not instruction:
        return jsonify({
            "status": "error",
            "message": "No instruction provided"
        }), 400

    # Process instruction through LangGraph workflow
    result = handle_instruction(instruction)

    return jsonify({
        "status": "success",
        "instruction": instruction,
        "parsed_actions": result.get("parsed_actions", []),
        "generated_code": result.get("generated_code", ""),
        "assertions": result.get("assertions", []),
        "workflow_status": result.get("status", "unknown")
    })


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "AI Web Testing Agent"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

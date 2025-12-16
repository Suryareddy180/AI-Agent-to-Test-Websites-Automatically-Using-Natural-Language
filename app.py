from flask import Flask, render_template, request, jsonify
from agent.langgraph_agent import handle_instruction

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test", methods=["POST"])
def test():
    data = request.get_json()
    instruction = data.get("instruction")

    result = handle_instruction(instruction)

    return jsonify({
        "status": "success",
        "instruction": instruction,
        "agent_response": result
    })

if __name__ == "__main__":
    app.run(debug=True)

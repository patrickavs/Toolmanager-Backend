from flask import Flask, jsonify, request
from pymongo import MongoClient

from toolService import ToolService

app = Flask(__name__)

# Configure MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["toolmanagerDB"]
collection = db["tools"]

tool_service = ToolService(collection)


# Listing all tools
@app.route("/tools", methods=["GET"])
def get_all_tools():
    tools = tool_service.get_all_tools()
    return jsonify(tools)


# Getting a specific tool
@app.route("/tools/<tool_id>", methods=["GET"])
def get_tool(tool_id):
    tool = tool_service.get_tool(tool_id)
    if tool is None:
        return jsonify({"message": "Tool not found"}), 404
    return jsonify(tool)


# Adding a new tool
@app.route("/tools", methods=["POST"])
def add_tool():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    new_tool = tool_service.add_tool(data)
    return jsonify(new_tool), 201


# Updating a tool
@app.route("/tools/<tool_id>", methods=["PUT"])
def update_tool(tool_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    updated_tool = tool_service.update_tool(tool_id, data)
    if updated_tool is None:
        return jsonify({"message": "Tool not found"}), 404
    return jsonify(updated_tool)


# Deleting a tool
@app.route("/tools/<tool_id>", methods=["DELETE"])
def delete_tool(tool_id):
    deleted_count = tool_service.delete_tool(tool_id)
    if deleted_count == 0:
        return jsonify({"message": "Tool not found"}), 404
    return jsonify({"message": "Tool deleted"})


if __name__ == "__main__":
    app.run(debug=True)

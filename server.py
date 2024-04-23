from flask import Flask, jsonify, request
from pymongo import MongoClient

from toolService import ToolService
from materialService import MaterialService

app = Flask(__name__)

# Configure MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["toolmanagerDB"]
toolCollection = db["tools"]
materialCollection = db["materials"]

tool_service = ToolService(toolCollection)
material_service = MaterialService(materialCollection)

## Tools ##


# Listing all tools
@app.get("/tools")
def get_all_tools():
    tools = tool_service.get_all_tools()
    return jsonify(tools)


# Getting a specific tool
@app.get("/tools/<tool_id>")
def get_tool(tool_id):
    tool = tool_service.get_tool(tool_id)
    if tool is None:
        return jsonify({"message": "Tool not found"}), 404
    return jsonify(tool)


# Adding a new tool
@app.post("/tools")
def add_tool():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    new_tool = tool_service.add_tool(data)
    return jsonify(new_tool), 201


# Updating a tool
@app.put("/tools/<tool_id>")
def update_tool(tool_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    updated_tool = tool_service.update_tool(tool_id, data)
    if updated_tool is None:
        return jsonify({"message": "Tool not found"}), 404
    return jsonify(updated_tool)


# Deleting a tool
@app.delete("/tools/<tool_id>")
def delete_tool(tool_id):
    deleted_count = tool_service.delete_tool(tool_id)
    if deleted_count == 0:
        return jsonify({"message": "Tool not found"}), 404
    return jsonify({"message": "Tool deleted"})


## Materials ##


# Listing all materials
@app.get("/materials")
def get_all_materials():
    materials = material_service.get_all_materials()
    return jsonify(materials)


# Getting a specific material
@app.get("/materials/<material_id>")
def get_material(material_id):
    material = material_service.get_material(material_id)
    if material is None:
        return jsonify({"message": "Material not found"}), 404
    return jsonify(material)


# Adding a new material
@app.post("/materials")
def add_material():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    new_material = material_service.add_material(data)
    return jsonify(new_material), 201


# Updating a material
@app.put("/materials/<material_id>")
def update_material(material_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    updated_material = material_service.update_material(material_id, data)
    if updated_material is None:
        return jsonify({"message": "Material not found"}), 404
    return jsonify(update_material)


# Deleting a material
@app.delete("/materials/<material_id>")
def delete_material(material_id):
    deleted_count = material_service.delete_material(material_id)
    if deleted_count == 0:
        return jsonify({"message": "Material not found"}), 404
    return jsonify({"message": "Material deleted"})


if __name__ == "__main__":
    app.run(debug=True)

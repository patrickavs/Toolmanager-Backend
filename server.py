from flask import Flask, jsonify, request
from pymongo import MongoClient

from toolService import ToolService
from materialService import MaterialService
from userService import UserService

from bson import ObjectId

app = Flask(__name__)

# Configure MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["toolmanagerDB"]
toolCollection = db["tools"]
materialCollection = db["materials"]
userCollection = db["users"]

tool_service = ToolService(toolCollection)
material_service = MaterialService(materialCollection)
user_service = UserService(userCollection)

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


# Get materials for a tool
@app.get("/tools/<tool_id>/materials")
def get_materials_for_tool(tool_id):
    try:
        filter = {"_id": tool_id}
        tool = toolCollection.find_one(filter)

        if not tool:
            return [], 404

        material_ids = tool.get("materials", [])

        if not material_ids:
            return []

        materials = []
        for material_id in material_ids:
            material = material_service.get_material(material_id)
            if material:
                materials.append(material)

        return jsonify({f"materials for {tool['name']}:": materials})
    except (TypeError, ValueError):
        return jsonify({"message": "Invalid tool id"}), 400


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
    return jsonify(updated_material)


# Deleting a material
@app.delete("/materials/<material_id>")
def delete_material(material_id):
    deleted_count = material_service.delete_material(material_id)
    if deleted_count == 0:
        return jsonify({"message": "Material not found"}), 404
    return jsonify({"message": "Material deleted"})


# Get tools for a material
@app.get("/materials/<material_id>/tools")
def get_tools_for_material(material_id):
    try:
        filter = {"_id": material_id}
        material = materialCollection.find_one(filter)

        if not material:
            return [], 404

        tool_ids = material.get("tools", [])

        if not tool_ids:
            return []

        tools = []
        for tool_id in tool_ids:
            tool = tool_service.get_tool(tool_id)
            if tool:
                tools.append(tool)

        return jsonify({f"tools for {material['name']}": tools})
    except (TypeError, ValueError):
        return jsonify({"message": "Invalid tool id"}), 400


## User ##


# Listing all users
@app.get("/users")
def get_all_users():
    users = user_service.get_all_users()
    return jsonify(users)


# Getting a specific user
@app.get("/users/<user_id>")
def get_user(user_id):
    user = user_service.get_user(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user)


# Adding a new user
@app.post("/users")
def add_material():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    new_user = user_service.add_user(data)
    return jsonify(new_user), 201


# Updating a user
@app.put("/users/<user_id>")
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    updated_user = user_service.update_user(user_id, data)
    if updated_user is None:
        return jsonify({"message": "User not found"}), 404
    return jsonify(updated_user)


# Deleting a user
@app.delete("/users/<user_id>")
def delete_user(user_id):
    deleted_count = user_service.delete_user(user_id)
    if deleted_count == 0:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"message": "User deleted"})


if __name__ == "__main__":
    app.run(debug=True)

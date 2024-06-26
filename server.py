from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import timedelta
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from werkzeug.security import generate_password_hash, check_password_hash

from toolService import ToolService
from materialService import MaterialService
from userService import UserService
import os
from bson import ObjectId

# Load .env variables
load_dotenv()

# Placeholder for token blacklist
blacklist = set()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=3)
jwt = JWTManager(app)

# Configure MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["toolmanagerDB"]
toolCollection = db["tools"]
materialCollection = db["materials"]
userCollection = db["users"]

tool_service = ToolService(toolCollection)
material_service = MaterialService(materialCollection)
user_service = UserService(userCollection, toolCollection, materialCollection)

## Tools ##


# Listing all tools
@app.get("/tools/all")
def get_all_tools():
    tools, status = tool_service.get_all_tools()
    return jsonify(tools), status


# Getting a specific tool
@app.get("/tools/<tool_id>")
def get_tool(tool_id):
    tool, status = tool_service.get_tool(tool_id)
    if status != 200:
        return jsonify(tool), status
    return jsonify(tool), status


# Adding a new tool
@app.post("/tools")
def add_tool():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    new_tool, status = tool_service.add_tool(data)
    return jsonify(new_tool), status


# Updating a tool
@app.put("/tools/<tool_id>")
def update_tool(tool_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    updated_tool, status = tool_service.update_tool(tool_id, data)
    return jsonify(updated_tool), status


# Deleting a tool
@app.delete("/tools/<tool_id>")
def delete_tool(tool_id):
    message, status = tool_service.delete_tool(tool_id)
    return jsonify(message), status


# Get materials for a tool
@app.get("/tools/<tool_id>/materials")
def get_materials_for_tool(tool_id):
    try:
        filter = {"_id": tool_id}
        tool = toolCollection.find_one(filter)
        if not tool:
            return jsonify({"message": "Tool not found"}), 404
        material_ids = tool.get("materials", [])
        materials = [
            material_service.get_material(material_id) for material_id in material_ids
        ]
        return jsonify({"materials": materials}), 200
    except (TypeError, ValueError):
        return jsonify({"message": "Invalid tool ID"}), 400


## Materials ##


# Listing all materials
@app.get("/materials/all")
def get_all_materials():
    materials, status = material_service.get_all_materials()
    return jsonify(materials), status


# Getting a specific material
@app.get("/materials/<material_id>")
def get_material(material_id):
    material, status = material_service.get_material(material_id)
    return jsonify(material), status


# Adding a new material
@app.post("/materials")
def add_material():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    new_material, status = material_service.add_material(data)
    return jsonify(new_material), status


# Updating a material
@app.put("/materials/<material_id>")
def update_material(material_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    updated_material, status = material_service.update_material(material_id, data)
    return jsonify(updated_material), status


# Deleting a material
@app.delete("/materials/<material_id>")
def delete_material(material_id):
    message, status = material_service.delete_material(material_id)
    return jsonify(message), status


# Get tools for a material
@app.get("/materials/<material_id>/tools")
def get_tools_for_material(material_id):
    try:
        filter = {"_id": material_id}
        material = materialCollection.find_one(filter)
        if not material:
            return jsonify({"message": "Material not found"}), 404
        tool_ids = material.get("tools", [])
        tools = [tool_service.get_tool(tool_id) for tool_id in tool_ids]
        return jsonify({"tools": tools}), 200
    except (TypeError, ValueError):
        return jsonify({"message": "Invalid material ID"}), 400


## User Management ##


# Listing all users
@app.get("/users")
def get_all_users():
    users, status = user_service.get_all_users()
    return jsonify(users), status


# Getting a specific user or the currently logged-in user
@app.get("/users/<email>")
@jwt_required()
def get_user(email):
    user, status = user_service.get_user(email)
    if status != 200:
        return jsonify({"message": "User not found"}), status
    return jsonify(user), status


# Adding a new user
@app.post("/users")
@jwt_required()
def add_user():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    new_user, status = user_service.add_user(data)
    return jsonify(new_user), status


# Updating a user
@app.put("/users/<email>")
@jwt_required()
def update_user(email):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    updated_user, status = user_service.update_user(email, data)
    return jsonify(updated_user), status


# Deleting a user
@app.delete("/users/<email>")
@jwt_required()
def delete_user(email):
    message, status = user_service.delete_user(email)
    return jsonify(message), status


# Listing all materials
@app.get("/users/<email>/materials")
@jwt_required()
def get_all_materials_for_user(email):
    materials, status = user_service.get_all_materials_for_user(email)
    return jsonify(materials), status


# Listing all tools
@app.get("/users/<email>/tools")
@jwt_required()
def get_all_tools_for_user(email):
    tools, status = user_service.get_all_tools_for_user(email)
    return jsonify(tools), status


# Add tool to user
@app.post("/users/<email>/tools")
@jwt_required()
def add_tool_for_user(email):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    new_tool, status = user_service.add_tool_for_user(email, data)
    return jsonify(new_tool), status


# Add material to user
@app.post("/users/<email>/materials")
@jwt_required()
def add_material_for_user(email):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing data"}), 400
    new_material, status = user_service.add_material_for_user(email, data)
    return jsonify(new_material), status


# Remove tool from user
@app.delete("/users/<email>/tools/<tool_id>")
@jwt_required()
def remove_tool_from_user(email, tool_id):
    message, status = user_service.remove_tool_from_user(email, tool_id)
    return jsonify(message), status


# Remove material from user
@app.delete("/users/<email>/materials/<material_id>")
@jwt_required()
def remove_material_from_user(email, material_id):
    message, status = user_service.remove_material_from_user(email, material_id)
    return jsonify(message), status


## Authentication ##


# Check if JWT-Token wasn't already in use
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blacklist


# Register a new user
@app.post("/api/register")
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data["password"])
    user_data = {
        "_id": str(ObjectId()),
        "name": data["name"],
        "email": data["email"],
        "password": hashed_password,
        "profilePic": "",
        "aboutMe": "",
        "bio": "",
        "tools": [],
        "materials": [],
    }
    new_user, status = user_service.add_user(user_data)
    return jsonify(new_user), status


# Login a user
@app.post("/api/login")
def login():
    data = request.get_json()
    user = userCollection.find_one({"email": data["email"]})
    if user and check_password_hash(user["password"], data["password"]):
        access_token = create_access_token(identity=user["email"])
        return jsonify({"access_token": access_token}), 200
    return jsonify({"message": "Invalid credentials"}), 401


# Logout a user
@app.post("/api/logout")
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200


if __name__ == "__main__":
    app.run(debug=True)

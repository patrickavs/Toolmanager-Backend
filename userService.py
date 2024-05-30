from pymongo.errors import DuplicateKeyError


class UserService:

    def __init__(self, collection, tool_service, material_service):
        self.collection = collection
        self.tool_service = tool_service
        self.material_service = material_service

    def get_all_users(self):
        try:
            users = list(self.collection.find())
            return users, 200
        except Exception as e:
            return {"message": str(e)}, 500

    def get_user(self, email):
        try:
            filter = {"email": email}
            user = self.collection.find_one(filter)
            if user is None:
                return {"message": "User not found"}, 404
            return user, 200
        except (TypeError, ValueError):
            return {"message": "Invalid user ID"}, 400

    def add_user(self, data):
        try:
            if self.collection.find_one({"email": data["email"]}):
                return {"message": "User with the given email already exists"}, 409
            inserted_id = self.collection.insert_one(data).inserted_id
            return {"_id": str(inserted_id)}, 201
        except DuplicateKeyError:
            return {"message": "User with the given ID already exists"}, 409
        except Exception as e:
            return {"message": str(e)}, 500

    def update_user(self, email, data):
        try:
            filter = {"email": email}
            update = {"$set": data}
            updated_count = self.collection.update_one(filter, update).matched_count
            if updated_count == 0:
                return {"message": "User not found"}, 404
            return self.collection.find_one(filter), 200
        except (TypeError, ValueError):
            return {"message": "Invalid user ID or data"}, 400
        except Exception as e:
            return {"message": str(e)}, 500

    def delete_user(self, email):
        try:
            filter = {"email": email}
            deleted_count = self.collection.delete_one(filter).deleted_count
            if deleted_count == 0:
                return {"message": "User not found"}, 404
            return {"message": "User deleted"}, 200
        except (TypeError, ValueError):
            return {"message": "Invalid user ID"}, 400
        except Exception as e:
            return {"message": str(e)}, 500

    def get_all_tools(self, email):
        try:
            user, status_code = self.get_user(email)
            if status_code != 200:
                return user, status_code

            tool_ids = user.get("tools", [])
            tools = []
            for tool_id in tool_ids:
                tool, tool_status_code = self.tool_service.get_tool(tool_id)
                if tool_status_code == 200:
                    tools.append(tool)
            return {"tools": tools}, 200
        except Exception as e:
            return {"message": str(e)}, 500

    def get_all_materials(self, email):
        try:
            user, status_code = self.get_user(email)
            if status_code != 200:
                return user, status_code

            material_ids = user.get("materials", [])
            materials = []
            for material_id in material_ids:
                material, material_status_code = self.material_service.get_material(
                    material_id
                )
                if material_status_code == 200:
                    materials.append(material)
            return {"materials": materials}, 200
        except Exception as e:
            return {"message": str(e)}, 500

    def add_tool_to_user(self, email, tool_id):
        try:
            user, status_code = self.get_user(email)
            if status_code != 200:
                return user, status_code

            if "tools" not in user:
                user["tools"] = []

            if tool_id in user["tools"]:
                return {"message": "Tool already added to the user"}, 409

            user["tools"].append(tool_id)
            self.update_user(email, {"tools": user["tools"]})
            return {"message": "Tool added successfully"}, 200
        except Exception as e:
            return {"message": str(e)}, 500

    def add_material_to_user(self, email, material_id):
        try:
            user, status_code = self.get_user(email)
            if status_code != 200:
                return user, status_code

            if "materials" not in user:
                user["materials"] = []

            if material_id in user["materials"]:
                return {"message": "Material already added to the user"}, 409

            user["materials"].append(material_id)
            self.update_user(email, {"materials": user["materials"]})
            return {"message": "Material added successfully"}, 200
        except Exception as e:
            return {"message": str(e)}, 500

    def delete_tool_from_user(self, email, tool_id):
        try:
            user, status_code = self.get_user(email)
            if status_code != 200:
                return user, status_code

            if "tools" in user and tool_id in user["tools"]:
                user["tools"].remove(tool_id)
                self.update_user(email, {"tools": user["tools"]})
                return {"message": "Tool removed from user successfully"}, 200
            return {"message": "Tool not found in user's tools"}, 404
        except Exception as e:
            return {"message": str(e)}, 500

    def delete_material_from_user(self, email, material_id):
        try:
            user, status_code = self.get_user(email)
            if status_code != 200:
                return user, status_code

            if "materials" in user and material_id in user["materials"]:
                user["materials"].remove(material_id)
                self.update_user(email, {"materials": user["materials"]})
                return {"message": "Material removed from user successfully"}, 200
            return {"message": "Material not found in user's materials"}, 404
        except Exception as e:
            return {"message": str(e)}, 500

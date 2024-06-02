from pymongo.errors import DuplicateKeyError


class UserService:

    def __init__(self, collection, toolCollection, materialCollection):
        self.collection = collection
        self.toolCollection = toolCollection
        self.materialCollection = materialCollection

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

    def get_all_tools_for_user(self, email):
        try:
            user_response, status_code = self.get_user(email)
            if status_code != 200:
                return user_response, status_code

            user = user_response
            tool_ids = user.get("tools", [])
            if not tool_ids:
                return {"tools": []}, 200

            tools = []
            for tool_id in tool_ids:
                tool = self.toolCollection.find_one({"_id": tool_id})
                if tool:
                    tools.append(tool)

            return tools, 200
        except Exception as e:
            print("Error getting tools for user")
            return {"message": str(e)}, 500

    def get_all_materials_for_user(self, email):
        try:
            user_response, status_code = self.get_user(email)
            if status_code != 200:
                return user_response, status_code

            user = user_response
            material_ids = user.get("materials", [])
            if not material_ids:
                return {"materials": []}, 200

            materials = []
            for material_id in material_ids:
                material = self.materialCollection.find_one({"_id": material_id})
                if material:
                    materials.append(material)

            return materials, 200
        except Exception as e:
            print("Error getting materials for user")
            return {"message": str(e)}, 500

    def add_tool_for_user(self, email, tool_data):
        try:
            # Insert tool into tools collection
            tool_id = tool_data.get("_id")

            # Update user document to include new tool's ID
            filter = {"email": email}
            update = {"$addToSet": {"tools": str(tool_id)}}
            updated_count = self.collection.update_one(filter, update).matched_count

            if updated_count == 0:
                return {"message": "User not found"}, 404

            return {"tool_id": str(tool_id)}, 201
        except Exception as e:
            return {"message": str(e)}, 500

    def add_material_for_user(self, email, material_data):
        try:
            # Insert material into materials collection
            material_id = material_data.get("_id")

            # Update user document to include new material's ID
            filter = {"email": email}
            update = {"$addToSet": {"materials": str(material_id)}}
            updated_count = self.collection.update_one(filter, update).matched_count

            if updated_count == 0:
                return {"message": "User not found"}, 404

            return {"material_id": str(material_id)}, 201
        except Exception as e:
            return {"message": str(e)}, 500

    def remove_tool_from_user(self, email, tool_id):
        try:
            # Remove the tool's ID from the user's document
            filter = {"email": email}
            update = {"$pull": {"tools": tool_id}}
            updated_count = self.collection.update_one(filter, update).matched_count

            if updated_count == 0:
                return {"message": "User not found"}, 404

            return {"message": "Tool removed from user"}, 200
        except Exception as e:
            return {"message": str(e)}, 500

    def remove_material_from_user(self, email, material_id):
        try:
            # Remove the material's ID from the user's document
            filter = {"email": email}
            update = {"$pull": {"materials": material_id}}
            updated_count = self.collection.update_one(filter, update).matched_count

            if updated_count == 0:
                return {"message": "User not found"}, 404

            return {"message": "Material removed from user"}, 200
        except Exception as e:
            return {"message": str(e)}, 500

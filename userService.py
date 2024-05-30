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
            user = self.get_user(email)
            tool_ids = user.get("tools", [])
            tools = []
            for tool_id in tool_ids:
                tool = self.toolCollection.get_tool(tool_id)
                tools.append(tool)
            return {"tools": tools}
        except Exception as e:
            print("Error getting tools for user")
            return {"message": str(e)}, 500

    def get_all_materials_for_user(self, email):
        try:
            user = self.get_user(email)
            material_ids = user.get("materials", [])
            materials = []
            for material_id in material_ids:
                material = self.materialCollection.get_material(material_id)
                materials.append(material)
            return {"materials": materials}
        except Exception as e:
            print("Error getting materials for user")
            return {"message": str(e)}, 500

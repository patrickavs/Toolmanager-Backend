from pymongo.errors import DuplicateKeyError


class ToolService:

    def __init__(self, collection):
        self.collection = collection

    def get_all_tools(self):
        try:
            return list(self.collection.find()), 200
        except Exception as e:
            return {"message": str(e)}, 500

    def get_tool(self, tool_id):
        try:
            filter = {"_id": tool_id}
            tool = self.collection.find_one(filter)
            if tool:
                return tool, 200
            return {"message": "Tool not found"}, 404
        except (TypeError, ValueError) as e:
            return {"message": str(e)}, 400

    def add_tool(self, data):
        try:
            inserted_id = self.collection.insert_one(data).inserted_id
            return str(inserted_id), 201
        except DuplicateKeyError:
            return {"message": "Duplicate key error"}, 409
        except Exception as e:
            return {"message": str(e)}, 500

    def update_tool(self, tool_id, data):
        try:
            filter = {"_id": tool_id}
            update = {"$set": data}
            updated_count = self.collection.update_one(filter, update).matched_count
            if updated_count == 0:
                return {"message": "Tool not found"}, 404
            return self.collection.find_one(filter), 200
        except (TypeError, ValueError) as e:
            return {"message": str(e)}, 400

    def delete_tool(self, tool_id):
        try:
            filter = {"_id": tool_id}
            deleted_count = self.collection.delete_one(filter).deleted_count
            if deleted_count == 0:
                return {"message": "Tool not found"}, 404
            return {"message": "Tool deleted"}, 200
        except (TypeError, ValueError) as e:
            return {"message": str(e)}, 400

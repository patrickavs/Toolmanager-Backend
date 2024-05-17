from pymongo.errors import DuplicateKeyError


class ToolService:

    def __init__(self, collection):
        self.collection = collection

    def get_all_tools(self):
        return list(self.collection.find())

    def get_tool(self, tool_id):
        try:
            filter = {"_id": tool_id}
            return self.collection.find_one(filter)
        except (TypeError, ValueError):
            return None, 400

    def add_tool(self, data):
        try:
            inserted_id = self.collection.insert_one(data).inserted_id
            return inserted_id
        except DuplicateKeyError:
            return None, 409

    def update_tool(self, tool_id, data):
        try:
            filter = {"_id": tool_id}
            update = {"$set": data}
            updated_count = self.collection.update_one(filter, update).matched_count
            if updated_count == 0:
                return None, 404
            return self.collection.find_one(filter)
        except (TypeError, ValueError):
            return None, 400

    def delete_tool(self, tool_id):
        try:
            filter = {"_id": tool_id}
            deleted_count = self.collection.delete_one(filter).deleted_count
            return deleted_count
        except (TypeError, ValueError):
            return None, 400

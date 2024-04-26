from pymongo.errors import DuplicateKeyError
from materialService import MaterialService


class ToolService:

    def __init__(self, collection):
        self.collection = collection

    def get_all_tools(self):
        return list(self.collection.find())

    def get_tool(self, tool_id):
        filter = {"_id": tool_id}
        return self.collection.find_one(filter)

    def add_tool(self, data):
        try:
            inserted_id = self.collection.insert_one(data).inserted_id
            return self.collection.find_one({"_id": inserted_id})
        except DuplicateKeyError:
            return None, 409

    def update_tool(self, tool_id, data):
        filter = {"_id": tool_id}
        update = {"$set": data}
        updated_count = self.collection.update_one(filter, update).matched_count
        if updated_count == 0:
            return None, 404
        return self.collection.find_one(filter)

    def delete_tool(self, tool_id):
        filter = {"_id": tool_id}
        deleted_count = self.collection.delete_one(filter).deleted_count
        return deleted_count

    def get_materials_for_tool(self, tool_id):
        filter = {"_id": tool_id}
        tool = self.collection.find_one(filter)
        if not tool:
            return []

        material_ids = tool.get("materials", [])

        if not material_ids:
            return []

        materials = []
        for material_id in material_ids:
            material = MaterialService.get_material(material_id)
            if material:
                materials.append(material)
        return materials

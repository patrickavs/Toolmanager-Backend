from bson import ObjectId
from pymongo.errors import DuplicateKeyError


class MaterialService:

    def __init__(self, collection):
        self.collection = collection

    def get_all_materials(self):
        return list(self.collection.find())

    def get_material(self, material_id):
        try:
            filter = {"_id": material_id}
            return self.collection.find_one(filter)
        except (TypeError, ValueError):
            return None, 400

    def add_material(self, data):
        try:
            inserted_id = self.collection.insert_one(data).inserted_id
            return inserted_id
        except DuplicateKeyError:
            return None, 409

    def update_material(self, material_id, data):
        try:
            filter = {"_id": material_id}
            update = {"$set": data}
            updated_count = self.collection.update_one(filter, update).matched_count
            if updated_count == 0:
                return None, 404
            return self.collection.find_one(filter)
        except (TypeError, ValueError):
            return None, 400

    def delete_material(self, material_id):
        try:
            filter = {"_id": material_id}
            deleted_count = self.collection.delete_one(filter).deleted_count
            return deleted_count
        except (TypeError, ValueError):
            return None, 400

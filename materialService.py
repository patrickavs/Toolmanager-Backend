from bson import ObjectId
from pymongo.errors import DuplicateKeyError


class MaterialService:

    def __init__(self, collection):
        self.collection = collection

    def get_all_materials(self):
        return list(self.collection.find())

    def get_material(self, material_id):
        try:
            # Convert string id to ObjectId before finding
            object_id = ObjectId(material_id)
            filter = {"_id": object_id}
            return self.collection.find_one(filter)
        except (TypeError, ValueError):
            # Handle potential exceptions for invalid ObjectIds
            return None, 400  # Bad Request

    def add_material(self, data):
        try:
            inserted_id = self.collection.insert_one(data).inserted_id
            # No need to query again, return the inserted_id which is an ObjectId
            return inserted_id
        except DuplicateKeyError:
            return None, 409

    def update_material(self, material_id, data):
        try:
            # Convert string id to ObjectId before finding
            object_id = ObjectId(material_id)
            filter = {"_id": object_id}
            update = {"$set": data}
            updated_count = self.collection.update_one(filter, update).matched_count
            if updated_count == 0:
                return None, 404
            return self.collection.find_one(filter)
        except (TypeError, ValueError):
            # Handle potential exceptions for invalid ObjectIds
            return None, 400  # Bad Request

    def delete_material(self, material_id):
        try:
            # Convert string id to ObjectId before deleting
            object_id = ObjectId(material_id)
            filter = {"_id": material_id}
            deleted_count = self.collection.delete_one(filter).deleted_count
            return deleted_count
        except (TypeError, ValueError):
            # Handle potential exceptions for invalid ObjectIds
            return None, 400  # Bad Request

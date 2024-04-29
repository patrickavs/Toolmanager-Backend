from pymongo.errors import DuplicateKeyError


class MaterialService:

    def __init__(self, collection):
        self.collection = collection

    def get_all_materials(self):
        return list(self.collection.find())

    def get_material(self, material_id):
        filter = {"_id": material_id}
        return self.collection.find_one(filter)

    def add_material(self, data):
        try:
            inserted_id = self.collection.insert_one(data).inserted_id
            return self.collection.find_one({"_id": inserted_id})
        except DuplicateKeyError:
            return None, 409

    def update_material(self, material_id, data):
        filter = {"_id": material_id}
        update = {"$set": data}
        updated_count = self.collection.update_one(filter, update).matched_count
        if updated_count == 0:
            return None, 404
        return self.collection.find_one(filter)

    def delete_material(self, material_id):
        filter = {"_id": material_id}
        deleted_count = self.collection.delete_one(filter).deleted_count
        return deleted_count

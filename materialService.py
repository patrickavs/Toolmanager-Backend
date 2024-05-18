from pymongo.errors import DuplicateKeyError


class MaterialService:

    def __init__(self, collection):
        self.collection = collection

    def get_all_materials(self):
        try:
            materials = list(self.collection.find())
            return materials, 200
        except Exception as e:
            return {"message": str(e)}, 500

    def get_material(self, material_id):
        try:
            filter = {"_id": material_id}
            material = self.collection.find_one(filter)
            if material is None:
                return {"message": "Material not found"}, 404
            return material, 200
        except (TypeError, ValueError):
            return {"message": "Invalid material ID"}, 400

    def add_material(self, data):
        try:
            inserted_id = self.collection.insert_one(data).inserted_id
            return {"_id": str(inserted_id)}, 201
        except DuplicateKeyError:
            return {"message": "Material with the given ID already exists"}, 409
        except Exception as e:
            return {"message": str(e)}, 500

    def update_material(self, material_id, data):
        try:
            filter = {"_id": material_id}
            update = {"$set": data}
            updated_count = self.collection.update_one(filter, update).matched_count
            if updated_count == 0:
                return {"message": "Material not found"}, 404
            return self.collection.find_one(filter), 200
        except (TypeError, ValueError):
            return {"message": "Invalid material ID or data"}, 400
        except Exception as e:
            return {"message": str(e)}, 500

    def delete_material(self, material_id):
        try:
            filter = {"_id": material_id}
            deleted_count = self.collection.delete_one(filter).deleted_count
            if deleted_count == 0:
                return {"message": "Material not found"}, 404
            return {"message": "Material deleted"}, 200
        except (TypeError, ValueError):
            return {"message": "Invalid material ID"}, 400
        except Exception as e:
            return {"message": str(e)}, 500

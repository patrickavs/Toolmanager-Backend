from pymongo.errors import DuplicateKeyError


class UserService:

    def __init__(self, collection):
        self.collection = collection

    def get_all_users(self):
        try:
            users = list(self.collection.find())
            return users, 200
        except Exception as e:
            return {"message": str(e)}, 500

    def get_user(self, user_id):
        try:
            filter = {"_id": user_id}
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

    def update_user(self, user_id, data):
        try:
            filter = {"_id": user_id}
            update = {"$set": data}
            updated_count = self.collection.update_one(filter, update).matched_count
            if updated_count == 0:
                return {"message": "User not found"}, 404
            return self.collection.find_one(filter), 200
        except (TypeError, ValueError):
            return {"message": "Invalid user ID or data"}, 400
        except Exception as e:
            return {"message": str(e)}, 500

    def delete_user(self, user_id):
        try:
            filter = {"_id": user_id}
            deleted_count = self.collection.delete_one(filter).deleted_count
            if deleted_count == 0:
                return {"message": "User not found"}, 404
            return {"message": "User deleted"}, 200
        except (TypeError, ValueError):
            return {"message": "Invalid user ID"}, 400
        except Exception as e:
            return {"message": str(e)}, 500

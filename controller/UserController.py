from interface.IController import IController
from model.UserModel import UserModel
class UserController(IController):
    def __init__(self):
        pass
    
    def get(arg):
         return {"success": "call User get successfully!"}
    
    def post():
        userModel = UserModel()
        created = userModel.create("anton@gmail.com","123456","Anton")
        if not created: 
            return {"failure by create object"}
        return {"success": "user created successfully"}
    
    def destroy(id):
        model = UserModel()
        result = model.remove(id)
        if not result:
            return {"failure to destroy user"}
        return {"success": "user destroyed successfully"}
    
    def put(arg,data):
        return {"success": "user updated successfully"}
    

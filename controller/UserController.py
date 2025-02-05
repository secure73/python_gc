from interface.IController import IController
from model.UserModel import UserModel
from helper.HTTP_Response import HTTP_Response
class UserController(IController):
    def __init__(self):
        pass
    
    def get(self):
         response = HTTP_Response()
         response.success({"message":"it is successfull"})
         return
    
    def post(self,data):
        userModel = UserModel()
        created = userModel.create("anton@gmail.com","123456","Anton")
        if not created: 
            return {"failure by create object"}
        return {"success": "user created successfully"}
    
    def destroy(self,data):
        model = UserModel()
        result = model.remove(id)
        if not result:
            return {"failure to destroy user"}
        return {"success": "user destroyed successfully"}
    
    def put(self,data):
        response = HTTP_Response()
        response.success(data)
    

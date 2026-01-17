from ._imports import *

class UserValidationUtility():
    def __init__(self):
        pass
    
    
    
    def validate_user_request(self, model:UserModel)->UserModel:
        if model == None:
            model = UserModel()
            model.IsInvalid = True
            model.Message = "Invalid user model"
            return model
        request = model.request
        if request == None:
            model.request = UserRequest()
            model.request.IsInvalid = True
            model.request.Message = "Invalid user request"
            model.IsInvalid = True
            model.Message = "Invalid user request"
            return model
        
        if request.UserId <= 0:
            model.IsInvalid = True
            model.Message = "Invalid user Id"
            return model
        
        model.item = UserItem()
        model.item.Id = request.Id
        model.item.UserId = request.UserId
        model.item.Name = request.Name
        model.IsInvalid = False
        
        return model
    
    




    def validate_user_model(self, model:UserModel)->UserModel:
        if model == None:
            model = UserModel()
            model.IsInvalid = True
            model.Message = "Invalid user model"
            return model
        if model.item == None:
            model.item = UserItem()
            model.IsInvalid = True
            model.Message = "Invalid user item"
            return model
        return model
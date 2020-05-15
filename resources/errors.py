errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "EmailAlreadyExistsError": {
         "message": "User with given email address already exists",
         "status": 409
     },
     "StateAlreadyExistsError": {
         "message": "State already exists",
         "status": 409
     },
     "UnauthorizedError": {
         "message": "Invalid username or password",
         "status": 401
     },
     "NoAuthorizationError": {
         "message": "Unauthorized access. A token is needed to access this feature",
         "status": 401
     },
     "NoDataReceived":{
         "message": 'No Data Receivied',
         "status": 324
     }
}

class InternalServerError(Exception):
    
    def __init__(self):
        pass

    def __call__(self):
        return errors["InternalServerError"]

class SchemaValidationError(Exception):
    
    def __init__(self):
        pass
    def __call__(self):
        return errors["SchemaValidationError"]

class EmailAlreadyExistsError(Exception):

    def __init__(self):
        pass
    def __call__(self):
        return errors["EmailAlreadyExistsError"]

class StateAlreadyExistsError(Exception):

    def __init__(self):
        pass
    def __call__(self):
        return errors["StateAlreadyExistsError"]

class UnauthorizedError(Exception):
    
    def __init__(self):
        pass
    def __call__(self):
        return errors["UnauthorizedError"]

class NoAuthorizationError(Exception):
    def __init__(self):
        pass
    def __call__(self):
        return errors["NoAuthorizationError"]

class NoDataReceived(Exception):
    def __init__(self):
        pass
    def __call__(self):
        return errors["NoDataReceived"]
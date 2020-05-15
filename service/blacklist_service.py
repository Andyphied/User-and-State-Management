from task.auth_task import save_token


def store_token(token):

    save_token.delay(token) # Saves token
    
    response_object = {
        'status': 'success',
        'message': 'Successfully logged out.'
    }
    return response_object, 200
    
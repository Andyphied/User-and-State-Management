from app import celery
from database.collections import State

@celery.task()
def save_state(data):
    user = State()
    user.store_state(data)
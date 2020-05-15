from app import celery
from database.collections import Blacklist_Token, User


@celery.task()
def save_user(data):
    user = User()
    user.store_user(data)


@celery.task()
def save_admin(data):
    user = User()
    user.store_admin(data)


@celery.task()
def save_blacklist_token(data):
    user = Blacklist_Token()
    user.store_blacklist_token(data)

@celery.task()
def save_state(data):
    user = State()
    user.store_state(data)
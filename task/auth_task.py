from app import celery
from database.collections import Blacklist_Token



@celery.task()
def save_token(token):
    user = Blacklist_Token()
    user.store_blacklist_token(token)
import uuid
from datetime import datetime, timedelta
from db.connection import SConnection

def signin(login, password):
    # check
    res = SConnection().signin_check(login, password)
    if not res: return None
    # new session
    uid = res[0]['uid']
    sid = str(uuid.uuid4())
    expired = datetime.now() + timedelta(days=2)
    res = SConnection().signin_new_session(sid, uid, expired)
    if res[1] != 1: return None
    return sid
    
def signup(login, password):
    # new user
    res = SConnection().signup(login, password)
    return res[1] == 1


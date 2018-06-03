import uuid
from datetime import datetime, timedelta
from db.connection import SConnection

def signin(login, password):
    with SConnection().__lock__:
        # check
        res = SConnection().__signin_check__(login, password)
        if not res: return None
        # new session
        uid = res[0]['uid']
        sid = str(uuid.uuid4())
        expired = datetime.now() + timedelta(days=2)
        res = SConnection().__signin_new_session__(sid, uid, expired)
        if res[1] != 1: return None
        return sid

def signup(login, password):
    # new user
    with SConnection().__lock__:
        res = SConnection().__signup__(login, password)
        return res[1] == 1

def check_expired(sid):
    SConnection().remove_expired()
    with SConnection().__lock__:
        res = SConnection().__check_sid__(sid)
    print (res)
    return len(res) == 0

def get_projects(sid):
    with SConnection().__lock__:
        result = SConnection().__get_projects__(sid)
    return result

def add_project(sid, pname):
    with SConnection().__lock__:
        result = SConnection().__add_project__(sid, pname)
    return result

def add_olymp(sid, name, start, end):
    with SConnection().__lock__:
        result = SConnection().__add_olymp__(sid, name, start, end)
    return result

def save_project(*args):
    print(args)
    with SConnection().__lock__:
        result = SConnection().__save_project__(*args)
    return result

def load_project(sid, pid):
    with SConnection().__lock__:
        result = SConnection().__get_project__(sid, pid)
    return result

def load_olymps_as_author(sid):
    with SConnection().__lock__:
        result = SConnection().__get_olymps_author__(sid)
    return result

def load_olymps_as_user(sid):
    with SConnection().__lock__:
        result = SConnection().__get_olymps_user__(sid)
    return result

def load_olymps_open():
    with SConnection().__lock__:
        result = SConnection().__get_olymps_open__()
    return result

def publish_task(r):
    with SConnection().__lock__:
        r['oid'] = int(r['oid'])
        res = SConnection().__check_for_project_author__(r['pid'], r['sid'])
        if len(res) == 0: return None
        res = SConnection().__check_for_olymp_author__(r['oid'], r['sid'])
        if len(res) == 0: return None
        result = SConnection().__publish__(r['pid'], r['description'], r['name'], r['oid'])
    return result

def tryRegister(sid, oid):
    with SConnection().__lock__:
        if not SConnection().__get_reg__(sid, oid):
            SConnection().__register__(sid, oid)

def loadOlymp(sid, oid):
    with SConnection().__lock__:
        attempts = SConnection().__get_attempts__(sid, oid)
        # TODO: load tasks names instead
        tasks = SConnection().__get_tasks__(oid)
        results = SConnection().__get_results__(oid)
    return {'attempts':attempts, 'tasks':tasks, 'results':results}

def load_task_data(tid):
    with SConnection().__lock__:
        result = SConnection().__load_task_data__(tid)
    return result

def set_result(result, sid, tid):
    with SConnection().__lock__:
        result = SConnection().__add_attempt__(result, sid, tid)
    return result

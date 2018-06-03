import postgresql
import metas
from config import SConfig


class SConnection(metaclass=metas.Singleton):
    def __init__(self):
        self.path = SConfig().DATABASE
        self.db = postgresql.open(self.path)
        # do 'prepare'
        self.signin_check = self.db.prepare('select uid from users where login = $1 and password = $2')
        self.signin_new_session = self.db.prepare('insert into sessions (sid, uid, expired) values($1, $2, $3)')
        self.signup = self.db.prepare('insert into users (login, password) values ($1, $2)')

    def execute(self, query):
        print (query)
        result = None
        if isinstance(query, list):
            with self.db.xact() as xact:
                result = map(self.db.query, query)
        else:
            result = self.db.query(query)
        print (result)
        return result


# todo: trigger romoving expired

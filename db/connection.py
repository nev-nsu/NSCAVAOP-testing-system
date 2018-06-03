import postgresql
from threading import Lock
import metas
from config import SConfig


class SConnection(metaclass=metas.Singleton):
    def __init__(self):
        self.path = SConfig().DATABASE
        self.db = postgresql.open(self.path)
        self.__lock__ = Lock()
        # do 'prepare'
        self.__signin_check__ = self.db.prepare('select uid from users where \
            login = $1 and password = $2')
        self.__signin_new_session__ = self.db.prepare('insert into sessions \
            (sid, uid, expired) values($1, $2, $3)')
        self.__signup__ = self.db.prepare('insert into users (login, password) \
            values ($1, $2)')
        self.__check_sid__ = self.db.prepare('select * from sessions where sid = $1 and expired > now()')
        self.__check_for_project_author__ = self.db.prepare('select * from projects where \
            pid = $1 and author in (select uid from sessions \
            where sid = $2 and expired > now())')
        self.__check_for_olymp_author__ = self.db.prepare('select * from olymps where \
            oid = $1 and author in (select uid from sessions \
            where sid = $2 and expired > now())')
        self.__get_projects__ = self.db.prepare('select * from projects where \
            author in (select uid from sessions where sid = $1 and expired > now())')
        self.__add_project__ = self.db.prepare('insert into projects (author, name) values \
            ((select uid from sessions where sid = $1 and expired > now()), $2)')
        self.__get_project__ = self.db.prepare('select * from projects where \
            author in (select uid from sessions where sid = $1 and expired > now()) and pid = $2')
        self.__save_project__ = self.db.prepare('update projects set  \
            code = $3, optimization = $4, tests = $5, verifier = $6, response_type = $7 where \
            author in (select uid from sessions where sid = $1 and expired > now()) and pid = $2')
        self.__get_olymps_author__ = self.db.prepare('select oid, name from olymps \
            where author in (select uid from sessions where sid = $1 and expired>now())')
        self.__get_olymps_user__ = self.db.prepare('select oid, name from olymps \
            where oid in (select oid from registrations \
            where uid in (select uid from sessions where sid = $1 and expired>now()))')
        self.__get_olymps_open__ = self.db.prepare('select oid, name from olymps \
            where start_time > now()')
        self.__add_olymp__ = self.db.prepare('insert into olymps (author, name, start_time, end_time) values \
            ((select uid from sessions where sid = $1 and expired > now()), \
            $2, (select to_timestamp($3, \'DD.MM.YYYY HH24:MI:SS\')), \
            (select to_timestamp($4, \'DD.MM.YYYY HH24:MI:SS\')))')
        self.__publish__ = self.db.prepare('insert into tasks (oid, name, description, pid) values ( \
            $4, $3, $2, $1)')
        self.__get_attempts__ = self.db.prepare('select * from attempts \
            where tid in (select tid from tasks where oid = $2) and \
            uid in (select uid from sessions where sid = $1)')
        self.__get_tasks__ = self.db.prepare('select * from tasks where oid = $1')
        self.__get_results__ = self.db.prepare('select users.login, sum(result) as scores from attempts, users \
            where users.uid = attempts.uid and tid in (select tid from tasks where oid = $1) \
            group by users.login order by scores')
        self.__get_reg__ = self.db.prepare('select * from registrations where oid = $2 and uid in \
            (select uid from sessions where sid = $1)')
        self.__register__ = self.db.prepare('insert into registrations (uid, oid) values \
            ((select uid from sessions where sid = $1), $2)')
        self.__load_task_data__ = self.db.prepare('select * from projects \
            where pid = (select pid from tasks where tid = $1)')
        self.__add_attempt__ = self.db.prepare('insert into attempts (tid, uid, result) values \
            ($3, (select uid from sessions where sid = $2), $1)')
        self.__get_tests__ = self.db.prepare('select tests from projects, tasks \
            where projects.pid = tasks.pid and tasks.tid = $1')

    def remove_expired(self):
        with SConnection().__lock__:
            self.db.query('delete from sessions where expired < now()')

    def execute(self, query):
        with SConnection().__lock__:
            print (query)
            result = None
            if isinstance(query, list):
                with self.db.xact() as xact:
                    result = map(self.db.query, query)
            else:
                result = self.db.query(query)
            print (result)
            return result

    def lock(self):
        self.__lock__.acquire()

    def unlock(self):
        self.__lock__.release()

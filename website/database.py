import mysql.connector


# If something went wrong (exception)
def mysql_error(err):
    print("Something went wrong: {}".format(err))


class DataBase:
    def __init__(self, user, password):
        self.cnx = None
        self.cursor = None
        self.config = {'user': user,
                       'password': password,
                       'host': '127.0.0.1',
                       'database': 'dormitory',
                       'raise_on_warnings': True}

    def connect(self):
        self.cnx = mysql.connector.connect(**self.config)
        self.cursor = self.cnx.cursor()

    def close(self):
        self.cursor.close()
        self.cnx.close()

    def commit(self):
        self.cnx.commit()

    def rollback(self):
        self.cnx.rollback()

    def call_procedure(self, procedure, args=()):

        self.connect()
        try:
            result = self.cursor.callproc(procedure, args)
            self.commit()
            return result
        except mysql.connector.Error as err:
            self.rollback()
            mysql_error(err)
            return None
        finally:
            self.close()

    def query(self, query, args=()):
        self.connect()
        try:
            _query = (query)
            self.cursor.execute(_query, args)
            result = self.cursor.fetchall()
            self.commit()
            return result
        except mysql.connector.Error as err:
            self.rollback()
            mysql_error(err)
            return None
        finally:
            self.close()


UserDB = DataBase('admin', 'admin')

AdminDB = DataBase('admin', 'admin')

ReceptionDB = DataBase('reception', 'reception')

CleanerDB = DataBase('cleaner', 'cleaner')


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

    def call_procedure(self, procedure, args=()):

        self.connect()
        try:
            self.cursor.callproc(procedure, args)
            self.commit()
        except mysql.connector.Error as err:
            mysql_error(err)
        finally:
            self.close()

    def query(self, query, args=()):
        self.connect()
        try:
            _query = (query)
            self.cursor.execute(_query, args)
            self.commit()
        except mysql.connector.Error as err:
            mysql_error(err)
            return err
        finally:
            self.close()

        return self.cursor


import mysql.connector

# If something went wrong (exception)
def mysql_error(err):
    print("Something went wrong: {}".format(err))


class ReceptionDB:
    config = {'user': 'reception',
              'password': 'reception',
              'host': '127.0.0.1',
              'database': 'dormitory',
              'raise_on_warnings': True}

# View users
    @staticmethod
    def view_user(id_user=None, fiscal_code=None):
        cnx = mysql.connector.connect(**ReceptionDB.config)
        cursor = cnx.cursor()
        # If parameters are not passed it returns all users
        if id_user is None and fiscal_code is None:
            query = ("SELECT * FROM user")
        else:
            query = ("SELECT * FROM user WHERE id_user = %s or fiscal_code = %s")

        try:
            result = cursor.execute(query, (id_user, fiscal_code))
            cursor.close()
            cnx.close()
            return result
        except mysql.connector.Error as err:
            mysql_error(err)


    def create_user






class CleanerDB:
    config = {'user': 'database',
              'password': 'database',
              'host': '127.0.0.1',
              'database': 'dormitory',
              'raise_on_warnings': True}


class AdminDB:
    config = {'user': 'admin',
              'password': 'admin',
              'host': '127.0.0.1',
              'database': 'dormitory',
              'raise_on_warnings': True}

    @staticmethod
    def register_user(matr, username, fisc_code, passw, name, surname, gender, role):
        cnx = mysql.connector.connect(**AdminDB.config)
        cursor = cnx.cursor()

        if role == 'admin' or 'staff':
            data_staff = (username, fisc_code, passw, name, surname, gender, role)
            add_staff = ("INSERT INTO staff(s_fiscal_code, password, s_name, s_surname, s_gender, role)"
                       "VALUES (%s, %s, %s, %s, %s, %s)")
            cursor.execute(add_staff, data_staff)
        else:
            add_student = (
                "INSERT INTO student(matriculation_number, fiscal_code, password, name, surname, gender, role)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s)")
            data_student = (matr, fisc_code, passw, name, surname, gender, role)
            cursor.execute(add_student, data_student)

        cnx.commit()
        cursor.close()
        cnx.close()

    @staticmethod
    def check_staff(username, password):
        cnx = mysql.connector.connect(**AdminDB.config)
        cursor = cnx.cursor()
        args = (username, password, 0)
        result = cursor.callproc('check_staff', args)
        cursor.close()
        cnx.close()
        return result[2]


class UserDB:
    config = {'user': 'progetto',
              'password': 'progetto',
              'host': '127.0.0.1',
              'database': 'dormitory',
              'raise_on_warnings': True}

    @staticmethod
    def register_user(matr, fisc_code, passw, name, surname, gender, role):
        cnx = mysql.connector.connect(**UserDB.config)
        cursor = cnx.cursor()
        add_student = ("INSERT INTO student(matriculation_number, fiscal_code, password, name, surname, gender, role)"
                       "VALUES (%s, %s, %s, %s, %s, %s, %s)")

        data_student = (matr, fisc_code, passw, name, surname, gender, role)

        cursor.execute(add_student, data_student)
        cnx.commit()
        cursor.close()
        cnx.close()

    @staticmethod
    def check_user(username, password):
        cnx = mysql.connector.connect(**UserDB.config)
        cursor = cnx.cursor()
        args = (username, password, 0)
        result = cursor.callproc('check_user', args)
        cursor.close()
        cnx.close()
        return result[2]

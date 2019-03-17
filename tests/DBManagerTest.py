from src.DBManager import DBManager


def test_connect():
    try:
        DBManager.connect()
        DBManager.create_tables()
        if DBManager.db is False:
            return False
        return True
    except Exception as ex:
        return False


def test_dump():
    users = ["Riccardo", "Giuseppe Palazzolo", "Angelo D'Amante", "Fabio Zappardino", "Nicola Carchaxjia",
             "Federico Vaccaro", "Tommaso Marigo"]
    path = "D:\\GDrive\\CiarcaVicchio\\_chat.txt"
    count = 100000
    try:
        DBManager.dump(users, path, count)
        return True
    except Exception as ex:
        print(str(ex))
        return False

def test_suite():
    res = True

    res = res & test_connect()

    res = res & test_dump()

    DBManager.query('SELECT * FROM ImportedMessages')

    return res


print(test_suite())

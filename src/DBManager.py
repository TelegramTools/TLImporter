import datetime, sqlite3, os, progressbar


class DBManager:

    db = None

    @staticmethod
    def connect():
        if DBManager.db is None:
            try:
                DBManager.db = sqlite3.connect("TLImporter-DB.db")
            except sqlite3.OperationalError:
                print("ERROR 1: DATABASE OPERATION ERROR!")
        return DBManager.db

    @staticmethod
    def create_tables():
        cursor = DBManager.db.cursor()
        cursor.execute('''CREATE TABLE ImportedMessages(User1 BOOLEAN, Sender TEXT, Date TEXT, Message TEXT)''')
        cursor.execute('''CREATE TABLE SentMessagesIDs(User1 INTEGER, User2 INTEGER)''')
        cursor.execute('''CREATE TABLE Statistics(User1ID INTEGER, User2ID INTEGER, NameUser1 TEXT, NameUser2 
        TEXT, TotalCountUser1 INTEGER, TotalCountUser2 INTEGER, AffectedMessages INTEGER, SoloMode BOOLEAN)''')

        cursor.execute('''CREATE TABLE Settings(NameUser1 TEXT, NameUser2 TEXT, FileName TEXT, FilePath TEXT, 
        SoloMode BOOLEAN)''')

        cursor.execute('''CREATE TABLE Version(AppName TEXT, AppVersion TEXT, CreationDate TEXT)''')
        DBManager.db.commit()
        date = str(datetime.datetime.today())
        reg = ("TLImporter", "3.0", date)
        DBManager.db.execute("INSERT INTO Version VALUES(?,?,?)", reg)
        DBManager.db.commit()

    @staticmethod
    def dump(users, file_path, total_count):
        bar = progressbar.ProgressBar(max_value=total_count)
        bar.start()
        completed = 0
        with open(file_path, mode="r", encoding="utf-8") as f:
            db = DBManager.connect()
            for line in f:
                for us in users:
                    if line.find("] " + us + ":") != -1:
                            header, msg = line.split("] " + us + ": ")  # FIXME not sure about the dots
                            reg4 = (True, us, header, msg)
                            db.execute("INSERT INTO ImportedMessages VALUES(?,?,?,?)", reg4)
                            completed = completed + 1
                            break
            db.commit()
            bar.finish()


    @staticmethod
    def query(quer):
        cursor = DBManager.db.cursor()
        res = DBManager.db.execute(quer)
        for r in res:
            print(str(r) + "\n")

    @staticmethod
    def commit():
        pass

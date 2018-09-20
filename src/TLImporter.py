import datetime
import getpass
import logging
import shutil
import sqlite3
import sys
import time
from os import mkdir
import cryptg
from cryptg import *

import progressbar  # progressbar2 module
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from telethon.crypto import AuthKey
from telethon.tl.functions.messages import *
from telethon.tl.types import *
from telethon.utils import *
from telethon.sessions import *
import pyAesCrypt

api_id = ##INSERT YOUR API ID HERE
api_hash = ##INSERT YOUR APIHASH HERE
TLdevice_model = 'Desktop device'
TLsystem_version = 'Console'
TLapp_version = '- TLImporter 3.0.1'
TLlang_code = 'en'
TLsystem_lang_code = 'en'
SelfUser1 = None
user1 = None
user2 = None
SelfUser2 = None
User1IDs = []
User2IDs = []
NoTimestamps = False
AppendHashtag = False
SendDatabase = True
SecretMode = False
EndDate = True
ExceptionReached = False
SoloImporting = False
ValidFile = False
Hashtag = "\n#TLImporter"
FilePath = None
NameUser1 = None
NameUser2 = None
incorrectname = "This name is not valid. Please, try again, with a correct name: "
LineCount = 0
User1Count = 0
User2Count = 0
TotalCount = 0
RawLoopCount = 0
Filename = None
client2 = None
dialogs = None
ChosenChat = None
password = ##THIS IS THE PASSWORD THAT WILL BE USED TO ENCRYPT DATABASES USING TLSecret. YOU MUST USE THE SAME PASSWORD IN THE RECEIVING APP AND TLSECRET.
bufferSize = 64 * 1024
SecretMessage = None

client1 = TelegramClient('User1', api_id, api_hash, device_model=TLdevice_model, system_version=TLsystem_version, app_version=TLapp_version, lang_code=TLlang_code, system_lang_code=TLsystem_lang_code)

def sprint(string, *args, **kwargs):
    #Safe Print (handle UnicodeEncodeErrors on some terminals)
    try:
        print(string, *args, **kwargs)
    except UnicodeEncodeError:
        string = string.encode('utf-8', errors='ignore')\
                       .decode('ascii', errors='ignore')
        print(string, *args, **kwargs)

def PrintChatList():
    global dialogs
    while True:
        dialogs = client1.get_dialogs(limit=None)
        i = None
        while i is None:
            print("This is your chat list:\n\n")
            for i, dialog in enumerate(dialogs, start=1):
                if get_display_name(dialog.entity) is "":
                    name = "Deleted Account"
                elif isinstance(dialog.entity, InputPeerSelf):
                    name = "Chat with yourself (Saved Messages)"
                else:
                    name = get_display_name(dialog.entity)
                sprint('{}. {}'.format(i, name))

            print()
            print('> Who is your partner?')
            print('> Available commands:')
            print('  !q: Quits the dialogs window and exits.')
            print('  !l: Logs out, terminating this session.')
            print()
            i = input('Enter dialog ID or a command to continue: ')
            if i is None:
                continue
            if i == '!q':
                sys.exit()
            if i == '!l':
                client1.log_out()
                sys.exit()
        try:
            i = int(i if i else 0) - 1
            # Ensure it is inside the bounds, otherwise retry
            dialog_count = dialogs.total
            if not 0 <= i < dialog_count:
                i = None
        except:
            i = None
            print("That's not a valid Chat. Please, try again.")
            continue

            # Retrieve the selected user (or chat, or channel)
        return dialogs[i].entity

def EventHandler(event):
    global SecretMessage
    if getattr(event.original_message, 'media', None):
        if isinstance(event.original_message.media, (MessageMediaDocument, Document)):
            for attr in event.original_message.media.document.attributes:
                if isinstance(attr, DocumentAttributeFilename):
                    if attr.file_name == "DB.aes":
                        print("\nResponse received! Processing...")
                        try:
                            os.remove("DB.aes")
                        except:
                            pass
                        client1.download_media(event.original_message)
                        SecretMessage = client1.send_message(ChosenChat, "WooHoo!")
                        client1.disconnect()
    return

def StartClient1():
    global SelfUser1
    global client1
    try:
        client1.connect()
        if not client1.is_user_authorized():
            client1.start(force_sms=False)
        SelfUser1 = client1.get_me()
    except:
        if not client1.is_connected():
            getpass.getpass("You are not connected to the internet or the phone was given in the incorrect format. Check your connection and press ENTER to try again: ")
        StartClient1()
    return

def StartClient2():
    global SelfUser2
    global client2
    try:
        client2.connect()
        if not client2.is_user_authorized():
            client2.start(force_sms=False)
        SelfUser2 = client2.get_me()
    except:
        if not client2.is_connected():
            getpass.getpass(
            "You are not connected to the internet or the phone was given in the incorrect format. Check your connection and press ENTER to try again: ")
        StartClient1()
    return

def StartSecretMode():
    global dialogs, ChosenChat, password, bufferSize, client2, SecretMessage
    getpass.getpass("\n\nYou have chosen to use the Telegram Tool's secret mode for logging your partner in Telegram.\nNow, it's time to choose your partner in your chat list. Press ENTER to continue: ")
    print("Gathering your chat list...")
    ChosenChat = PrintChatList()
    dialogs.clear()
    print("\n\nWaiting for a response from your partner...")
    client1.add_event_handler(EventHandler, events.NewMessage(chats=ChosenChat, incoming=True))
    client1.run_until_disconnected()
    pyAesCrypt.decryptFile("DB.aes", "TempDB.session", password, bufferSize)
    old_db = sqlite3.connect('TempDB.session')
    db = old_db.cursor()
    db.execute('SELECT * FROM sessions')
    List = []
    for row in db:
        List.append(row[0])
        List.append(row[1])
        List.append(row[2])
        List.append(row[3])
    old_db.close()
    try:
        os.remove("DB.aes")
        os.remove("TempDB.session")
    except:
        pass
    client2 = TelegramClient(None, api_id, api_hash, device_model=TLdevice_model,
                             system_version=TLsystem_version, app_version=TLapp_version, lang_code=TLlang_code,
                             system_lang_code=TLsystem_lang_code)
    client2.session.set_dc(List[0], List[1], List[2])
    #client2.session.auth_key = AuthKey(data=List[3]) TO USE PRIOR 1.0 TELETHON VERSION
    client2._sender.state.auth_key = AuthKey(data=List[3])
    List.clear()
    StartClient1()
    client1.remove_event_handler(EventHandler, events.NewMessage(chats=ChosenChat, incoming=True))
    client1.delete_messages(ChosenChat, SecretMessage.id, revoke=True)
    StartClient2()
    print("Secret Mode's Authentication done successfully!")

def ChangeTimestampSettings():
    global NoTimestamps
    global EndDate
    while True:
        answer = None
        print()
        print("TLImporter will try to find the date for each message inside the document.\nIf they couldn't be found, these settings won't take any effect")
        print()
        print("> Timestamp setting: Choose between adding timestamps to the messages or not.")
        print("> Position setting: Choose between adding the timestamps to the beginning of the message or to the end.")
        print()
        if NoTimestamps is True:
            print("> Your current timestamp setting: No Timestamps")
        else:
            print("> Your current setting: Add Timestamp")
        if EndDate is True:
            print("> Position setting: Add Timestamps to the end of the message")
        else:
            print("> Position setting: Add Timestamps to the beginning of the message")
        print()
        print("> Available commands:")
        print(" > !1: Switch between adding Timestamps or not adding timestamps")
        print(" > !2: Switch between adding timestamps to the end or to the beginning of the messages")
        print(" > !C: Cancel and go back.")
        print()
        answer = input("Enter your command: ")
        answer.replace(" ", "")
        if not (answer == '!C' or answer == '!1' or answer == '!2'):
            while True:
                print()
                answer = input("The command you entered was invalid. Please, enter a valid command: ")
                answer.replace(" ", "")
                if (answer == "!1") or (answer == "!2") or (answer == "!C"):
                    break
        if (answer == "!C"):
            break
            return
        if (answer == "!1"):
            if NoTimestamps:
                NoTimestamps = False
            else:
                NoTimestamps = True
        if (answer == "!2"):
            if EndDate:
                EndDate = False
            else:
                EndDate = True

def ChangeHashtagsSettings():
    global AppendHashtag
    answer = None
    print()
    print("You can choose between adding the hashtag '#TLImporter' to every message imported or not, so they can be easily searchable.\nThis setting depends on what's convenient for you, but you don't need it strictly:\nTLImporter will always keep a list of all the messages sent in the database, so you can later undo the changes using TLRevert.")
    print()
    if AppendHashtag is True:
        print("> Your current setting: Add Hashtags.")
    else:
        print("> Your current setting: Don't Add Hashtags")
    print()
    print(">Available commands: ")
    print(">  !C: Cancel and go back.")
    print(">  !1: Change your settings and add hashtags to messages.")
    print(">  !2: Change your settings and don't add hashtags to messages.")
    print()
    answer = input("Enter your command: ")
    answer.replace(" ", "")
    answer.upper()
    if not (answer == '!C' or answer == '!1' or answer == '!2'):
        while True:
            print()
            answer = input("You entered an invalid command. Please, enter a valid one:")
            answer.replace(" ", "")
            answer.upper()
            if (answer == "!C") or (answer == "!1") or (answer == "!2"):
                break
    if (answer == "!C"):
        return
    if (answer == "!1"):
        AppendHashtag = True
        return
    if (answer == "!2"):
        AppendHashtag = False
        return

def ChangeDatabaseSettings():
    global SendDatabase
    answer = None
    print()
    print("TLImporter creates a database containing all the imported messages. That allows you to use TLRevert\n(https://github.com/TelegramTools/TLRevert) to undo all the changes made by TLImporter. You can also open this database using apps like SQLiteDatabaseBrowser\nhttps://github.com/sqlitebrowser/sqlitebrowser.")
    print("\nYou can choose between making a backup of the database on your Telegram's 'Saved Messages' (the chat with yourself) or don't do it.")
    print()
    if SendDatabase is True:
        print("> Your current setting: Make a Backup of the Database inside your 'Saved Messages'.")
    else:
        print("> Your current setting: Don't make a backup of the Database and keep it only in the disk.")
    print()
    print("> Available commands: ")
    print(">   !C: Cancel and go back.")
    print(">   !1: Make a backup in your 'Saved Messages'")
    print(">   !2: Don't make a backup in 'Saved Messages'")
    print()
    answer = input("Enter a command: ")
    answer.replace(" ", "")
    answer.upper()
    if not (answer == '!C' or answer == '!1' or answer == '!2'):
        while True:
            print()
            answer = input("The command you entered was invalid. Please, enter a valid one: ")
            answer.replace(" ", "")
            answer.upper()
            if (answer == "!C") or (answer == "!1") or (answer == "!2"):
                break
    if (answer == "!C"):
        return
    if (answer == "!1"):
        SendDatabase = True
        return
    if (answer == "!2"):
        SendDatabase = False
        return

def HandleExceptions():
    global SelfUser1
    global peer
    global SendDatabase
    global SoloImporting
    global RawLoopCount
    global user1
    global user2
    if not SoloImporting and RawLoopCount != 0:
        GetIncomingIdOfUser1(user1, RawLoopCount)
        GetIncomingIdOfUser2(user2, RawLoopCount)
    answer = None
    print("\n\n")
    print(
        "It seems that you have already reached some problems before. You can keep retrying again, or exit TLImporter and report this error in\nhttps://github.com/TelegramTools/TLImporter/issues.")
    print("\n\n> Available commands: ")
    print(" > !1: Try again")
    print(" > !2: Save Changes in the database and exit TLImporter")
    answer = input("\nEnter you command: ")
    answer.replace(" ", "")
    answer = answer.upper()
    if not (answer == '!1' or answer == '!2'):
        while True:
            print()
            answer = input("The command you entered was invalid. Please, enter a valid command: ")
            answer = answer.replace(" ", "")
            if (answer == "!1") or (answer == "!2"):
                break
    if (answer == "!1"):
        return
    if (answer == "!2"):
        CommitMessages(None)
        print(
            "Changes saved! You can use TLRevert in case you want to revert the changes made by TLImporter in the future.\nYou will need to start from scratch if you want to continue the merging process later.")
        if SendDatabase is True:
            print(
                "You have chosen to make a copy of your database in your 'Saved Messages' inside Telegram.\nBacking up database...")
            databasecopy = SendFileClient1(SelfUser1, file="data\TLImporter-Database.db",
                                           caption="This is the TLImporter's database with " + peer)
            SendMessageClient1(SelfUser1,
                               "💾 You can read this database using programs like https://github.com/sqlitebrowser/sqlitebrowser/releases. This database is **mandatory** if you want to use [TLRevert](https://github.com/TelegramTools/TLRevert) in order to revert all the changes made by TLImporter. Read the manuals of both programs if you have any doubt about them. **Thank you very much for using** [TLImporter](https://github.com/TelegramTools/TLImporter)**!**\n\n**--ferferga**",
                               reply_to=databasecopy.id)
        getpass.getpass("\n\nYou can close TLImporter by pressing ENTER: ")
        sys.exit(0)
    return

def countdown(t):
    print("\n\n")
    while t:
        timeformat = '--> We have reached a flood limitation. Waiting for: ' + str(datetime.timedelta(seconds=t))
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1

def SendFileClient1(*args, **kwargs):
    global ExceptionReached
    try:
        return client1.send_file(*args, allow_cache=False, **kwargs)
    except FloodWaitError as e:
        logging.exception("TLImporter FLOODEXCEPTION IN SendFileClient1: " + str(e))
        countdown(e.seconds)
        return SendFileClient1(*args, **kwargs)
    except Exception as e:
        logging.exception("TLImporter TELEGRAMEXCEPTION IN SendFileClient1: " + str(e))
        print("\nSomething went wrong in Telegram's side. This is the full exception:\n\n"  + str(e))
        ExceptionReached = True
        if ExceptionReached is False:
            getpass.getpass("Press ENTER to try again: ")
            ExceptionReached = True
        else:
            HandleExceptions()
        return SendFileClient1(*args, **kwargs)

def SendMessageClient1(*args, **kwargs):
    global ExceptionReached
    try:
        return client1.send_message(*args, **kwargs)
    except FloodWaitError as e:
        logging.exception("TLImporter FLOODEXCEPTION IN SendMessageClient1: " + str(e))
        countdown(e.seconds)
        return SendMessageClient1(*args, **kwargs)
    except Exception as e:
        logging.exception("TLImporter TELEGRAMEXCEPTION IN SendMessageClient1: " + str(e))
        print("\nSomething went wrong in Telegram's side. This is the full exception:\n\n"  + str(e))
        if ExceptionReached is False:
            getpass.getpass("Press ENTER to try again: ")
            ExceptionReached = True
        else:
            HandleExceptions()
        return SendMessageClient1(*args, **kwargs)

def SendMessageClient2(*args, **kwargs):
    global ExceptionReached
    try:
        return client2.send_message(*args, **kwargs)
    except FloodWaitError as e:
        logging.exception("TLImporter FLOODEXCEPTION IN SendMessageClient2: " + str(e))
        countdown(e.seconds)
        return SendMessageClient2(*args, **kwargs)
    except Exception as e:
        logging.exception("TLImporter TELEGRAMEXCEPTION IN SendMessageClient2: " + str(e))
        print("\nSomething went wrong in Telegram's side. This is the full exception:\n\n"  + str(e))
        if ExceptionReached is False:
            getpass.getpass("Press ENTER to try again: ")
            ExceptionReached = True
        else:
            HandleExceptions()
        return SendMessageClient2(*args, **kwargs)

def GetIncomingIdOfUser2(u, lim):
    global ExceptionReached
    global User1IDs
    try:
        message = client1.get_messages(u, limit=lim)
        for msg in message:
            if msg.id not in User1IDs:
                User1IDs.append(msg.id)
        message.clear()
        return
    except FloodWaitError as e:
        logging.exception("TLImporter FLOODEXCEPTION IN GETINCOMINGIDOFUSER2: " + str(e))
        #print("\n\nWe have reached a flood limitation. Waiting for " + str(datetime.timedelta(seconds=e.seconds)))
        countdown(e.seconds)
        return GetIncomingIdOfUser2(u, lim)
    except Exception as e:
        logging.exception("TLImporter TELEGRAMEXCEPTION IN GETINCOMINGIDOFUSER2: " + str(e))
        print("Something went wrong in Telegram's side. This is the full exception:\n\n"  + str(e))
        if ExceptionReached is False:
            getpass.getpass("Press ENTER to try again: ")
            ExceptionReached = True
        else:
            HandleExceptions()
        return GetIncomingIdOfUser2(u, lim)

def GetIncomingIdOfUser1(u, lim):
    global ExceptionReached
    global User2IDs
    try:
        message = client2.get_messages(u, limit=lim)
        for msg in message:
            if msg.id not in User2IDs:
                User2IDs.append(msg.id)
        message.clear()
        return
    except FloodWaitError as e:
        logging.exception("TLImporter FLOODEXCEPTION IN GETINCOMINGIDOFUSER1: " + str(e))
        countdown(e.seconds)
        return GetIncomingIdOfUser1(u, lim)
    except Exception as e:
        logging.exception("TLImporter TELEGRAMEXCEPTION IN GETINCOMINGIDOFUSER1: " + str(e))
        print("\nSomething went wrong in Telegram's side. This is the full exception:\n\n"  + str(e))
        if ExceptionReached is False:
            getpass.getpass("Press ENTER to try again: ")
            ExceptionReached = True
        else:
            HandleExceptions()
        return GetIncomingIdOfUser1(u, lim)

def CreateTables():
    db = DBConnection(False, False)
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE ImportedMessages(User1 BOOLEAN, Sender TEXT, Date TEXT, Message TEXT)''')
    cursor.execute('''
    CREATE TABLE SentMessagesIDs(User1 INTEGER, User2 INTEGER)''')
    cursor.execute('''
        CREATE TABLE Statistics(User1ID INTEGER, User2ID INTEGER, NameUser1 TEXT, NameUser2 TEXT, TotalCountUser1 INTEGER, TotalCountUser2 INTEGER, AffectedMessages INTEGER, SoloMode BOOLEAN)''')
    cursor.execute('''
        CREATE TABLE Settings(NameUser1 TEXT, NameUser2 TEXT, FileName TEXT, FilePath TEXT, SoloMode BOOLEAN)''')
    cursor.execute('''
    CREATE TABLE Version(AppName TEXT, AppVersion TEXT, CreationDate TEXT)''')
    db.commit()
    date = str(datetime.datetime.today())
    reg = ("TLImporter", "3.0", date)
    db.execute("INSERT INTO Version VALUES(?,?,?)", reg)
    db.commit()

def DBConnection(first, close):
    try:
        conn = sqlite3.connect("TLImporter-DB.db")
        if first is True:
            print("Created database successfully!")
        if close is True:
            conn.close()
            return
        return conn
    except sqlite3.OperationalError:
        print("ERROR 1: DATABASE OPERATION ERROR! Trying again...")
        DBConnection(first, close)

def CommitMessages(database):
    global User1IDs
    global User2IDs
    global SelfUser1
    global SelfUser2
    try:
        database.commit()
    except:
        pass
    for id1 in User1IDs:
        reg5 = (id1, None)
        database.execute("INSERT INTO SentMessagesIDs VALUES(?,?)", reg5)
    database.commit()
    LoopingCount = 0
    for id1 in User1IDs:
        if len(User2IDs) != 0:
            database.execute("UPDATE SentMessagesIDs SET User2={id} WHERE User1={user1id}". \
                             format(user1id=id1, id=User2IDs.pop(0)))
            LoopingCount = LoopingCount + 1
        else:
            break
    if len(User2IDs) != 0:
        for id2 in User2IDs:
            reg5 = (None, id2)
            database.execute("INSERT INTO SentMessagesIDs VALUES(?,?)", reg5)
    database.commit()
    return

def CheckMessages():
    global SoloImporting
    global NameUser1
    global NameUser2
    global SelfUser1
    global SelfUser2
    global incorrectname
    global LineCount
    global User1Count
    global User2Count
    global ValidFile
    global TotalCount
    print()
    if SoloImporting is True:
        NameUser1 = input("Who is one of the partners?: ")
    else:
        NameUser1 = input("Who will be you (+" + SelfUser1.phone + ") in this chat?: ")
    while True:
        if NameUser1 is None:
            NameUser1 = input(incorrectname)
        if NameUser1 is not None:
            NameUser1 = NameUser1.replace(":", "")
            break
    print()
    if SoloImporting is True:
        NameUser2 = input("Who is the other partner?: ")
    else:
        NameUser2 = input("Who will be " + SelfUser2.first_name + " (+" + SelfUser2.phone + ") in this chat?: ")
    while True:
        if NameUser2 is None:
            NameUser2 = input(incorrectname)
        if NameUser2 is not None:
            NameUser2 = NameUser2.replace(":", "")
            break
    if SoloImporting is True:
        print("\nOne of the partners is " + NameUser1 + " and the other one is " + NameUser2 + ". Checking if the file is valid to be imported...\n")
    else:
        print("\nYou are " + NameUser1 + " and your partner (+" + SelfUser2.phone + ") is " + NameUser2 + ". Checking if the file is valid to be imported...\n")
        print()
    with open(FilePath, mode="r", encoding="utf-8") as f:
        User1Found = False
        User2Found = False
        for line in f:
            TotalCount = TotalCount + 1
            if line.find(NameUser1 + ":") != -1:
                User1Found = True
                User1Count = User1Count + 1
            elif line.find(NameUser2 + ":") != -1:
                User2Found = True
                User2Count = User2Count + 1
        if TotalCount != (User1Count + User2Count):
            TotalCount = User1Count + User2Count
        if User1Found and User2Found:
            ValidFile = True
        else:
            ValidFile = False
            return

def DumpDB():
    global TotalCount
    global NameUser1
    global NameUser2
    global FilePath
    global Filename
    bar = progressbar.ProgressBar(max_value=TotalCount)
    bar.start()
    completed = 0
    with open(FilePath, mode="r", encoding="utf-8") as f:
        Filename = os.path.basename(FilePath)
        db = DBConnection(False, False)
        User1 = False
        Msg = []
        User1 = False
        User2 = False
        header = None
        Iterated = False
        for l in f:
            if (l.find(": " + NameUser1 + ":") != -1 or l.find(": " + NameUser2 + ":") != -1) and Iterated:
                if User1:
                    reg4 = (True, NameUser1, header, Msg[0])
                elif User2:
                    reg4 = (False, NameUser2, header, Msg[0])
                db.execute("INSERT INTO ImportedMessages VALUES(?,?,?,?)", reg4)
            elif Iterated:
                Msg[0] = Msg[0] + l

            if l.find(": " + NameUser1 + ":") != -1:
                Iterated = True
                header = None
                Msg.clear()
                header, msg = l.split(": " + NameUser1 + ": ")
                Msg.append(msg)
                User1 = True
                User2 = False
            elif l.find(": " + NameUser2 + ":") != -1:
                Iterated = True
                header = None
                Msg.clear()
                header, msg = l.split(": " + NameUser2 + ": ")
                Msg.append(msg)
                User1 = False
                User2 = True
            completed = completed + 1
            try:
                bar.update(completed)
            except:
                pass
        if len(Msg) != 0:
            if User1:
                reg4 = (True, NameUser1, header, Msg[0])
            elif User2:
                reg4 = (False, NameUser2, header, Msg[0])
            db.execute("INSERT INTO ImportedMessages VALUES(?,?,?,?)", reg4)
        Msg.clear()
        db.commit()
        bar.finish()

def ExportMessages():
    global NoTimestamps
    global EndDate
    global SelfUser2
    global SelfUser1
    global User2IDs
    global User1IDs
    global TotalCount
    global NameUser2
    global NameUser1
    global RawLoopCount
    global user1
    global user2
    global Filename
    global FilePath
    print("\nYou can cancel at any time pressing CTRL+C keyboard combination.")
    print("\nINFORMATION: Each 2000 messages, a pause of around 7 minutes will be done for reducing Telegram's flood limits.\nBe patient, the process will be still going on.\n")
    try:
        if SoloImporting:
            user1 = client1.get_me()
        else:
            try:
                user2 = client1.get_input_entity(SelfUser2.phone)
            except:
                client1.get_dialogs(limit=None)
                user2 = client1.get_input_entity(SelfUser2.id)
            try:
                user1 = client2.get_input_entity(SelfUser1.phone)
            except:
                client2.get_dialogs(limit=None)
                user1 = client2.get_input_entity(SelfUser1.id)
        bar = progressbar.ProgressBar(max_value=TotalCount)
        bar.start()
        completed = 0
        database = DBConnection(False, False)
        if not SoloImporting:
            reg1 = (SelfUser1.id, SelfUser2.id, SelfUser1.first_name + " (+" + SelfUser1.phone + ")", SelfUser2.first_name + " (+" + SelfUser2.phone + ")", client1.get_messages(user2, 0).total, client2.get_messages(user1, 0).total, TotalCount, SoloImporting)
            welcmsg = SendMessageClient1(user2, "📲`IMPORTING THE CHAT WITH` __" + NameUser1 + "__ and __" + NameUser2 + "__ using `" + Filename + "` as source file. __'" + NameUser2 + "'__ is **" + SelfUser2.first_name + "** now.")
        else:
            reg1 = (SelfUser1.id, None, SelfUser1.first_name + " (+" + SelfUser1.phone + ")", None, client1.get_messages(user1, 0).total, None, TotalCount, SoloImporting)
            welcmsg = SendMessageClient1(user2, "📲`IMPORTING THE CHAT WITH` __" + NameUser1 + "__ and __" + NameUser2 + "__ using `" + Filename + "` as source file.")
        reg2 = (NameUser1, NameUser2, Filename, FilePath, SoloImporting)
        database.execute("INSERT INTO Statistics VALUES(?,?,?,?,?,?,?,?)", reg1)
        database.execute("INSERT INTO Settings VALUES(?,?,?,?,?)", reg2)
        database.commit()
        User1IDs.append(welcmsg.id)
        if not SoloImporting:
            GetIncomingIdOfUser1(user1, 1)
        db = database.cursor()
        db.execute('SELECT * FROM ImportedMessages')
        for row in db:
            Out = None
            Date = None
            Message = None
            Sender = None
            list = None
            LongMessage = False
            if row[0] == 0:
                Out = False
            else:
                Out = True

            if NoTimestamps:
                if SoloImporting:
                    Sender = "`" + row[1] + ":`\n"
                else:
                    Date = None
                    Sender = None
            else:
                if SoloImporting and EndDate:
                    Sender = "`" + row[1] + ":`\n"
                else:
                    Sender = None
                if EndDate:
                    Date = "`[" + row[2] + "]`"
                elif SoloImporting:
                    Date = "`[" + row[2] + "] " + row[1] + ":`\n"
                else:
                    Date = "`[" + row[2] + "]`\n"
            Message = row[3]

            if NoTimestamps:
                if len(Message) > 4096:
                    if not SoloImporting:
                        n = 4096
                    else:
                        n = 4096 - len(Sender)
                    list = [Message[i:i + n] for i in range(0, len(Message), n)]
                elif SoloImporting and len(Message+Sender) > 4096:
                    LongMessage = True
            else:
                if len(Message) > 4096:
                    if not SoloImporting:
                        n = 4096 - len(Date)
                    else:
                        n = 4096 - len(Date) - len(Sender)
                    list = [Message[i:i + n] for i in range(0, len(Message), n)]
                elif not SoloImporting and len(Message+Date) > 4096:
                    LongMessage = True
                elif SoloImporting and len(Message+Date+Sender) > 4096:
                    LongMessage = True

            if list is None:
                if LongMessage:
                    if SoloImporting:
                        if NoTimestamps:
                            msg = SendMessageClient1(user1, Sender)
                            msg2 = SendMessageClient1(user1, Message, reply_to=msg.id)
                            User1IDs.append(msg.id)
                            User1IDs.append(msg2.id)
                        else:
                            msg = SendMessageClient1(user1, Date)
                            msg2 = SendMessageClient1(user1, Message, reply_to=msg.id)
                            User1IDs.append(msg.id)
                            User1IDs.append(msg2.id)
                    else:
                        if Out:
                            msg = SendMessageClient1(user2, Date)
                            msg2 = SendMessageClient1(user2, Message, reply_to=msg.id)
                            User1IDs.append(msg.id)
                            User1IDs.append(msg2.id)
                        else:
                            msg = SendMessageClient2(user1, Date)
                            msg2 = SendMessageClient2(user1, Message, reply_to=msg.id)
                            User2IDs.append(msg.id)
                            User2IDs.append(msg2.id)
                else:
                    if SoloImporting:
                        if NoTimestamps:
                            msg = SendMessageClient1(user1, Sender+Message)
                        elif EndDate:
                            msg = SendMessageClient1(user1, Sender + Message + Date)
                        else:
                            msg = SendMessageClient1(user1, Date + Sender + Message)
                        User1IDs.append(msg.id)
                    else:
                        if Out:
                            if NoTimestamps:
                                msg = SendMessageClient1(user2, Message)
                            elif EndDate:
                                msg = SendMessageClient1(user2, Message + Date)
                            else:
                                msg = SendMessageClient1(user2, Date + Message)
                            User1IDs.append(msg.id)
                        else:
                            if NoTimestamps:
                                msg = SendMessageClient2(user1, Message)
                            elif EndDate:
                                msg = SendMessageClient2(user1, Message + Date)
                            else:
                                msg = SendMessageClient2(user1, Date + Message)
                            User2IDs.append(msg.id)
            else:
                LoopCount = 0
                IDs = []
                if SoloImporting:
                    if NoTimestamps:
                        for m in list:
                            if LoopCount == 0:
                                msg = SendMessageClient1(user1, Sender + m)
                            else:
                                msg = SendMessageClient1(user1, Sender + m, reply_to=IDs[LoopCount - 1])
                            LoopCount = LoopCount + 1
                            IDs.append(msg.id)
                            User1IDs.append(msg.id)
                    elif EndDate:
                        for m in list:
                            if LoopCount == 0:
                                msg = SendMessageClient1(user1, Sender + m + Date)
                            else:
                                msg = SendMessageClient1(user1, Sender + m + Date, reply_to=IDs[LoopCount - 1])
                            LoopCount = LoopCount + 1
                            IDs.append(msg.id)
                            User1IDs.append(msg.id)
                    else:
                        for m in list:
                            if LoopCount == 0:
                                msg = SendMessageClient1(user1, Date + m)
                            else:
                                msg = SendMessageClient1(user1, Date + m, reply_to=IDs[LoopCount - 1])
                            LoopCount = LoopCount + 1
                            IDs.append(msg.id)
                            User1IDs.append(msg.id)
                else:
                    if Out:
                        if NoTimestamps:
                            for m in list:
                                if LoopCount == 0:
                                    msg = SendMessageClient1(user2, m)
                                else:
                                    msg = SendMessageClient1(user2, m, reply_to=IDs[LoopCount - 1])
                                LoopCount = LoopCount + 1
                                IDs.append(msg.id)
                                User1IDs.append(msg.id)
                        elif EndDate:
                            for m in list:
                                if LoopCount == 0:
                                    msg = SendMessageClient1(user2, m + Date)
                                else:
                                    msg = SendMessageClient1(user2, m + Date, reply_to=IDs[LoopCount - 1])
                                LoopCount = LoopCount + 1
                                IDs.append(msg.id)
                                User1IDs.append(msg.id)
                        else:
                            for m in list:
                                if LoopCount == 0:
                                    msg = SendMessageClient1(user2, Date + m)
                                else:
                                    msg = SendMessageClient1(user2, Date + m, reply_to=IDs[LoopCount - 1])
                                LoopCount = LoopCount + 1
                                IDs.append(msg.id)
                                User1IDs.append(msg.id)
                    else:
                        if NoTimestamps:
                            for m in list:
                                if LoopCount == 0:
                                    msg = SendMessageClient2(user1, m)
                                else:
                                    msg = SendMessageClient2(user1, m, reply_to=IDs[LoopCount - 1])
                                LoopCount = LoopCount + 1
                                IDs.append(msg.id)
                                User2IDs.append(msg.id)
                        elif EndDate:
                            for m in list:
                                if LoopCount == 0:
                                    msg = SendMessageClient2(user1, m + Date)
                                else:
                                    msg = SendMessageClient2(user1, m + Date, reply_to=IDs[LoopCount - 1])
                                LoopCount = LoopCount + 1
                                IDs.append(msg.id)
                                User2IDs.append(msg.id)
                        else:
                            for m in list:
                                if LoopCount == 0:
                                    msg = SendMessageClient2(user1, Date + m)
                                else:
                                    msg = SendMessageClient2(user1, Date + m, reply_to=IDs[LoopCount - 1])
                                LoopCount = LoopCount + 1
                                IDs.append(msg.id)
                                User2IDs.append(msg.id)
                IDs.clear()
                LoopCount = 0

            RawLoopCount = RawLoopCount + 1
            completed = completed + 1
            bar.update(completed)
            # For avoiding some flood limits, it seems better to me to also gather the ids of the messages in the other account
            # instead of doing it when all it's finished.
            if not SoloImporting and RawLoopCount == 2000:
                GetIncomingIdOfUser2(user2, 2000)
                GetIncomingIdOfUser1(user1, 2000)
                RawLoopCount = 0
                time.sleep(420)
            elif RawLoopCount == 2000 and SoloImporting:
                RawLoopCount = 0
                time.sleep(420)
        if RawLoopCount != 0 and not SoloImporting:
            GetIncomingIdOfUser2(user2, RawLoopCount)
            GetIncomingIdOfUser1(user1, RawLoopCount)
            RawLoopCount = 0
        client1.send_read_acknowledge(user2, max_id=0)
        client2.send_read_acknowledge(user1, max_id=0)
        if SoloImporting:
            confirm = SendMessageClient1(user1, "✅ **SUCCESS!!**\nSuccessfully imported **" + str(TotalCount) + "** messages. **" + str(User1Count) + "** messages were from `" + NameUser1 + "` and **" + str(User2Count) + "** messages were from `" + NameUser2 + "`.\nThis chat now contains **" + str(client1.get_messages(user1, 0).total) + "** messages.\n\nThank you very much for using TLImporter!\n\n**--ferferga** ✅")
            User1IDs.append(confirm.id)
        else:
            confirm = SendMessageClient1(user2, "✅ **SUCCESS!!**\nSuccessfully imported **" + str(
                TotalCount) + "** messages. **" + str(
                User1Count) + "** messages were from `" + NameUser1 + "` and **" + str(
                User2Count) + "** messages were from `" + NameUser2 + "`.\nThis chat now contains **" + str(client1.get_messages(user2, 0).total) + "** messages.\n\nThank you very much for using TLImporter!\n\n**--ferferga** ✅")
            User1IDs.append(confirm.id)
            GetIncomingIdOfUser1(user1, 1)
        CommitMessages(database)
        bar.finish()
        print("\n\nThe process has been finished correctly!")

    except KeyboardInterrupt:
        print("\nThe process has been cancelled. Saving changes in the database...")
        if RawLoopCount != 0 and not SoloImporting:
            GetIncomingIdOfUser2(user2, RawLoopCount)
            GetIncomingIdOfUser1(user1, RawLoopCount)
            RawLoopCount = 0
        CommitMessages(database)
        DBConnection(False, True)
        print(
            "Changes saved! You will be able to use TLRevert to revert the changes made by TLImporter in the future, and remove all the messages sent by the application.\nYou will need to start from scratch if you want to continue the merging process later.")
        if SendDatabase is True:
            print(
                "You have chosen to make a copy of your database in your 'Saved Messages' inside Telegram.\nBacking up database...")
            databasecopy = SendFileClient1(SelfUser1, file="TLImporter-DB.db",
                                           caption="This is the TLImporter's database between " + NameUser1 + " and " + NameUser2)
            SendMessageClient1(SelfUser1,
                               "💾 You can read this database using programs like https://github.com/sqlitebrowser/sqlitebrowser/releases. This database is **mandatory** if you want to use [TLRevert](https://github.com/TelegramTools/TLRevert) in order to revert all the changes made by TLImporter. Read the manuals of both programs if you have any doubt about them. **Thank you very much for using** [TLImporter](https://github.com/TelegramTools/TLImporter)**!**\n\n**--ferferga**",
                               reply_to=databasecopy.id)
        else:
            return
    except Exception as e:
        logging.exception("TLIMPORTER EXCEPTION IN EXPORTINGMESSAGES: " + str(e))
        bar.finish()
        print("Something went wrong in our side. This is the full exception:\n\n"  + str(e))
        print("\nSaving changes in the database, so you can use TLRevert to revert the changes made by TLImporter and remove all the messages sent by the application...")
        if RawLoopCount != 0 and not SoloImporting:
            GetIncomingIdOfUser2(user2, RawLoopCount)
            GetIncomingIdOfUser1(user1, RawLoopCount)
            RawLoopCount = 0
        CommitMessages(database)
        DBConnection(False, True)
        if SendDatabase is True:
            print("You have chosen to make a copy of your database in your 'Saved Messages' inside Telegram.\nBacking up database...")
            if SoloImporting:
                databasecopy = SendFileClient1(SelfUser1, file="TLImporter-DB.db",
                                               caption="This is the TLImporter's database between " + NameUser1 + " and " + NameUser2)
            else:
                databasecopy = SendFileClient1(SelfUser1, file="TLImporter-DB.db",
                                               caption="This is the TLImporter's database with your partner " + SelfUser2.first_name + "(+" + SelfUser2.phone + ")")
            SendMessageClient1(SelfUser1,
                               "💾 You can read this database using programs like https://github.com/sqlitebrowser/sqlitebrowser/releases. This database is **mandatory** if you want to use [TLRevert](https://github.com/TelegramTools/TLRevert) in order to revert all the changes made by TLImporter. Read the manuals of both programs if you have any doubt about them. **Thank you very much for using** [TLImporter](https://github.com/TelegramTools/TLImporter)**!**\n\n**--ferferga**", reply_to=databasecopy.id)
        getpass.getpass("This part of the process can't be recovered. Press ENTER to close the app...")
        sys.exit(0)

##ENTRY POINT OF THE CODE
try:
    os.remove("TLImporter-log.log")
except:
    pass
logging.basicConfig(filename="TLImporter-log.log", level=logging.DEBUG, format='%(asctime)s %(message)s')
getpass.getpass("HELLO! WELCOME TO TELEGRAM CHAT IMPORTER!\n\nThis app will import your TXT conversations from third-party apps (like WhatsApp) into your existing Telegram Chat with your partner. \nRead all the documentation on the GitHub page (https://github.com/TelegramTools/TLImporter/wiki) for all the important information.\n\nPress ENTER to continue")
getpass.getpass("\n\nWARNING: Telegram allows only a specific and unknown amount of messages within a specific timeframe for security reasons. You might not be able to message friends for a small period of time.\nThis is known as a 'flood limitation'.\n\nThus, I suggest you to do this at night or in a period of time that you do not need to use Telegram. Check https://github.com/TelegramTools/TLImporter/wiki/Before-starting for more information. Press ENTER to continue.")
print("\n\nLogging you into Telegram...")
StartClient1()
print("\n\nYou are logged in as " + SelfUser1.first_name + "!")
try:
    os.remove("TLImporter-DB.db")
except:
    pass
print("\nCreating database...")
DBConnection(True, False)
CreateTables()
while True:
    answer = None
    answer = input("Do you want to import a conversation using two users, in a 1:1 format? Otherwise, the chat will be imported inside your 'Saved Messages'. [y/n]: ")
    answer = answer.replace(" ", "")
    answer = answer.upper()
    if not (answer == 'Y' or answer == 'N'):
        while True:
            print()
            answer = input("The command you entered was not valid. Please, enter a valid one: ")
            answer = answer.replace(" ", "")
            answer = answer.upper()
            if (answer == "Y") or (answer == "N"):
                break
    if answer == "Y":
        SoloImporting = False
        break
    if answer == "N":
        SoloImporting = True
        break
if SoloImporting is False:
    print("\n\nNow, you have to log in your partner in Telegram...\n")
    while True:
        answer = None
        answer = input(
            "\nDo you want to log in your partner using the 'Secret Mode'? Refer to the documentation in GitHub (check https://github.com/TelegramTools/TLSecret as well) for more information. [y/n]: ")
        answer = answer.replace(" ", "")
        answer = answer.upper()
        if not (answer == 'Y' or answer == 'N'):
            while True:
                print()
                answer = input("The command you entered was not valid. Please, enter a valid one: ")
                answer = answer.replace(" ", "")
                answer = answer.upper()
                if (answer == "Y") or (answer == "N"):
                    break
        if answer == "Y":
            SecretMode = True
            break
        if answer == "N":
            SecretMode = False
            break
    if SecretMode:
        StartSecretMode()
    else:
        client2 = TelegramClient('User2', api_id, api_hash, device_model=TLdevice_model,
                                 system_version=TLsystem_version, app_version=TLapp_version, lang_code=TLlang_code,
                                 system_lang_code=TLsystem_lang_code)
        print("")
        StartClient2()
    print ("\n\nYour partner is logged in as " + SelfUser2.first_name + " (+" + SelfUser2.phone + ")")
    print('\n\nYou are going to copy a conversation from ' + SelfUser1.first_name + ' (+' + SelfUser1.phone + ') to ' + SelfUser2.first_name + ' (+' + SelfUser2.phone + ')')
else:
    print("\n\nYou are going to import the conversation in your Telegram's 'Saved Messages' section.")
while True:
    FilePath = input("""\nIt's time to type the path of the file to import. You can also drag and drop it here to get the full path easily.\n\nPath of the file: """)
    if FilePath is None:
        print("You have entered a invalid path. Try again.")
        continue
    else:
        try:
            FilePath = FilePath.replace('"', "")
        except:
            pass
    if not os.path.isfile(FilePath):
        print("You have entered a wrong path, no file could be found. Try again.")
        continue
    else:
        CheckMessages()
        if ValidFile is True:
            break
        else:
            print(NameUser1 + " and " + NameUser2 + " couldn't be found in " + FilePath + ".\n")
            print("This file is not valid. I'm going to ask you again the filepath and the name of the users.\nMake sure that you set up everything accordingly. Read the FAQ (https://github.com/TelegramTools/TLImporter/wiki/Importing-chats) for more information.")
print("This file is valid to be imported. It has " + str(TotalCount) + " lines in total.")
print("\n" + NameUser1 + " has " + str(User1Count) + " messages. " + NameUser2 + " has " + str(User2Count) + " messages.")
print("\nProcessing and saving messages in the database...")
DumpDB()
print("\nSuccessfully completed!")
print("\n\nNow, before importing the chat, we will set up a few settings:\n")
print()
while True:
    print("Here are your current settings:\n")
    if NoTimestamps is True:
        print("> 1. Timestamps settings: Don't add timestamps")
    else:
        print("> 1. Timestamps settings: Add Timestamps")
    if EndDate is True:
        print(">     - Position: End of the message")
    else:
        print(">     - Position: Beginning of the message")
    if AppendHashtag is True:
        print("> 2. Add hashtags to each message: Yes")
    else:
        print("> 2. Add hashtags to each message: No")
    if SendDatabase is True:
        print("> 4. Backup of the database in 'Saved Messages': Yes")
    else:
        print("> 4. Backup of the database in 'Saved Messages': No")
    print()
    print("> Available commands: ")
    print("  !C: Confirm these settings and start the import of the chat")
    print("  !1: See a description and change timestamps settings")
    print("  !2: See a description and change hashtags settings")
    print("  !3: See a description and change Database settings")
    print()
    answer = str(input("Enter a command: "))
    answer = answer.replace(" ", "")
    answer = answer.upper()
    if not (answer == '!C' or answer == '!1' or answer == '!2' or answer == '!3'):
        while True:
            print()
            answer = input("The command you entered was not valid. Please, enter a valid one: ")
            answer = answer.replace(" ", "")
            answer = answer.upper()
            if (answer == "!C") or (answer == "!1") or (answer == "!2") or (answer == "!3"):
                break
    if (answer == "!C"):
        break
    if (answer == "!1"):
        ChangeTimestampSettings()
    if (answer == "!2"):
        ChangeHashtagsSettings()
    if (answer == "!3"):
        ChangeDatabaseSettings()
print("STARTED! Importing the conversation in Telegram...")
print()
ExportMessages()
print("\n")
getpass.getpass("Press ENTER to log out: ")
print('Logging ' + SelfUser1.first_name + ' (+' + SelfUser1.phone + ') and ' + SelfUser2.first_name + ' (+' + SelfUser2.phone + ') out of Telegram...')
client1.log_out()
client2.log_out()
print("Thank you very much for using the app!\n\n--ferferga\n\nGOODBYE!")
print()
getpass.getpass("Press ENTER to close the app: ")
sys.exit(0)
